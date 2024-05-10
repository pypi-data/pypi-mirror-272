from supervisor_detect.utils.missing_optional_dependency import import_optional


save_state_dict, load_state_dict = import_optional(
    'supervisor_detect.utils.state._pytorch.state',
    names=['save_state_dict', 'load_state_dict']
)

__all__ = [
    "save_state_dict",
    "load_state_dict",
]
