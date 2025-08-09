import os
import requests
import json

# Overpass API endpoint
OVERPASS_URL = "http://overpass-api.de/api/interpreter"

# Query: get roads & traffic-related nodes in Bangalore bounding box
# Bounding box format: (south, west, north, east)
bbox = "12.8341,77.4601,13.1390,77.7306"

query = f"""
[out:json];
(
  node["highway"]( {bbox} );
  way["highway"]( {bbox} );
  relation["highway"]( {bbox} );
);
out body;
>;
out skel qt;
"""

print("Fetching OSM traffic data...")
response = requests.post(OVERPASS_URL, data={"data": query})

if response.status_code == 200:
    data = response.json()
    os.makedirs("data", exist_ok=True)
    with open("data/osm_bangalore_roads.json", "w") as f:
        json.dump(data, f, indent=2)
    print("✅ Data saved to data/osm_bangalore_roads.json")
else:
    print(f"❌ Error {response.status_code}: {response.text}")