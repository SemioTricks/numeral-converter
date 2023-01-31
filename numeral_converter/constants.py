from collections import OrderedDict
from typing import Any, Dict

DEFAULT_MORPH: Dict[str, Any] = OrderedDict(
    [
        ("case", "nominative"),
        ("num_class", "quantitative"),
        ("number", None),
        ("gender", "masculine"),
    ]
)

MORPH_FORMS: Dict[str, Any] = {
    "case": (
        "accusative",
        "dative",
        "genetive",
        "instrumental",
        "nominative",
        "prepositional",
    ),
    "num_class": ("collective", "ordinal", "quantitative"),
    "gender": ("feminine", "masculine", "neuter"),
    "number": ("plural", "singular"),
}
