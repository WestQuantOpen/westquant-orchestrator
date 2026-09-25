from __future__ import annotations
import argparse, csv, json
from pathlib import Path
from westquant_core import read_jsonl, write_jsonl
from .normalize import normalize_record, record_identity
from .stats import aggregate, stage_action_table


def main() -> None:
    p=argparse.ArgumentParser(description="Merge and validate WestQuant policy traces across frameworks")
    p.add_argument("inputs", nargs="+", help="trajectory.jsonl files or directories")
    p.add_argument("--output", default="results/westquant-cross-framework")
    args=p.parse_args()
    files=[]
    for raw in args.inputs:
        path=Path(raw)
        if path.is_dir(): files.extend(path.rglob("trajectory.jsonl"))
        else: files.append(path)
    rows=[]; seen=set(); duplicates=0
    for f in files:
        for r in read_jsonl(f):
            n=normalize_record(r); ident=record_identity(n)
            if ident in seen: duplicates+=1; continue
            seen.add(ident); rows.append(n)
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    write_jsonl(out/"all_trajectories.jsonl", rows)
    stats=aggregate(rows); stats["duplicates_removed"]=duplicates; stats["source_files"]=len(files)
    (out/"statistics.json").write_text(json.dumps(stats,indent=2,sort_keys=True),encoding="utf-8")
    table=stage_action_table(rows)
    keys=sorted({k for r in table for k in r})
    with (out/"stage_action_summary.csv").open("w",newline="",encoding="utf-8") as fh:
        w=csv.DictWriter(fh,fieldnames=keys); w.writeheader(); w.writerows(table)
    print(json.dumps(stats,indent=2,sort_keys=True))

if __name__=="__main__": main()
