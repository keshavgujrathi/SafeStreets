import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap, MarkerCluster, Fullscreen
import io

# =========================
# Load data
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/bengaluru_segments.csv")

df = load_data()

st.set_page_config(page_title="SafeStreets — Bengaluru Safety Prototype", layout="wide")

# =========================
# Title
# =========================
st.title("🚦 SafeStreets — Bengaluru Safety Prototype")
st.markdown("""
A clean, interactive dashboard to explore **road safety scores** across Bengaluru.  
Use the filters in the sidebar to adjust **road type, score range, map style, and visualization layers**.
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
marker_limit = st.sidebar.slider("Max markers to display", 200, 2000, 500, step=100)

# Map options
layer_choice = st.sidebar.radio("Map Layers", ["Heatmap", "Markers", "Both"], index=2)

tile_options = {
    "Carto Light": ("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", 
                    "© OpenStreetMap contributors © Carto"),
    "Carto Dark": ("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", 
                   "© OpenStreetMap contributors © Carto"),
    "OpenStreetMap": ("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", 
                      "© OpenStreetMap contributors"),
}
tile_name = st.sidebar.selectbox("🗺 Map Style", list(tile_options.keys()))
tiles, attr = tile_options[tile_name]

show_legend = st.sidebar.checkbox("Show Legend", value=True)

# Filter dataset
filtered = df[
    (df["safety_score"] >= score_range[0]) &
    (df["safety_score"] <= score_range[1]) &
    (df["highway"].isin(road_types))
]

st.sidebar.markdown(f"**Showing {len(filtered)} road segments**")

# =========================
# Layout: Map + Insights
# =========================
left, right = st.columns([2, 1])

# ----------- MAP ----------
with left:
    m = folium.Map(location=[12.9716, 77.5946], zoom_start=12, tiles=tiles, attr=attr)

    # Fullscreen toggle
    Fullscreen(position="topright").add_to(m)

    if {"lat", "lon"}.issubset(filtered.columns):

        # Heatmap Layer
        if layer_choice in ["Heatmap", "Both"]:
            heat_data = filtered[["lat", "lon", "safety_score"]].dropna().values.tolist()
            HeatMap(
                heat_data,
                radius=10,
                blur=20,
                max_zoom=12,
                min_opacity=0.4
            ).add_to(m)

        # Marker Cluster
        if layer_choice in ["Markers", "Both"]:
            subset = filtered.head(marker_limit)  # limit markers
            marker_cluster = MarkerCluster().add_to(m)
            for _, row in subset.iterrows():
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

        # Legend (toggle-able)
        if show_legend:
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
             color:#222;
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

# ----------- INSIGHTS ----------
with right:
    # Summary stats
    st.subheader("📊 Safety Overview")
    avg_score = filtered["safety_score"].mean()
    safe = (filtered["safety_score"] >= 70).sum()
    medium = ((filtered["safety_score"] < 70) & (filtered["safety_score"] >= 40)).sum()
    risky = (filtered["safety_score"] < 40).sum()

    st.metric("Average Safety Score", f"{avg_score:.1f}")
    st.write(f"✅ Safe: {safe} | ⚠️ Medium: {medium} | 🚨 Risky: {risky}")

    # Leaderboard
    st.subheader("🔥 Top 20 Risky Segments")
    top_risky = filtered.sort_values("safety_score", ascending=True).head(20)

    for i, row in top_risky.iterrows():
        icon = "🚗" if "motorway" in row['highway'] else "🛣" if "primary" in row['highway'] else "🏙"
        color = "red" if row['safety_score'] < 40 else "orange" if row['safety_score'] < 70 else "green"
        st.markdown(f"""
        <div style="padding:8px; border-bottom:1px solid #eee;">
        <b>#{i+1}</b> {icon} {row['highway'].title()}  
        <br><small>Road ID: {row['id']}</small>  
        <span style="color:{color};"><b>Score: {row['safety_score']}</b></span>
        </div>
        """, unsafe_allow_html=True)

    # Downloads
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_segments.csv",
        mime="text/csv",
    )

    # Save leaderboard snapshot (HTML)
    buffer = io.StringIO()
    top_risky.to_html(buf=buffer, index=False)
    st.download_button(
        label="📷 Save Top 20 Risky Segments (HTML Snapshot)",
        data=buffer.getvalue().encode("utf-8"),
        file_name="top_risky_segments.html",
        mime="text/html",
    )
