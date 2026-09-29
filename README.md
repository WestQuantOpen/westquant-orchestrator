# westquant-orchestrator

Cross-framework orchestration and dataset normalization for WestQuant Open.

Responsibilities:

- normalize Qiskit legacy sequential records and new plugin records to
  `wqt-policy-v0.1`;
- preserve successes, failures, invalid verification, unknown verification and
  beam-pruned actions;
- deduplicate merged traces by stable action identity;
- aggregate framework/stage/action/outcome statistics;
- run resumable framework jobs without losing runner errors.

## Merge traces

```bash
westquant-merge-traces \
  qiskit-results/ pytket-results/ pennylane-results/ pulser-results/ \
  --output results/cross-framework
```

## CUDA-Q passports

`normalize_execution_passport` converts a `westquant-cudaq` execution passport
into the canonical `wqt-policy-v0.1` record format, preserving backend,
environment, runtime, memory, quality, QPU-job, and shot information.
