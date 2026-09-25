from __future__ import annotations
import json, time, traceback
from pathlib import Path
from typing import Any, Iterable
from westquant_core import write_jsonl
from .model import FrameworkJob
from .normalize import normalize_record


def run_jobs(jobs: Iterable[FrameworkJob], *, output: str | Path, resume: bool=True) -> list[dict[str, Any]]:
    root=Path(output); root.mkdir(parents=True, exist_ok=True)
    summaries=[]
    for job in jobs:
        d=root/job.framework/job.job_id; d.mkdir(parents=True, exist_ok=True)
        run_path=d/"run.json"
        if resume and run_path.exists():
            try:
                old=json.loads(run_path.read_text())
                if old.get("status")=="completed": summaries.append(old); continue
            except Exception: pass
        start=time.perf_counter()
        try:
            result=job.runner()
            if hasattr(result,"records"):
                records=result.records(framework=job.framework, context=job.metadata)
            elif isinstance(result,list): records=result
            else: raise TypeError("runner must return a search result with records() or a record list")
            rows=[normalize_record(r) for r in records]
            write_jsonl(d/"trajectory.jsonl", rows)
            status={"job_id":job.job_id,"framework":job.framework,"challenge_id":job.challenge_id,"status":"completed","n_records":len(rows),"elapsed_seconds":time.perf_counter()-start,"metadata":job.metadata}
        except Exception as exc:
            status={"job_id":job.job_id,"framework":job.framework,"challenge_id":job.challenge_id,"status":"runner_error","elapsed_seconds":time.perf_counter()-start,"metadata":job.metadata,"error":{"type":type(exc).__name__,"message":str(exc),"traceback":traceback.format_exc()}}
        run_path.write_text(json.dumps(status,indent=2,sort_keys=True),encoding="utf-8")
        summaries.append(status)
    return summaries
