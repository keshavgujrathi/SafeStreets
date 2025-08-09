# SafeStreets – Tech Stack & Architecture

## 1. Tech Stack (Phase 1 MVP)

| Layer               | Tech / Tool                           | Purpose |
|---------------------|---------------------------------------|---------|
| Data Ingestion      | Python, Requests, Pandas              | Fetch and process data from APIs/CSV |
| Data Sources        | HERE Traffic API, NCRB CSV, data.gov.in | Safety & incident data |
| Backend Processing  | Flask or FastAPI                      | API endpoints to serve processed data |
| Frontend            | Streamlit / React + Mapbox/Folium     | Map visualization & user interface |
| Database (optional) | PostgreSQL or SQLite                  | Store processed/clean data |
| Deployment          | Render / Railway / Heroku             | Hosting MVP backend & frontend |
| Version Control     | Git, GitHub                           | Repo & collaboration |
| Documentation       | Markdown, GitHub Wiki                 | Project docs & guides |

---

## 2. Architecture Overview

**Data Flow:**
1. **Data Collection Layer**  
   - Fetch data from HERE API, NCRB, data.gov.in.  
   - Store in temporary database or in-memory Pandas DataFrames.

2. **Processing Layer**  
   - Clean and normalize data.  
   - Assign Safety Score = function(crime rate, traffic incident frequency, time of day).  
   - Generate GeoJSON for map rendering.

3. **Backend Layer**  
   - Expose `/safety-score` and `/safe-route` endpoints.  
   - Handle queries like:  
     `GET /safe-route?from=A&to=B`

4. **Frontend Layer**  
   - Render safety heatmaps.  
   - Display safest route options.  
   - Basic form for user incident reporting.

5. **Storage Layer** (Optional for MVP)  
   - Save processed data for re-use to avoid repeated API calls.

---

## 3. Phase-wise Roadmap

**Phase 1 (4-6 weeks)** – MVP  
- Static map with risk zones for 1 pilot city.  
- Basic safe route suggestion using HERE API.

**Phase 2 (6-10 weeks)** – User Reports + Multi-City  
- Add crowdsourced reporting form.  
- Expand to 3 cities.  

**Phase 3 (10+ weeks)** – AI Predictions  
- Use historical + real-time data to predict near-future risk zones.  
- Push notifications for registered users.

---

## 4. Diagram

![Architecture Diagram](docs/assets/architecture_diagram.png)

(Will be added once finalized.)