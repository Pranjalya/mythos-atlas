"""
Backend Configuration Settings for MythosAtlas.
"""

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    STATIC_MYTHS_FILE: Path = DATA_DIR / "processed" / "static_myths.json"
    ENRICHED_MYTHS_FILE: Path = DATA_DIR / "processed" / "enriched_myths.json"
    MOTIF_EMBEDDINGS_FILE: Path = DATA_DIR / "processed" / "motif_embeddings.json"

    # Qdrant collection
    QDRANT_COLLECTION: str = "mythos_motifs"

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent.parent / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
