import argparse
import re
from pathlib import Path

import pandas as pd
import yaml


def parse_speed(raw):
    """Robust parser: '50', '50 km/h', '30mph', None -> int or None"""
    if pd.isna(raw):
        return None
    s = str(raw).lower().strip()
    m = re.search(r"(\d+)", s)
    if not m:
        return None
    val = int(m.group(1))
    # crude mph -> km/h if explicitly says mph
    if "mph" in s:
        val = int(round(val * 1.60934))
    return val


def compute_row_score(row, cfg):
    w = cfg["weights"]
    caps = cfg["caps"]
    highway_risk = cfg.get("highway_risk", {})

    score = w["base"]

    # highway risk
    hw = str(row.get("highway", "")).lower()
    score += highway_risk.get(hw, 0)

    # speed factor
    spd = parse_speed(row.get("maxspeed"))
    if spd is not None:
        if spd <= 30:
            score += w["speed_low_bonus"]
        elif spd <= 50:
            score += w["speed_mid_bonus"]
        else:
            score += w["speed_high_penalty"]

    # lighting
    lit = str(row.get("lit", "")).lower()
    if lit == "yes":
        score += w["lit_yes_bonus"]
    elif lit == "no":
        score += w["lit_no_penalty"]

    # sidewalks
    sidewalk = str(row.get("sidewalk", "")).lower()
    if sidewalk in {"both", "left", "right"}:
        score += w["sidewalk_bonus"]
    elif sidewalk == "no":
        score += w["sidewalk_no_penalty"]

    # geometry complexity proxy
    n_nodes = row.get("n_nodes")
    try:
        n_nodes = int(n_nodes)
        if n_nodes <= 5:
            score += w["nodes_short_bonus"]
        elif n_nodes >= 50:
            score += w["nodes_long_penalty"]
    except Exception:
        pass

    # clip
    score = max(caps["min"], min(caps["max"], score))
    return int(score)


def score_dataframe(df, cfg):
    # ensure required cols exist
    for col in ["id", "highway", "maxspeed", "lit", "sidewalk", "n_nodes"]:
        if col not in df.columns:
            df[col] = None
    df["safety_score"] = df.apply(lambda r: compute_row_score(r, cfg), axis=1)
    return df


def main():
    ap = argparse.ArgumentParser(description="Compute safety scores from processed segments")
    ap.add_argument("--in", dest="inp", default="data/processed/bengaluru_segments.csv")
    ap.add_argument("--out", dest="out", default="data/processed/bengaluru_segments.csv")
    ap.add_argument("--config", dest="config", default="config/config.yaml")
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    df = pd.read_csv(args.inp)
    df = score_dataframe(df, cfg)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, index=False)
    print(f"✅ wrote {args.out} with safety_score, rows={len(df)}")


if __name__ == "__main__":
    main()
