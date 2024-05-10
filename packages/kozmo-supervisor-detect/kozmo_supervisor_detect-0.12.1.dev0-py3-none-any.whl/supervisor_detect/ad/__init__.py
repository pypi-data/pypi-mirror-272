from supervisor_detect.utils.missing_optional_dependency import import_optional

AdversarialAE = import_optional('supervisor_detect.ad.adversarialae', names=['AdversarialAE'])
ModelDistillation = import_optional('supervisor_detect.ad.model_distillation', names=['ModelDistillation'])

__all__ = [
    "AdversarialAE",
    "ModelDistillation"
]
