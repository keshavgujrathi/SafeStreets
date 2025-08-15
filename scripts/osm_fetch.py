import requests, json, os, datetime

BBOX_BENGALURU = (12.95, 77.55, 12.99, 77.65)  # small central bbox to keep files <20MB

def overpass_query(bbox):
    s,w,n,e = bbox
    return f"""
    [out:json][timeout:60];
    (
      way["highway"]({s},{w},{n},{e});
      node["highway"="traffic_signals"]({s},{w},{n},{e});
      node["highway"="crossing"]({s},{w},{n},{e});
      way["highway"]["lit"]({s},{w},{n},{e});
      way["highway"]["sidewalk"]({s},{w},{n},{e});
      way["maxspeed"]({s},{w},{n},{e});
    );
    out body;
    >;
    out skel qt;
    """

def fetch_and_save(bbox=BBOX_BENGALURU, city="bengaluru"):
    os.makedirs("data/raw", exist_ok=True)
    q = overpass_query(bbox)
    r = requests.get("https://overpass-api.de/api/interpreter", params={"data": q}, timeout=90)
    r.raise_for_status()
    data = r.json()
    stamp = datetime.datetime.utcnow().strftime("%Y%m%d")
    path = f"data/raw/osm_{city}_{stamp}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print("✅ saved:", path)

if __name__ == "__main__":
    fetch_and_save()
