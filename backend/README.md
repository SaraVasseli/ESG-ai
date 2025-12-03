# ESG-ai – Backend (FastAPI + LLM)

This is the backend for **ESG-ai**, a small demo that generates ESG disclosure text from structured metrics using a Large Language Model (LLM).

The goal is to simulate a tiny slice of an ESG platform: given a company, a few sustainability metrics, and selected frameworks (CSRD, SASB, GRI, CDP), the API returns:

- A draft **ESG disclosure section** (2–3 paragraphs)
- A list of **suggested improvements** to the disclosure or underlying performance

The backend is built with **Python + FastAPI** and integrates with an LLM provider (e.g., OpenAI).

---

## Tech stack

- **Python** (3.11+ recommended)
- **FastAPI** – web framework & OpenAPI/Swagger docs
- **Uvicorn** – ASGI server for local dev
- **Pydantic** – request/response validation and typing
- **python-dotenv** – load environment variables from `.env`
- **openai** – LLM client (can be swapped out later)
- **CORS** enabled for an Angular frontend (`http://localhost:4200`)

---

## Project structure

Inside `backend/`:

```text
backend/
  .venv/                 # Python virtual environment (local only, not committed)
  app/
    __init__.py
    main.py              # FastAPI app + routes (health, generate, history)
    config.py            # Env configuration (API keys, model name, etc.)
    models.py            # Pydantic data models (request & response schemas)
    llm_client.py        # LLM helper: builds prompts, calls model, parses output
  .env                   # Local environment variables (ignored by git)

```
