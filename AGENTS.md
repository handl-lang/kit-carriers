# Agent guide — kit-carriers

The semantic carriers for the mlopt game — online-softmax monoids
(`om`/`om_lower`), the deferred omd carrier (`xcarrier`/`omd_lower`),
affine scans (`scan_lower`/`scan_fused`), decayed carriers
(`decayed_lower`), decode laws/geometry (`decode_laws`/
`decode_geom`), the traced-monoidal extensions (`trace`/
`trace_lift`), and `machinery` (the `register_carriers` payload).
Split from `handl-lang/graphopt` `packages/mlopt-carriers` in P3
Step D-1b (the second package of the graphopt domain-package
dissolution; the `mlopt-*` → `kit-*` rename).  Python 3.13, torch +
`mlopt-core`/`mlopt-orchestrator` on the eqsat substrate.

## Layout

- `src/kit_carriers/` — the one shipped package:
  - `om.py` / `om_lower.py` / `om_fused.py` — the online-softmax
    monoid, its batched lowering, and fused variants;
  - `xcarrier.py` / `omd_lower.py` — the deferred (cross-position)
    carrier and its lowering;
  - `scan_lower.py` / `scan_fused.py` — affine-scan plans and fused
    scan executors;
  - `decayed_lower.py` — the decayed (forgetting-factor) carrier;
  - `trace.py` / `trace_lift.py` — traced-monoidal carriers and the
    lift machinery;
  - `decode_laws.py` / `decode_geom.py` — decode-step law families
    and geometry rules;
  - `machinery.py` — `build_machinery()` (the value
    `mlopt_orchestrator.carriers.register_carriers` seats);
  - `CARRIERS` — the composed `RuleSet` (`OM_RULES` + `TRACE_RULES`
    + `XC_RULES` + `DECODE_RULES` + `DECODE_GEOM_RULES`), resolved
    lazily per name (the law modules import torch).
- `tests/` — the package-bound suite (the carrier/lowering/trace/
  decode-geometry files carved out of graphopt's `tests/` — every
  file whose imports stay inside this package's dep closure:
  `kit_carriers` + `mlopt_core`/`mlopt_torch`/
  `mlopt_orchestrator`/`mlopt_dtypes` + torch).  Cross-stack
  integration tests (anything touching `mlopt_discovery`,
  `mlopt_cuda`, `mlopt_host_tensor`, `kit_onnx`, gamekit, benchkit)
  stayed in graphopt and import `kit_carriers` as a git dep.

## Contracts

- **Mutually-dependent backend layer** — not a leaf: the carrier law
  modules carry `TORCH_BINDINGS` and import `mlopt_torch`
  (`torch_bridge`, `executors`); `mlopt_torch.adapters` resolves the
  carrier lowerings lazily under `ModuleNotFoundError` (the torch
  sink degrades to trace + generic without them).  The declared
  dependency runs one way (carriers → torch); the reverse edge stays
  undeclared and lazy — do not add a `mlopt-torch → kit-carriers`
  dep (a declared cycle is not installable).
- Substrate deps: `mlopt-core`, `mlopt-orchestrator`,
  `mlopt-dtypes` (handl-lang/eqsat, `packages/` subdirs,
  tag-pinned); `mlopt-torch` (handl-lang/graphopt,
  `packages/mlopt-torch` subdir, tag-pinned).
- `import kit_carriers` registers the carrier machinery with the
  orchestrator and must stay torch-safe at package import — the law
  modules resolve lazily through `__getattr__`.
- History was preserved via `git subtree split` of
  `graphopt:packages/mlopt-carriers` — `git log` here reaches back
  through the graphopt history.

## Verification

```sh
uv sync --group dev
.venv/bin/python -m pytest tests/ -q
.venv/bin/ruff check src
.venv/bin/ruff format --check src
.venv/bin/ty check
```

<!-- myco:agent-awareness -->

## Agent awareness

- Session start / any work discussion: run `myco status --prompt`
  before proposing next steps — know the board first.
- User describes new work → offer to capture it (`myco todo add`,
  `issue new`, `proposal new`). Don't wait to be asked.
- Picking up a task: `myco resume <ID>` is the briefing.
- Wrapping up: `myco handoff <ID>` anything resumable; keep statuses
  honest (claimed → in-progress → blocked/done).

<!-- /myco:agent-awareness -->
