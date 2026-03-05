from __future__ import annotations

from io import BytesIO
from pathlib import Path
import uuid

import pandas as pd
from fastapi import UploadFile

from backend.config.constants import ALLOWED_UPLOAD_EXTENSIONS, MAX_BATCH_ROWS
from backend.config.settings import get_settings
from backend.utils.errors import ServiceError


def _extension(filename: str) -> str:
    return Path(filename or '').suffix.lower()


def read_tabular_upload(upload: UploadFile) -> pd.DataFrame:
    extension = _extension(upload.filename or '')
    if extension not in ALLOWED_UPLOAD_EXTENSIONS:
        raise ServiceError('Unsupported file type. Upload CSV or Excel file.', status_code=415)

    try:
        raw = upload.file.read()
    finally:
        upload.file.close()

    if not raw:
        raise ServiceError('Uploaded file is empty.', status_code=400)

    try:
        if extension == '.csv':
            frame = pd.read_csv(BytesIO(raw))
        else:
            frame = pd.read_excel(BytesIO(raw))
    except Exception as exc:
        raise ServiceError(f'Could not parse uploaded file: {exc}', status_code=400) from exc

    if frame.empty:
        raise ServiceError('Uploaded file has no rows.', status_code=400)
    if len(frame) > MAX_BATCH_ROWS:
        raise ServiceError(f'File too large. Maximum {MAX_BATCH_ROWS} rows allowed.', status_code=413)

    return frame


def store_processed_file(frame: pd.DataFrame) -> tuple[str, Path]:
    settings = get_settings()
    file_id = str(uuid.uuid4())
    output_path = settings.batch_output_dir / f'{file_id}.csv'
    frame.to_csv(output_path, index=False)
    return file_id, output_path


def resolve_processed_file(file_id: str) -> Path:
    settings = get_settings()
    safe_id = Path(file_id).name
    path = settings.batch_output_dir / f'{safe_id}.csv'
    if not path.exists():
        raise ServiceError('Processed file not found.', status_code=404)
    return path