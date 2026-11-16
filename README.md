# kit-carriers

The semantic carriers for the mlopt game — online-softmax monoids
(`om`/`om_lower`), the deferred omd carrier (`xcarrier`/`omd_lower`),
affine scans (`scan_lower`), decayed carriers (`decayed_lower`),
trace/traced-monoidal extensions (`trace`/`trace_lift`), and the
carrier law families (`decode_laws`, `decode_geom`, `om_fused`,
`scan_fused`, `machinery`).  Split out of `handl-lang/graphopt`
(`packages/mlopt-carriers`) in P3 Step D-1b and renamed
`mlopt-carriers` → `kit-carriers` / `mlopt_carriers` → `kit_carriers`.

`kit_carriers` registers its machinery with the neutral orchestrator
(`mlopt_orchestrator.carriers.register_carriers`) at import and owns
the `CARRIERS` rule-set composition (`OM_RULES`, `TRACE_RULES`,
`XC_RULES`, `DECODE_RULES`, `DECODE_GEOM_RULES`).

It is **not** a leaf: it sits in the mutually-dependent backend
layer with `kit-torch` (the carrier law modules carry
`TORCH_BINDINGS`; the torch sink builds its executor table from the
carrier lowerings under a lazy import).  Substrate deps resolve
from `handl-lang/eqsat` (`mlopt-core`, `mlopt-orchestrator`,
`mlopt-dtypes`); `kit-torch` resolves from `handl-lang/graphopt`.

## Install

```sh
uv sync --group dev
```

or as a git dependency:

```toml
kit-carriers = { git = "https://github.com/handl-lang/kit-carriers.git", tag = "v0.1.0" }
```

## Verify

```sh
.venv/bin/python -m pytest tests/ -q
.venv/bin/ruff check src tests
.venv/bin/ty check
```
