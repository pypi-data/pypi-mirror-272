from supervisor_detect.utils.missing_optional_dependency import import_optional

UAE, HiddenOutput, preprocess_drift = import_optional(
    'supervisor_detect.cd.pytorch.preprocess',
    names=['UAE', 'HiddenOutput', 'preprocess_drift'])

__all__ = [
    "UAE",
    "HiddenOutput",
    "preprocess_drift"
]
