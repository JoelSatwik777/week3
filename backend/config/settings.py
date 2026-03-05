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
    cors_origins: list[str]


def _get_cors_origins() -> list[str]:
    raw = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173')
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
        ollama_model=os.getenv('OLLAMA_MODEL', 'llama3'),
        llm_timeout_seconds=int(os.getenv('LLM_TIMEOUT_SECONDS', '90')),
        llm_max_chars=int(os.getenv('LLM_MAX_CHARS', '1800')),
        cors_origins=_get_cors_origins(),
    )
    os.makedirs(settings.batch_output_dir, exist_ok=True)
    return settings
