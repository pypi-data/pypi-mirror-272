import json
import os
import shutil
import urllib.request
import urllib.parse
import zipfile
import torch
import torch.nn as nn
# import tensorflow as tf
from typing import Dict, List, Optional, Tuple, Union
import enum
import re
from collections import defaultdict


def named_module_tensors(
        module: nn.Module, include_buffers: bool = True, recurse: bool = False, remove_non_persistent: bool = False
):
    """
    A helper function that gathers all the tensors (parameters + buffers) of a given module. If `include_buffers=True`
    it's the same as doing `module.named_parameters(recurse=recurse) + module.named_buffers(recurse=recurse)`.

    Args:
        module (`torch.nn.Module`):
            The module we want the tensors on.
        include_buffer (`bool`, *optional*, defaults to `True`):
            Whether or not to include the buffers in the result.
        recurse (`bool`, *optional`, defaults to `False`):
            Whether or not to go look in every submodule or just return the direct parameters and buffers.
        remove_non_persistent (`bool`, *optional*, defaults to `False`):
            Whether or not to remove the non persistent buffer from the buffers. Useful only when include_buffers =
            True
    """
    for named_parameter in module.named_parameters(recurse=recurse):
        yield named_parameter

    if include_buffers:
        non_persistent_buffers = set()
        if remove_non_persistent:
            non_persistent_buffers = get_non_persistent_buffers(module, recurse=recurse)
        for named_buffer in module.named_buffers(recurse=recurse):
            name, _ = named_buffer
            if name not in non_persistent_buffers:
                yield named_buffer


def get_non_persistent_buffers(module: nn.Module, recurse: bool = False):
    """
    Gather all non persistent buffers of a given modules into a set

    Args:
        module (`nn.Module`):
            The module we want the non persistent buffers on.
        recurse (`bool`, *optional*, defaults to `False`):
            Whether or not to go look in every submodule or just return the direct non persistent buffers.
    """

    non_persistent_buffers_set = module._non_persistent_buffers_set
    if recurse:
        for _, m in module.named_modules():
            non_persistent_buffers_set |= m._non_persistent_buffers_set

    return non_persistent_buffers_set


class CustomDtype(enum.Enum):
    r"""
    An enum that contains multiple custom dtypes that can be used for `infer_auto_device_map`.
    """
    FP8 = "fp8"
    INT4 = "int4"


def dtype_byte_size(dtype: torch.dtype):
    """
    Returns the size (in bytes) occupied by one parameter of type `dtype`.

    Example:

    ```py
    >>> dtype_byte_size(torch.float32)
    4
    ```
    """
    if dtype == torch.bool:
        return 1 / 8
    elif dtype == CustomDtype.INT4:
        return 1 / 2
    elif dtype == CustomDtype.FP8:
        return 1
    bit_search = re.search(r"[^\d](\d+)$", str(dtype))
    if bit_search is None:
        raise ValueError(f"`dtype` is not a valid dtype: {dtype}.")
    bit_size = int(bit_search.groups()[0])
    return bit_size // 8


def _get_proper_dtype(dtype: Union[str, torch.device]) -> torch.dtype:
    """
    Just does torch.dtype(dtype) if necessary.
    """
    if isinstance(dtype, str):
        # We accept "torch.float16" or just "float16"
        dtype = dtype.replace("torch.", "")
        dtype = getattr(torch, dtype)
    return dtype


def compute_module_sizes(
        model: nn.Module,
        dtype: Optional[Union[str, torch.device]] = None,
        special_dtypes: Optional[Dict[str, Union[str, torch.device]]] = None,
):
    """
    Compute the size of each submodule of a given model.
    """
    if dtype is not None:
        dtype = _get_proper_dtype(dtype)
        dtype_size = dtype_byte_size(dtype)
    if special_dtypes is not None:
        special_dtypes = {key: _get_proper_dtype(dtyp) for key, dtyp in special_dtypes.items()}
        special_dtypes_size = {key: dtype_byte_size(dtyp) for key, dtyp in special_dtypes.items()}
    module_sizes = defaultdict(int)
    for name, tensor in named_module_tensors(model, recurse=True):
        if special_dtypes is not None and name in special_dtypes:
            size = tensor.numel() * special_dtypes_size[name]
        elif dtype is None:
            size = tensor.numel() * dtype_byte_size(tensor.dtype)
        else:
            size = tensor.numel() * min(dtype_size, dtype_byte_size(tensor.dtype))
        name_parts = name.split(".")
        for idx in range(len(name_parts) + 1):
            module_sizes[".".join(name_parts[:idx])] += size

    return module_sizes


