# SafeStreets – Problem & Scope Definition

## Problem Statement
Describe the exact safety and routing challenges faced by **urban commuters in India**.
Example:  
"Travelers often unknowingly pass through high-risk areas due to the absence of integrated real-time safety and route guidance systems in India."

---

## Target Users
- Daily commuters (car, bike, public transport)
- Tourists unfamiliar with city routes
- Delivery partners (Swiggy, Zomato, Dunzo, Amazon)
- Parents monitoring safe travel for family members

---

## Core Pain Points
- No unified source combining **crime, traffic incidents, and user safety reports**.
- Static crime data → not enough for real-time decisions.
- Existing maps (Google, Apple) do not prioritize **safety-first routing**.
- Crowdsourced apps like Waze exist but have **low penetration in India** for crime-related safety.

---

## MVP Scope (Phase 1 – 4-6 weeks)
- Display **risk zones** on map using HERE Traffic + NCRB + data.gov.in datasets.
- Simple “risk-aware route” recommendation.
- Crowdsourcing module: allow users to report incidents (basic location + type).
- Mobile + web view for accessibility.

---

## Out of Scope (Phase 1)
- AI-based crime prediction models (will come in Phase 3)
- Complex user authentication (basic login is fine)
- Real-time push notifications for all users (can be Phase 2)

---

## Success Metrics
- MVP functional demo with accurate zone mapping in at least **1 pilot city** (e.g., Bangalore or Delhi).
- Integration of **minimum 2 reliable data sources**.
- Map rendering latency under **2 seconds** for safety overlay.

---

## Risks & Mitigation
- **Data Gaps**: Some regions have no digital crime data → use crowdsourced reports to fill gaps.
- **User Adoption**: Initial user base may be low → focus on targeted groups (delivery riders, tourists) first.
- **API Costs**: HERE/Google quotas could be expensive at scale → optimize calls & cache data.