# 🚦 SafeStreets — Real-time Safety Intelligence (Prototype)

**Problem**  
Urban safety in India is underserved in tech. Google Maps can tell you traffic, but it can’t yet tell you if a route is *safe*.  
SafeStreets aims to bridge this gap — using open-source data and AI to provide **contextual safety scores**, interactive maps, and smarter routing.

---

## 🌟 Current Prototype (v0)

### Features
- ✅ Road-level safety scoring (mock formula using OSM features: speed, lighting, sidewalks)  
- ✅ Interactive heatmap (🟢 Safe / 🟠 Medium / 🔴 Risky)  
- ✅ Filters for score range + road type  
- ✅ Clean legend with score categories  
- ✅ Built with **Streamlit + Folium**  

<p align="center">
  <img src="docs/assets/prototype_map.png" width="600">
</p>

---

## 📊 Tech Stack
- **Backend/Data:** Python, Pandas, OSMnx  
- **Frontend:** Streamlit, Folium  
- **Visualization:** Heatmaps, interactive popups  
- **Planned:** scikit-learn for ML-based risk prediction, crowdsourced data integration  

---

## 📂 Repository Structure
SafeStreets/
├── app/ # Streamlit app
│ └── streamlit_app.py
├── data/
│ ├── raw/ # Raw OSM data
│ └── processed/ # Processed CSVs
├── notebooks/ # EDA + mock scoring
├── scripts/ # Data fetch + processing scripts
├── docs/assets/ # Screenshots & mockups
└── README.md

---

## 🚀 Roadmap
- [x] Initialize repo + OSM ingestion  
- [x] Prototype safety scoring + heatmap  
- [x] Build Streamlit app with filters + legend  
- [ ] Replace mock scoring with **real-world datasets** (crime reports, lighting, accidents)  
- [ ] Train ML model to predict safety scores dynamically  
- [ ] Add route recommendations ("safer alternative path")  
- [ ] Expand to multiple Indian metros  

---

## ⚖️ License
[MIT](LICENSE)  
Open to contributions and collaborations.