def calculate_maximum_sizes(model):
    if isinstance(model, torch.nn.Module):
        return calculate_maximum_sizes_torch(model)
    # elif isinstance(model, tf.keras.Model):
    #     return calculate_maximum_sizes_tf(model)
    else:
        raise ValueError("Unsupported model type")


# def calculate_maximum_sizes_tf(model):
#     """为TensorFlow模型计算大小"""
#     total_size = 0
#     largest_layer = None
#     largest_layer_size = 0
#
#     for layer in model.layers:
#         layer_size = sum(tf.size(v).numpy() * v.dtype.size for v in layer.trainable_variables)
#         if layer_size > largest_layer_size:
#             largest_layer_size = layer_size
#             largest_layer = layer.name
#         total_size += layer_size
#
#     return total_size, largest_layer


def calculate_maximum_sizes_torch(model: torch.nn.Module):
    "Computes the total size of the model and its largest layer"
    sizes = compute_module_sizes(model)
    # `transformers` models store this information for us
    no_split_modules = getattr(model, "_no_split_modules", None)
    if no_split_modules is None:
        no_split_modules = []

    modules_to_treat = (
            list(model.named_parameters(recurse=False))
            + list(model.named_children())
            + list(model.named_buffers(recurse=False))
    )
    largest_layer = get_max_layer_size(modules_to_treat, sizes, no_split_modules)
    total_size = sizes[""]
    return total_size, largest_layer


def get_max_layer_size(
        modules: List[Tuple[str, torch.nn.Module]], module_sizes: Dict[str, int], no_split_module_classes: List[str]
):
    """
    Utility function that will scan a list of named modules and return the maximum size used by one full layer. The
    definition of a layer being:
    - a module with no direct children (just parameters and buffers)
    - a module whose class name is in the list `no_split_module_classes`

    Args:
        modules (`List[Tuple[str, torch.nn.Module]]`):
            The list of named modules where we want to determine the maximum layer size.
        module_sizes (`Dict[str, int]`):
            A dictionary mapping each layer name to its size (as generated by `compute_module_sizes`).
        no_split_module_classes (`List[str]`):
            A list of class names for layers we don't want to be split.

    Returns:
        `Tuple[int, List[str]]`: The maximum size of a layer with the list of layer names realizing that maximum size.
    """
    max_size = 0
    layer_names = []
    modules_to_treat = modules.copy()
    while len(modules_to_treat) > 0:
        module_name, module = modules_to_treat.pop(0)
        modules_children = list(module.named_children()) if isinstance(module, torch.nn.Module) else []
        if len(modules_children) == 0 or module.__class__.__name__ in no_split_module_classes:
            # No splitting this one so we compare to the max_size
            size = module_sizes[module_name]
            if size > max_size:
                max_size = size
                layer_names = [module_name]
            elif size == max_size:
                layer_names.append(module_name)
        else:
            modules_to_treat = [(f"{module_name}.{n}", v) for n, v in modules_children] + modules_to_treat
    return max_size, layer_names


FLOAT32 = "float32"
FLOAT16 = "float16"
BFLOAT16 = "bfloat16"
INT8 = "int8"
INT4 = "int4"


