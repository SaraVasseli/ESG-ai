# 🚀 ESG-AI

ThiAI-Powered ESG Disclosure Generator

Python FastAPI backend + Angular 17 frontend + OpenAI LLM

ESG-AI is a full-stack demonstration project that generates ESG (Environmental, Social, Governance) disclosures using LLMs.
It mirrors real sustainability reporting workflows used by organizations preparing disclosures for CSRD, SASB, GRI, and CDP frameworks.

This project was built as a 2–3 day technical demo to showcase:

🔹 LLM integration (OpenAI API)

🔹 Python FastAPI backend with clean architecture

🔹 Angular 17 frontend using new signals, inject(), and @if / @for

🔹 Lightweight UI using Angular Material

🔹 Token usage tracking & cost awareness

🔹 A realistic ESG data flow, similar to industry tools like Novisto

---

## Project Structure

```text
ESG-ai/
│
├── backend/              # FastAPI + OpenAI
│   ├── app/
│   │   ├── main.py       # Routes & API definitions
│   │   ├── models.py     # Pydantic schemas
│   │   ├── llm_client.py # LLM interface + token usage tracking
│   │   ├── config.py     # Environment & API settings
│   │   └── __init__.py
│   ├── .env              # API keys (ignored in git)
│   ├── requirements.txt
│   └── README.md 
│
└frontend/
│
├── public/
│   └── favicon.ico
│
├── src/
│   ├── app/
│   │   ├── services/
│   │   │   └── esg-ai.service.ts      # API calls to FastAPI backend
│   │   ├── units/
│   │   │   └── util.ts                
│   │   ├── app.config.ts              # App-wide providers
│   │   ├── app.html                   # Angular Material UI template
│   │   ├── app.scss                   # Layout & Material styling
│   │   ├── app.spec.ts                # Test scaffold (Angular CLI default)
│   │   └── app.ts                     # Standalone component (signals + logic)
│   │
│   ├── index.html                     # Root HTML entrypoint
│   ├── main.ts                        # Bootstrap for standalone Angular build
│   └── styles.scss                    # Global styles + Material theme
│
├── angular.json
├── package.json
└── README.md 

```

---

## ESG Overview (Why This Project Makes Sense)

ESG reports summarize how companies manage:

🔹Environmental impacts (emissions, energy, waste)

🔹Social impacts (diversity, safety, training)

🔹Governance practices (board composition, oversight)


Companies disclose performance annually and often reference frameworks:

🔹CSRD — EU mandatory sustainability reporting

🔹SASB — investor-focused US standards

🔹GRI — global sustainability reporting

🔹CDP — climate/water/forests questionnaire

This project simulates that workflow:

1 - User inputs company ESG context (sector, frameworks, initiatives)

2- User supplies quantitative ESG metrics

3- Backend constructs a regulatory-style prompt

4- LLM outputs:

🔹A disclosure-ready narrative

🔹Improvement recommendations

🔹Token usage metadata