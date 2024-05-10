from supervisor_detect.utils.missing_optional_dependency import import_optional

load_kernel_config_ke = import_optional(
        'supervisor_detect.saving._keops.loading',
        names=['load_kernel_config'])

__all__ = [
    "load_kernel_config_ke",
]