class ModelUtils:

    def __init__(self):
        self.svc_ip = os.getenv("svc_ip")
        self.model_id = os.getenv("model_id")
        self.dataset_id = os.getenv("dataset_id")
        self.user_id = os.getenv("user_id")
        self.modelApi = os.getenv("modelApi")
        self.ip = os.getenv("ip")
        # self.gitAddr = os.getenv("git_addr")
        self.memory = os.getenv("memory")
        self.model_file = os.getenv("model_file")
        self.algorithm_id = os.getenv("algorithm_id")
        self.batch = os.getenv("batch")
        self.mutilType = os.getenv("mutil_ype")
        self.name = os.getenv("name")
        self.version = os.getenv("model_version")

    # 发送准确率
    def send_acc(self, acc):
        data = {'modelId': self.model_id, "acc": acc}
        data = urllib.parse.urlencode(data).encode('utf-8')
        address = f"http://{self.svc_ip}:8080/train/addAcc"
        req = urllib.request.Request(url=address, data=data, method='POST')
        response = urllib.request.urlopen(req)
        # 根据需要，你可以添加处理响应或错误的代码。

    # 发送验证准确率
    def sent_validation_acc(self, acc):

        data = {'modelId': self.model_id, "validationAccuracy": acc}
        data = urllib.parse.urlencode(data).encode('utf-8')
        address = "http://" + self.svc_ip + ":8080/model/addValidationAcc"
        req = urllib.request.Request(url=address, data=data, method='POST')
        response = urllib.request.urlopen(req)
        print('Accuracy:', acc, '%')

    # 获得数据集地址
    def get_dataset_path(self):
        return f"/dataset/"

    def get_model_file_path(self):
        return f"/model_file/"

    # 获得验证时需要的api地址
    def get_validation_url(self):
        return self.modelApi

    def get_model_output_path(self):
        # return f"/result/{self.model_id}/{self.version}"
        return f"/result/"

    # 保存模型结果
    def save_result(self, *source_paths):
        destination_root = '/result'  # 根目录
        zip_filename = f"/download/{self.model_id}/results.zip"

        # 确保/download/model_id目录存在
        model_id_path = os.path.join('/download', self.model_id)
        if not os.path.exists(model_id_path):
            os.makedirs(model_id_path)

        # 创建一个新的zip文件
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for source_path in source_paths:
                # 计算目标路径
                destination_path = os.path.join(destination_root, os.path.basename(source_path))

                if os.path.isfile(source_path):
                    # 如果是文件，将其复制到目标目录
                    shutil.copy2(source_path, destination_path)
                    # 将文件加入到zip包中
                    zipf.write(destination_path, os.path.basename(source_path))
                elif os.path.isdir(source_path):
                    # 如果是目录，递归复制整个目录
                    for foldername, subfolders, filenames in os.walk(source_path):
                        # 计算在zip文件中的相对路径
                        # relative_path_in_zip = os.path.relpath(foldername, os.path.dirname(source_path))
                        # 添加目录到zip文件中（创建空目录）
                        zipf.write(foldername, os.path.join(os.path.basename(source_path)))
                        for filename in filenames:
                            file_path = os.path.join(foldername, filename)
                            # 计算目标文件路径
                            destination_file_path = os.path.join(destination_root, os.path.basename(source_path),
                                                                 filename)
                            os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
                            shutil.copy2(file_path, destination_file_path)
                            # 将文件加入到zip包中
                            zipf.write(destination_file_path,
                                       os.path.join(os.path.basename(source_path), filename))

    def get_ips(self):
        data = {'modelId': self.model_id}
        data = urllib.parse.urlencode(data).encode('utf-8')
        address = f"http://{self.svc_ip}:8080/train/getJobIPs"
        req = urllib.request.Request(url=address, data=data, method='POST')
        try:
            with urllib.request.urlopen(req) as response:
                response_data = response.read()
                response_json = json.loads(response_data)

                # 检查返回的状态码是否为 200
                if response_json.get("code") == 200:
                    print(response_json.get("data"))
                    return response_json.get("data")
                else:
                    raise ValueError("Received non-200 response code")
        except Exception as e:
            print(f"Error occurred: {e}")
            return None

    def get_name(self):
        return self.ip

    def model_memory_usage(self, model, batch_size, dtype=FLOAT32):
        if self.memory is not None:
            if self.batch is not None:
                print(f"batch is {self.batch}")
                batch_size = batch_size // int(self.batch)
                return batch_size
            else:
                print(f"memory is {self.memory}")
                return batch_size

        total_size, largest_layer = calculate_maximum_sizes(model)
        DTYPE_MODIFIER = {FLOAT32: 1, FLOAT16: 2, BFLOAT16: 2, INT8: 4, INT4: 8}

        dtype_total_size = total_size
        dtype_largest_layer = largest_layer[0]

        modifier = DTYPE_MODIFIER[dtype]
        dtype_total_size /= modifier
        dtype_largest_layer /= modifier

        # batch_size = 16

        # print(dtype_total_size)
        # dtype_training_size = convert_bytes()
        dtype_training_size = round(((dtype_total_size * 4 * batch_size) / (1024 ** 3)), 2)
        dtype_publish_size = round(((dtype_total_size * 4) / (1024 ** 3)), 2)
        print(dtype_publish_size)
        # dtype_total_size = convert_bytes(dtype_total_size)
        # dtype_largest_layer = convert_bytes(dtype_largest_layer)
        # data.append(
        #     {
        #         "dtype": "float32",
        #         "Largest Layer or Residual Group": dtype_largest_layer,
        #         "Total Size": dtype_total_size,
        #         "Training using Adam": dtype_training_size,
        #     }
        # )
        #
        # print(data)
        data = {'modelId': self.model_id, "memory": dtype_training_size, "publishMemory": dtype_publish_size}
        data = urllib.parse.urlencode(data).encode('utf-8')
        address = f"http://{self.svc_ip}:8080/train/memory"
        req = urllib.request.Request(url=address, data=data, method='POST')
        response = urllib.request.urlopen(req)
        print(response)
        return batch_size
