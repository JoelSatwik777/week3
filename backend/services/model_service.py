from __future__ import annotations

from functools import lru_cache

import joblib
import pandas as pd

from backend.config.constants import MODEL_FEATURES
from backend.config.settings import get_settings
from backend.utils.errors import ServiceError


class ModelService:
    def __init__(self) -> None:
        settings = get_settings()
        self.model_path = settings.model_path

    @lru_cache(maxsize=1)
    def _load_model(self):
        if not self.model_path.exists():
            raise ServiceError(f'Model not found at {self.model_path}', status_code=500)
        return joblib.load(self.model_path)

    def _prepare_frame(self, rows: list[dict]) -> pd.DataFrame:
        frame = pd.DataFrame(rows)
        missing = [col for col in MODEL_FEATURES if col not in frame.columns]
        if missing:
            raise ServiceError(f'Missing required features: {missing}', status_code=422)
        return frame[MODEL_FEATURES]

    def predict_single(self, row: dict) -> tuple[float, float]:
        frame = self._prepare_frame([row])
        probability = float(self._load_model().predict_proba(frame)[0][1])
        confidence = abs(probability - 0.5) * 2
        return probability, confidence

    def predict_batch(self, frame: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
        prepared = self._prepare_frame(frame.to_dict(orient='records'))
        probabilities = pd.Series(self._load_model().predict_proba(prepared)[:, 1], index=frame.index)
        confidence = (probabilities - 0.5).abs() * 2
        return probabilities, confidence


@lru_cache(maxsize=1)
def get_model_service() -> ModelService:
    return ModelService()