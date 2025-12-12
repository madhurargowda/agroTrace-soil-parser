#!/usr/bin/env python3
import csv, json, os, sys
from statistics import mean

INPUT_CSV = "samples.csv"
OUT_DIR = "output"

def parse_row(row):
    sid = row["id"]
    ph = float(row["ph"])
    n = float(row["nitrogen"])
    p = float(row["phosphorus"])
    k = float(row["potassium"])
    moisture = float(row.get("moisture", 0.0))
    fert_score = (n + p + k) / 3.0
    ph_status = "acidic" if ph < 6.5 else ("alkaline" if ph > 7.5 else "neutral")
    return {
        "id": sid,
        "ph": ph,
        "ph_status": ph_status,
        "nitrogen": n,
        "phosphorus": p,
        "potassium": k,
        "moisture": moisture,
        "fertility_index": round(fert_score, 2)
    }

def main():
    if not os.path.exists(INPUT_CSV):
        print(f"Input CSV '{INPUT_CSV}' not found.", file=sys.stderr)
        sys.exit(2)

    os.makedirs(OUT_DIR, exist_ok=True)
    samples = []
    with open(INPUT_CSV, newline='') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            parsed = parse_row(row)
            samples.append(parsed)
            out_path = os.path.join(OUT_DIR, f"{parsed['id']}.json")
            with open(out_path, "w") as o:
                json.dump(parsed, o, indent=2)
            print(f"Wrote {out_path}")
    summary = {
        "count": len(samples),
        "avg_fertility": round(mean(s["fertility_index"] for s in samples),2) if samples else 0,
        "samples": [s["id"] for s in samples]
    }

    summary_path = os.path.join(OUT_DIR, "summary.json")
    with open(summary_path, "w") as o:
        json.dump(summary, o, indent=2)
    print("Wrote output/summary.json")
    return 0

if __name__ == "__main__":
    sys.exit(main())
