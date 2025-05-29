# AI tooling logs, model choices, parameters

# AI Tool Usage Log

This document provides a detailed log of AI-tool prompts, code generation steps, and model parameters used in this project.

---

## 1. Model Parameters

| Parameter              | Value (example)                                   |
|-----------------------|---------------------------------------------------|
| ALPHA_VANTAGE_API_KEY | [REDACTED]                                        |
| REDIS_URL             | redis://localhost:6379                            |
| GROQ_API_KEY          | [REDACTED]                                        |
| GROQ_MODEL_ID         | mistral-saba-24b                                  |
| HF_API_KEY            | [REDACTED]                                        |

*Note: API keys are redacted for security. See `.env` for actual values.*

---

## 2. AI Tool Prompt Log

| Date       | Tool/Agent         | Prompt/Instruction                                      | Notes/Outcome                |
|------------|--------------------|---------------------------------------------------------|------------------------------|
| 2025-05-29 | langchain_agent.py | "Summarize the following text..."                       | Used Mistral SABA 24B model  |
| 2025-05-29 | api_agent.py       | "Fetch latest stock price for AAPL"                     | Used Alpha Vantage API       |

_Add new entries below as you use AI tools._

---

## 3. Code Generation Steps

### Example: Generating a Data Ingestion Script
- **Step 1:** User prompt: "Create a script to fetch SEC filings."
- **Step 2:** Tool: `filings_scraper.py` created in `data_ingestion/`.
- **Step 3:** Model: `mistral-saba-24b` (GROQ)
- **Step 4:** API key used: `GROQ_API_KEY`
- **Step 5:** Output: Script fetches and parses SEC filings.

---

## 4. Additional Notes
- Log all significant AI tool interactions here for reproducibility and auditing.
- Update model parameters if `.env` changes.

---
