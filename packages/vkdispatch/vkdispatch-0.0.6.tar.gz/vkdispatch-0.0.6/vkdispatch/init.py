import vkdispatch_native

import typing

device_type_id_to_str_dict = {
    0: "Other",
    1: "Integrated GPU",
    2: "Discrete GPU",
    3: "Virtual GPU",
    4: "CPU",
}

class device_info:
    def __init__(self, dev_index: int, version_variant: int, version_major: int, version_minor: int,
                version_patch: int, driver_version: int, vendor_id: int, device_id: int,
                device_type: int, device_name: str, float_64_support: int, int_64_support: int,
                int_16_support: int, max_workgroup_size: typing.Tuple[int, int, int], max_workgroup_invocations: int,
                max_workgroup_count: typing.Tuple[int, int, int], max_bound_descriptor_sets: int,
                max_push_constant_size: int, max_storage_buffer_range: int, max_uniform_buffer_range: int,
                sub_group_size: int, supported_stages: int, supported_operations: int, 
                quad_operations_in_all_stages: int, max_compute_shared_memory_size: int):
        self.dev_index = dev_index

        self.version_variant = version_variant
        self.version_major = version_major
        self.version_minor = version_minor
        self.version_patch = version_patch

        self.driver_version = driver_version
        self.vendor_id = vendor_id
        self.device_id = device_id

        self.device_type = device_type

        self.device_name = device_name

        self.float_64_support = float_64_support
        self.int_64_support = int_64_support
        self.int_16_support = int_16_support

        self.max_workgroup_size = max_workgroup_size
        self.max_workgroup_invocations = max_workgroup_invocations
        self.max_workgroup_count = max_workgroup_count

        self.max_bound_descriptor_sets = max_bound_descriptor_sets
        self.max_push_constant_size = max_push_constant_size
        self.max_storage_buffer_range = max_storage_buffer_range
        self.max_uniform_buffer_range = max_uniform_buffer_range

        self.sub_group_size = sub_group_size
        self.supported_stages = supported_stages
        self.supported_operations = supported_operations
        self.quad_operations_in_all_stages = quad_operations_in_all_stages

        self.max_compute_shared_memory_size = max_compute_shared_memory_size
    
    def __repr__(self) -> str:
        result = f"Device {self.dev_index}: {self.device_name}\n"

        result += f"\tVulkan Version: {self.version_major}.{self.version_minor}.{self.version_patch}\n"
        result += f"\tDevice Type: {device_type_id_to_str_dict[self.device_type]}\n"
        
        if(self.version_variant != 0):
            result += f"\tVariant: {self.version_variant}\n"
        
        #result += f"\tDriver Version={self.driver_version}\n"
        #result += f"\tVendor ID={self.vendor_id}\n"
        #result += f"\tDevice ID={self.device_id}\n"

        result += f"\t64-bit Float Support: {self.float_64_support == 1}\n"
        result += f"\t64-bit Int Support: {self.int_64_support == 1}\n"
        result += f"\t16-bit Int Suppor: {self.int_16_support == 1}\n"
        result += f"\tMax Workgroup Sizes: {self.max_workgroup_size}\n"
        result += f"\tMax Workgroup Invocations: {self.max_workgroup_invocations}\n"
        result += f"\tMax Workgroup Counts: {self.max_workgroup_count}\n"
        #result += f"\tMax Bound Descriptor Sets={self.max_bound_descriptor_sets}\n"
        result += f"\tMax Push Constant Size: {self.max_push_constant_size}\n"
        result += f"\tMax Storage Buffer Range: {self.max_storage_buffer_range}\n"
        result += f"\tMax Uniform Buffer Range: {self.max_uniform_buffer_range}\n"

        result += f"\tSubgroup Size: {self.sub_group_size}\n"
        result += f"\tSupported Stages: {hex(self.supported_stages)}\n"
        result += f"\tSupported Operations: {hex(self.supported_operations)}\n"
        result += f"\tQuad Operations in All Stages: {self.quad_operations_in_all_stages}\n"

        result += f"\tMax Compute Shared Memory Size: {self.max_compute_shared_memory_size}\n"

        return result

__initilized_instance: bool = False

def init_instance(debug_mode: bool = False):
    global __initilized_instance

    if __initilized_instance:
        return

    vkdispatch_native.init(debug_mode)
    __initilized_instance = True

def get_devices(debug_mode: bool = False) -> typing.List[device_info]:
    init_instance(debug_mode)

    return [device_info(ii, *dev_obj) for ii, dev_obj in enumerate(vkdispatch_native.get_devices())]