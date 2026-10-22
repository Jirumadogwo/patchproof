# Repository conventions

- Keep engine modules directly under `src/patchproof/` and use absolute `patchproof` imports; the editable package must resolve identically locally and in CI.
- Keep every test under `tests/unit/`; benchmark fixtures under `tests/unit/benchmarks/` are explicitly staged by runner tests to check buggy candidates fail and reference solutions pass.
- Preserve deliberately defective starter workspaces; repairing the harness must not solve benchmark tasks.
- Preserve both historical scoring/reporting APIs; downstream users may depend on either generation.
- Run untrusted candidate code only in an external security sandbox; a Python subprocess provides no security boundary.
