from __future__ import annotations
from typing import Any

REQUIRED = {
    "framework", "challenge_id", "state_id", "next_state_id", "step_index",
    "stage", "action", "success", "selectable", "verification",
    "metrics_before", "metrics_after", "kept_in_beam", "terminal", "error",
}


def _normalize_action(stage: Any, action: Any) -> dict[str, Any]:
    if isinstance(action, dict):
        out = dict(action)
        out.setdefault("stage", stage)
        out.setdefault("name", str(out.get("id", "unknown")))
        out.setdefault("parameters", {})
        return out
    return {"stage": stage, "name": str(action), "parameters": {}}


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    """Normalize current and legacy WestQuant traces to WQT policy v0.1.

    The Qiskit sequential alpha originally used `compile_success`, a scalar
    `action`, `target_context`, and schema `0.2-sequential`. These aliases are
    intentionally accepted so old QoolQit/Qiskit research runs remain useful.
    """
    out = dict(record)
    out["schema_version"] = "wqt-policy-v0.1"
    if "success" not in out:
        out["success"] = bool(out.get("compile_success", False))
    out.setdefault("selectable", bool(out["success"]))
    if "context" not in out:
        out["context"] = {"target_context": out.get("target_context", {})}
    out["action"] = _normalize_action(out.get("stage"), out.get("action", out.get("action_name")))
    out.setdefault("reward_vector", {})
    out.setdefault("cost", {})
    if "compile_seconds" in out and "compile_seconds" not in out["cost"]:
        out["cost"] = {**out["cost"], "compile_seconds": out.get("compile_seconds")}
    out.setdefault("verification", {})
    out.setdefault("metrics_before", {})
    out.setdefault("metrics_after", {})
    out.setdefault("kept_in_beam", bool(out.get("kept", False)))
    out.setdefault("terminal", False)
    out.setdefault("error", None)

    missing = sorted(REQUIRED - set(out))
    if missing:
        raise ValueError(f"missing policy record fields: {missing}")

    verification = out.get("verification") or {}
    equivalence = str(verification.get("equivalence", "unknown")).lower()
    if not out["success"]:
        outcome = "failed"
    elif equivalence == "invalid":
        outcome = "verification_invalid"
    elif equivalence == "exact" and verification.get("verified"):
        outcome = "verified_exact"
    else:
        outcome = "compiled_unknown"
    out["outcome_class"] = out.get("outcome_class", outcome)
    return out


def record_identity(record: dict[str, Any]) -> tuple[Any, ...]:
    action = record.get("action") or {}
    return (
        record.get("framework"), record.get("challenge_id"), record.get("state_id"),
        record.get("next_state_id"), record.get("step_index"), record.get("stage"),
        action.get("id") or action.get("name") or str(action),
    )
