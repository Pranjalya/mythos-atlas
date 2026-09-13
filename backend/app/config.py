"""
Backend Configuration Settings for MythosAtlas.
"""

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


def _find_data_dir() -> Path:
    # 1. backend/data (when deployed to Vercel/Docker where backend/ is the root)
    backend_data = Path(__file__).resolve().parent.parent / "data"
    if (backend_data / "processed" / "enriched_myths.json").exists():
        return backend_data
    # 2. repo_root/data (local development in monorepo)
    repo_data = Path(__file__).resolve().parent.parent.parent / "data"
    if (repo_data / "processed" / "enriched_myths.json").exists():
        return repo_data
    # 3. app/data fallback
    app_data = Path(__file__).resolve().parent / "data"
    if (app_data / "processed" / "enriched_myths.json").exists():
        return app_data
    return backend_data


class Settings(BaseSettings):
    # API Credentials
    QDRANT_URL: Optional[str] = None
    QDRANT_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    # Server settings
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    ENVIRONMENT: str = "development"

    # Data paths
    DATA_DIR: Path = _find_data_dir()
    STATIC_MYTHS_FILE: Path = DATA_DIR / "processed" / "static_myths.json"
    ENRICHED_MYTHS_FILE: Path = DATA_DIR / "processed" / "enriched_myths.json"
    MOTIF_EMBEDDINGS_FILE: Path = DATA_DIR / "processed" / "motif_embeddings.json"

    # Qdrant collection
    QDRANT_COLLECTION: str = "mythos_motifs"

    model_config = SettingsConfigDict(
        env_file=[
            str(Path(__file__).resolve().parent.parent / ".env"),
            str(Path(__file__).resolve().parent.parent.parent / ".env"),
        ],
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
