# Banking Customer Churn Intelligence System

Production-style hybrid AI churn platform with:
- React dashboard frontend
- FastAPI modular backend
- Scikit-learn ML inference pipeline
- Ollama/Llama3 advisory generation (explanatory only)
- Single and batch portfolio prediction modes

## Architecture

### Backend (`backend/`)
- `routers/`: HTTP route definitions
- `services/`: ML, LLM, retention, file, and auth services
- `schemas/`: Pydantic request/response contracts
- `models/`: domain and database-ready model structures
- `utils/`: risk classification, formatting, logging, and errors
- `config/`: environment and constants configuration

### Frontend (`frontend/src/`)
- `components/layout/`: top navigation and shell controls
- `components/common/`: shared mode toggle
- `components/single/`: single-customer form + result UI
- `components/batch/`: file upload, summary cards, and distribution chart
- `api/`: backend API client layer
- `constants/`: form field metadata

### ML (`ml/`)
- `data_analysis.py`: training and model export pipeline
- `predict.py`: inference wrapper with confidence output
- `config.py`: shared dataset/model paths and feature list

## API Endpoints

### Single prediction
- `POST /predict`
- `POST /api/v1/predict`

Request body fields:
- `CreditScore`, `Geography`, `Gender`, `Age`, `Tenure`, `Balance`, `NumOfProducts`, `HasCrCard`, `IsActiveMember`, `EstimatedSalary`

Response:
- `churn_probability`
- `confidence`
- `risk_level`
- `retention_suggestions`
- `ai_advisory_report`

### Batch prediction
- `POST /predict-batch`
- `POST /api/v1/predict-batch`

Form data:
- `file`: CSV/XLSX/XLS
- `include_portfolio_ai_summary`: `true|false`

Response:
- `summary`
- `download_file_id`
- `download_url`
- `portfolio_ai_summary_report` (optional)

Download endpoint:
- `GET /predict-batch/download/{file_id}`

## Setup

1. Create and activate virtual environment.
2. Install backend dependencies:
   - `pip install -r requirements.txt`
3. Install frontend dependencies:
   - `cd frontend && npm install`
4. Optional LLM setup (CPU-friendly small model for faster summaries):
   - `ollama pull llama3.2:3b`
   - `ollama serve`

## Run

### Backend
`uvicorn backend.main:app --reload`

### Frontend
`cd frontend && npm run dev`

## Environment Configuration

Copy `.env.example` to `.env` and adjust values as needed:
- app metadata and logging
- model and storage paths
- Ollama endpoint/model/timeout and CPU-tuning (LLM_NUM_PREDICT, LLM_NUM_CTX)
- Maximum number of characters allowed for LLM responses (LLM_MAX_CHARS).  If you find that the “Recommendations to reduce churn” or executive summary are getting cut off, bump this value or remove the limit completely.
- CORS origins (defaults to localhost ports 5173 and 5174 for front‑end development; override with `CORS_ORIGINS` if you host the frontend elsewhere)

### LLM tuning

* `LLM_MAX_CHARS` – maximum number of characters kept from a response (default 2000).  Raise if you notice truncation in the AI summary or executive note.  Lower for tighter CPU control.
* `LLM_NUM_PREDICT` – maximum number of tokens the model may generate (default 200).  If the executive summary ends mid‑sentence or you only get 1‑2 of the requested
  sentences, increase this value rather than switching models.  Larger models may
  require a higher token limit to produce more verbose output.
* `OLLAMA_MODEL` – you can certainly try a different model for quality; however,
  the symptoms described (half‑generated content, trailing commas) are usually
  due to token/char limits or the prompt itself, not the model size.

## Docker Readiness

- `Dockerfile` for backend container
- `docker-compose.yml` for backend + frontend local containerized run

## Notes

- ML model decides churn probability.
- LLM only explains and recommends retention actions.
- If Ollama is down/timed out, API returns safe advisory fallback text.
- Default LLM is `llama3.2:3b` (CPU-friendly). Set `OLLAMA_MODEL=llama3.2:1b` in `.env` for even faster runs.