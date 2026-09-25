from __future__ import annotations
from collections import Counter, defaultdict
from statistics import median
from typing import Any, Iterable


def _num(values):
    xs=[float(x) for x in values if isinstance(x,(int,float))]
    if not xs: return {"n":0,"mean":None,"median":None,"min":None,"max":None}
    return {"n":len(xs),"mean":sum(xs)/len(xs),"median":median(xs),"min":min(xs),"max":max(xs)}


def aggregate(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows=list(records)
    by_framework=Counter(r["framework"] for r in rows)
    by_outcome=Counter(r.get("outcome_class","unknown") for r in rows)
    by_stage=Counter(r.get("stage") for r in rows)
    kept=sum(bool(r.get("kept_in_beam")) for r in rows)
    terminal=sum(bool(r.get("terminal")) for r in rows)
    metric_values=defaultdict(list)
    for r in rows:
        for k,v in (r.get("metrics_after") or {}).items():
            if isinstance(v,(int,float)): metric_values[k].append(v)
    return {
        "n_records":len(rows),
        "by_framework":dict(sorted(by_framework.items())),
        "by_outcome":dict(sorted(by_outcome.items())),
        "by_stage":dict(sorted(by_stage.items(), key=lambda kv: str(kv[0]))),
        "kept_in_beam":kept,
        "terminal":terminal,
        "metrics":{k:_num(v) for k,v in sorted(metric_values.items())},
    }


def stage_action_table(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    buckets=defaultdict(list)
    for r in records:
        action=r.get("action") or {}
        name=action.get("name", str(action))
        buckets[(r.get("framework"),r.get("stage"),name)].append(r)
    out=[]
    for key, rows in sorted(buckets.items()):
        outcomes=Counter(r.get("outcome_class","unknown") for r in rows)
        out.append({
            "framework":key[0],"stage":key[1],"action":key[2],"attempts":len(rows),
            "kept":sum(bool(r.get("kept_in_beam")) for r in rows),
            **{f"outcome_{k}":v for k,v in sorted(outcomes.items())},
        })
    return out
