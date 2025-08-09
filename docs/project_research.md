# SafeStreets – Data Source Research

## Objective
Identify reliable, India-specific data sources for crime reports, traffic incidents, and public safety, ensuring API availability and integration feasibility.

---

## Potential Data Sources

| Data Type               | Source / API Name                     | Link / Documentation                                                                                   | Data Coverage & Frequency                                           | Access Requirements                | Verification Status |
|-------------------------|----------------------------------------|--------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|--------------------------------------|---------------------|
| Crime Reports           | NCRB Open Data                         | https://ncrb.gov.in/en/crime-in-india                                                                   | Annual state/district crime statistics; not real-time               | Public PDFs; scraping needed         | ✅ Verified         |
| Crime Mapping           | Open Government Data (data.gov.in)     | https://data.gov.in                                                                                     | Various datasets (some city-specific), CSV/JSON format              | Free API with registration           | ✅ Verified         |
| Police Incident Feeds   | State Police APIs (if available)       | Varies per state (e.g., Delhi Police crime mapping)                                                     | Real-time or periodic updates (state-dependent)                     | API key or scraping                   | 🚧 Needs per-state check |
| Traffic Incidents       | Google Maps / Routes API               | **[Broken link – needs verification]**                                                                 | Historical traffic models, live congestion (no public incident feed) | API key, quota-based pricing          | ❗ To be rechecked |
| Traffic Incidents       | HERE Location Services                 | https://developer.here.com/documentation/traffic/dev_guide/topics/what-is.html                         | Real-time incident & congestion data                                | API key, free tier + paid plans       | ✅ Verified         |
| User Reports            | Custom crowdsourcing module (SafeStreets app) | N/A                                                                                                    | Real-time via user submissions                                      | Built-in feature in MVP               | N/A                 |
| Weather & Lighting Data | OpenWeatherMap API                     | https://openweathermap.org/api                                                                          | Real-time + forecast; relevant for safety context                   | Free tier available                   | ✅ Verified         |

---

## Notes for Future Checks
- **Google Traffic API**: Link currently not loading — revisit after confirming product status in Google Maps Platform documentation.
- **State Police Feeds**: Need to contact/state-by-state research for possible real-time APIs.
- **NCRB**: Annual updates mean lag in real-time data — use for historical risk modeling only.

---

## Next Step
Prioritize **HERE Location Services** + **Open Government Data** for Phase 1 MVP due to reliability, structured format, and API accessibility. Crowdsourcing module can be integrated in Phase 2 for scalability.