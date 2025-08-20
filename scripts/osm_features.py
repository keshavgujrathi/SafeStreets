import json
import pandas as pd


def compute_safety(row):
    score = 50  # base score

    # Speed factor
    if row["maxspeed"]:
        try:
            speed = int(str(row["maxspeed"]).split()[0])  # handles "50 mph"
            if speed <= 30:
                score += 20
            elif speed <= 50:
                score += 10
            else:
                score -= 10
        except:
            pass

    # Lighting factor
    if str(row["lit"]).lower() == "yes":
        score += 15
    elif str(row["lit"]).lower() == "no":
        score -= 10

    # Sidewalk factor
    if str(row["sidewalk"]).lower() in ["both", "left", "right"]:
        score += 10
    elif str(row["sidewalk"]).lower() == "no":
        score -= 5

    # Road length complexity
    if row["n_nodes"] <= 5:
        score += 5
    elif row["n_nodes"] >= 50:
        score -= 10

    return max(0, min(100, score))  # clamp 0–100


def extract_features(input_path: str, output_path: str):
    """Extracts road features from raw OSM JSON and computes safety scores."""

    with open(input_path, "r", encoding="utf-8") as f:
        osm_data = json.load(f)

    elements = osm_data["elements"]

    # Extract nodes
    nodes = {el["id"]: (el["lat"], el["lon"]) for el in elements if el["type"] == "node"}

    # Extract roads
    roads = []
    for el in elements:
        if el["type"] == "way" and "highway" in el["tags"]:
            node_ids = el["nodes"]
            coords = [nodes[nid] for nid in node_ids if nid in nodes]
            if coords:
                avg_lat = sum(c[0] for c in coords) / len(coords)
                avg_lon = sum(c[1] for c in coords) / len(coords)

                roads.append({
                    "id": el["id"],
                    "highway": el["tags"].get("highway", "unknown"),
                    "maxspeed": el["tags"].get("maxspeed", None),
                    "lit": el["tags"].get("lit", None),
                    "sidewalk": el["tags"].get("sidewalk", None),
                    "n_nodes": len(node_ids),
                    "lat": avg_lat,
                    "lon": avg_lon,
                })

    df = pd.DataFrame(roads)
    df["safety_score"] = df.apply(compute_safety, axis=1)

    df.to_csv(output_path, index=False)
    print(f"✅ Saved processed CSV: {output_path} ({df.shape})")

    return df


if __name__ == "__main__":
    extract_features("data/raw/osm_bengaluru.json", "data/processed/bengaluru_segments.csv")
