from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_version: str
    log_level: str
    model_path: Path
    batch_output_dir: Path
    ollama_base_url: str
    ollama_model: str
    llm_timeout_seconds: int
    llm_max_chars: int
    llm_num_predict: int  # max tokens to generate; lower = faster on CPU
    llm_num_ctx: int  # context size; lower = faster and less RAM on CPU
    cors_origins: list[str]


def _get_cors_origins() -> list[str]:
    # development builds sometimes run on 5173 or 5174 depending on the
    # framework version.  By default we permit both ports so the frontend
    # can communicate without requiring a manual environment tweak.  In a
    # production deployment you should explicitly set `CORS_ORIGINS` to the
    # correct hostnames for security.
    raw = os.getenv(
        'CORS_ORIGINS',
        'http://localhost:5173,http://127.0.0.1:5173,'
        'http://localhost:5174,http://127.0.0.1:5174',
    )
    return [item.strip() for item in raw.split(',') if item.strip()]


@lru_cache
def get_settings() -> Settings:
    root = Path(__file__).resolve().parents[2]
    settings = Settings(
        app_name=os.getenv('APP_NAME', 'Banking Customer Churn Intelligence API'),
        app_version=os.getenv('APP_VERSION', '1.0.0'),
        log_level=os.getenv('LOG_LEVEL', 'INFO'),
        model_path=Path(os.getenv('MODEL_PATH', str(root / 'ml' / 'banking_model.pkl'))),
        batch_output_dir=Path(
            os.getenv('BATCH_OUTPUT_DIR', str(root / 'backend' / 'storage' / 'batch_outputs'))
        ),
        ollama_base_url=os.getenv('OLLAMA_BASE_URL', 'http://127.0.0.1:11434'),
        ollama_model=os.getenv('OLLAMA_MODEL', 'llama3.2:3b'),  # CPU-friendly; use 1b for even faster
        llm_timeout_seconds=int(os.getenv('LLM_TIMEOUT_SECONDS', '60')),
        # default increased so that short portfolio summaries /
        # recommendation lists are unlikely to be clipped.  Users can still
        # override with the LLM_MAX_CHARS env var if they need a tighter cap.
        llm_max_chars=int(os.getenv('LLM_MAX_CHARS', '2000')),
        # num_predict controls how many tokens the model may generate.  The
        # default of 100 sometimes cuts off long executive summaries or lists;
        # bump to 200 so there's ample headroom.  Override with the
        # LLM_NUM_PREDICT environment variable if you need even more.
        llm_num_predict=int(os.getenv('LLM_NUM_PREDICT', '200')),
        llm_num_ctx=int(os.getenv('LLM_NUM_CTX', '2048')),  # smaller context = faster on CPU
        cors_origins=_get_cors_origins(),
    )
    os.makedirs(settings.batch_output_dir, exist_ok=True)
    return settings
