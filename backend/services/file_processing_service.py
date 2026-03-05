from __future__ import annotations

import pandas as pd
from fastapi import UploadFile

from backend.services.file_service import read_tabular_upload, resolve_processed_file, store_processed_file


def parse_upload_file(upload: UploadFile) -> pd.DataFrame:
    return read_tabular_upload(upload)


def save_processed_frame(frame: pd.DataFrame) -> tuple[str, str]:
    file_id, _ = store_processed_file(frame)
    return file_id, f'/predict-batch/download/{file_id}'


def get_processed_file_path(file_id: str):
    return resolve_processed_file(file_id)