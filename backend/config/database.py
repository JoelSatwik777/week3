from dataclasses import dataclass
import os


@dataclass(frozen=True)
class DatabaseSettings:
    url: str = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/churndb')
    pool_size: int = int(os.getenv('DB_POOL_SIZE', '5'))