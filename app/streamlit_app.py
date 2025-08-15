import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap, MarkerCluster

# =========================
# Load processed CSV
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/bengaluru_segments.csv")

df = load_data()

st.set_page_config(page_title="SafeStreets — Safety Map", layout="wide")

# =========================
# Title + description
# =========================
st.title("🚦 SafeStreets — Bengaluru Safety Prototype")
st.markdown("""
**Interactive map** combining heatmap + smart marker clustering.  
Explore road safety scores across Bengaluru with filters.
""")

# =========================
# Sidebar controls
# =========================
st.sidebar.header("⚙️ Filters")

score_range = st.sidebar.slider("Safety Score Range", 0, 100, (0, 100))
road_types = st.sidebar.multiselect(
    "Road Types",
    options=df["highway"].dropna().unique(),
    default=list(df["highway"].dropna().unique())
)

filtered = df[
    (df["safety_score"] >= score_range[0]) &
    (df["safety_score"] <= score_range[1]) &
    (df["highway"].isin(road_types))
]

st.sidebar.markdown(f"**Showing {len(filtered)} road segments**")

# =========================
# Map
# =========================
m = folium.Map(location=[12.9716, 77.5946], zoom_start=12, tiles="cartodbpositron")

if {"lat", "lon"}.issubset(filtered.columns):
    # Heatmap layer (always visible)
    heat_data = filtered[["lat", "lon", "safety_score"]].dropna().values.tolist()
    HeatMap(
        heat_data,
        radius=10,
        blur=20,
        max_zoom=12,
        min_opacity=0.4
    ).add_to(m)

    # Only add markers if dataset is manageable
    if len(filtered) < 2000:
        marker_cluster = MarkerCluster().add_to(m)
        for _, row in filtered.iterrows():
            color = "green" if row["safety_score"] > 70 else "orange" if row["safety_score"] > 40 else "red"
            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=3,
                color=color,
                fill=True,
                fill_opacity=0.6,
                popup=folium.Popup(
                    f"""
                    <b>Road ID:</b> {row['id']}<br>
                    <b>Type:</b> {row['highway']}<br>
                    <b>Score:</b> {row['safety_score']}
                    """,
                    max_width=250
                )
            ).add_to(marker_cluster)
    else:
        st.sidebar.info("ℹ️ Too many points — showing only heatmap for performance.")

    # Add custom legend
        # Add custom legend (with circle markers)
    legend_html = """
    <div style="
     position: fixed; 
     bottom: 50px; left: 50px; 
     width: 200px; 
     border:2px solid #444; 
     border-radius: 8px;
     z-index:9999; 
     font-size:14px; 
     background-color:white; 
     padding:10px 12px; 
     font-family: Arial, sans-serif; 
     color:#333;
     box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
    ">
    <b>Safety Score</b><br><br>
    <div style="display:flex; align-items:center; margin-bottom:6px;">
     <span style="background:green; width:12px; height:12px; 
       border-radius:50%; display:inline-block; margin-right:8px;"></span>
     Safe (70-100)
    </div>
    <div style="display:flex; align-items:center; margin-bottom:6px;">
     <span style="background:orange; width:12px; height:12px; 
       border-radius:50%; display:inline-block; margin-right:8px;"></span>
     Medium (40-70)
    </div>
    <div style="display:flex; align-items:center;">
     <span style="background:red; width:12px; height:12px; 
       border-radius:50%; display:inline-block; margin-right:8px;"></span>
     Risky (0-40)
    </div>
    </div>
"""

    m.get_root().html.add_child(folium.Element(legend_html))

    st_folium(m, width=950, height=650)

else:
    st.warning("⚠️ No coordinates found in CSV — showing only table preview.")
    st.dataframe(filtered.head())

# =========================
# Developer-only Preview
# =========================
with st.expander("🛠 Developer Data Preview (CSV sample)"):
    st.dataframe(filtered.head(20))
