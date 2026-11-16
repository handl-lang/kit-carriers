"""kit-carriers — the semantic carriers and their executors.

Online-softmax monoids (:mod:`~kit_carriers.om`,
:mod:`~kit_carriers.om_lower`), the deferred omd carrier
(:mod:`~kit_carriers.xcarrier`,
:mod:`~kit_carriers.omd_lower`), affine scans
(:mod:`~kit_carriers.scan_lower`), and the traced-monoidal
extensions (:mod:`~kit_carriers.trace`,
:mod:`~kit_carriers.trace_lift`).  Each module declares
``TORCH_BINDINGS`` (folded into :meth:`OpTable.full`) and registers
its shape rules on import — OpTable composes them lazily so the
modules themselves stay import-safe.

The carrier law families also own their rule sets:
``kit_carriers.om.OM_RULES`` /
``kit_carriers.trace.TRACE_RULES`` /
``kit_carriers.xcarrier.XC_RULES`` /
``kit_carriers.decode_laws.DECODE_RULES`` /
``kit_carriers.decode_geom.DECODE_GEOM_RULES`` are
:class:`~mlopt_core.laws.RuleSet` values, and ``CARRIERS`` (below)
is their composition — the preset the orchestrator's
``DEFAULT_RULES`` adds on top of the core default.  Every name
materialises **lazily**: the law modules import their backend
(torch), so touching them at package import would couple every
``import kit_carriers`` to torch.
"""

from typing import Any

from mlopt_core.ops import register_carrier
from mlopt_orchestrator.carriers import register_carriers

from kit_carriers.machinery import build_machinery

# Seat the carrier modules on ``OpTable.full()``'s carrier list.  eqsat
# v0.1.9+ names them in ``_CARRIER_MODULES`` already; registering here
# too keeps ``OpTable.full()``/``carrier_torch_bindings()`` correct for
# consumers still pinned to an older eqsat (``importlib`` caches the
# module, so the overlap with the builtins is free).
for _carrier_mod in (
    "kit_carriers.trace",
    "kit_carriers.xcarrier",
    "kit_carriers.om",
):
    register_carrier(_carrier_mod)
del _carrier_mod

# Install the carrier machinery with the neutral orchestrator (the
# edge inversion: carriers -> orchestrator, never the reverse).  The
# value holds only thunks, so this loads no tensor library.
register_carriers(build_machinery())

__all__ = [
    "CARRIERS",
    "DECODE_GEOM_RULES",
    "DECODE_RULES",
    "OM_RULES",
    "TRACE_RULES",
    "XC_RULES",
]


#: Family rule set name -> the module that defines it.  Each module
#: imports its backend (torch), so resolution stays lazy per name.
_FAMILY_MODULES = {
    "DECODE_GEOM_RULES": "kit_carriers.decode_geom",
    "DECODE_RULES": "kit_carriers.decode_laws",
    "OM_RULES": "kit_carriers.om",
    "TRACE_RULES": "kit_carriers.trace",
    "XC_RULES": "kit_carriers.xcarrier",
}


def __getattr__(name: str) -> Any:
    """Compose the carrier rule sets on first access (torch-coupled).

    Resolved per name so ``decode_laws`` stays reachable in a
    torch-free process — only ``CARRIERS`` needs every family.
    """
    if name == "CARRIERS":
        from kit_carriers.decode_geom import DECODE_GEOM_RULES
        from kit_carriers.decode_laws import DECODE_RULES
        from kit_carriers.om import OM_RULES
        from kit_carriers.trace import TRACE_RULES
        from kit_carriers.xcarrier import XC_RULES

        rs = (
            OM_RULES
            + TRACE_RULES
            + XC_RULES
            + DECODE_RULES
            + DECODE_GEOM_RULES
        )
    elif name in _FAMILY_MODULES:
        import importlib

        rs = getattr(
            importlib.import_module(_FAMILY_MODULES[name]), name
        )
    else:
        raise AttributeError(
            f"module {__name__!r} has no attribute {name!r}"
        )
    globals()[name] = rs
    return rs
