"""
Application configuration and settings.
"""
from typing import List
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Settings(BaseSettings):
    """Application settings from environment variables."""

    # App
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    debug: bool = os.getenv("DEBUG", False)

    # RAG Service
    rag_service_host: str = os.getenv("RAG_SERVICE_HOST", "localhost")
    rag_service_port: int = os.getenv("RAG_SERVICE_PORT", 8000)
    rag_service_url: str = f"http://{rag_service_host}:{rag_service_port}"

    # Backend
    backend_host: str = os.getenv("BACKEND_HOST", "localhost")
    backend_port: int = os.getenv("BACKEND_PORT", 8000)
    backend_url: str = f"http://{backend_host}:{backend_port}"

    # Frontend
    frontend_host: str = os.getenv("FRONTEND_HOST", "localhost")
    frontend_port: int = os.getenv("FRONTEND_PORT", 3000)
    frontend_url: str = f"http://{frontend_host}:{frontend_port}"

    # Database (PostGreSQL)
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "password")
    db_name: str = os.getenv("DB_NAME", "swarn_db")
    db_port: int = os.getenv("DB_PORT", 5432)
    db_url: str = f"postgresql://{db_user}:{db_password}@postgres:{db_port}/{db_name}"

    # PGAdmin
    pgadmin_host: str = os.getenv("PGADMIN_HOST", "localhost")
    pgadmin_port: int = os.getenv("PGADMIN_PORT", 5050)
    pgadmin_email: str = os.getenv("PGADMIN_EMAIL", "admin@admin.com")
    pgadmin_password: str = os.getenv("PGADMIN_PASSWORD", "admin")
    pgadmin_url: str = f"http://{pgadmin_host}:{pgadmin_port}"

    # JWT
    jwt_secret: str = os.getenv("JWT_SECRET", "your-secret-key-change-this-in-production")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_access_token_expire_minutes: int = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60)

    # Qdrant
    qdrant_host: str = os.getenv("QDRANT_HOST", "localhost")
    qdrant_port: int = os.getenv("QDRANT_PORT", 6333)
    qdrant_url: str = f"http://{qdrant_host}:{qdrant_port}"
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "your-api-key-change-this-in-production")

    # Ollama
    ollama_host: str = os.getenv("OLLAMA_HOST", "localhost")
    ollama_port: int = os.getenv("OLLAMA_PORT", 11434)
    ollama_base_url: str = f"http://{ollama_host}:{ollama_port}"
    ollama_model: str = os.getenv("OLLAMA_MODEL", "mistral")

    # Grafana
    grafana_host: str = os.getenv("GRAFANA_HOST", "localhost")
    grafana_port: int = os.getenv("GRAFANA_PORT", 3000)
    grafana_url: str = f"http://{grafana_host}:{grafana_port}"
    grafana_user: str = os.getenv("GRAFANA_USER", "admin")
    grafana_password: str = os.getenv("GRAFANA_PASSWORD", "admin")

    # Prometheus
    prometheus_host: str = os.getenv("PROMETHEUS_HOST", "localhost")
    prometheus_port: int = os.getenv("PROMETHEUS_PORT", 9090)
    prometheus_url: str = f"http://{prometheus_host}:{prometheus_port}"

    # Loki
    loki_host: str = os.getenv("LOKI_HOST", "localhost")
    loki_port: int = os.getenv("LOKI_PORT", 3100)
    loki_url: str = f"http://{loki_host}:{loki_port}"

    # Tempo
    tempo_host: str = os.getenv("TEMPO_HOST", "localhost")
    tempo_port: int = os.getenv("TEMPO_PORT", 4317)
    tempo_url: str = f"{tempo_host}:{tempo_port}"

    # LangFuse
    langfuse_url: str = os.getenv("LANGFUSE_HOST", "http://langfuse-web:3000") 
    langfuse_public_key: str = os.getenv("LANGFUSE_PUBLIC_KEY", "your-api-key-change-this-in-production")
    langfuse_secret_key: str = os.getenv("LANGFUSE_SECRET_KEY", "your-api-key-change-this-in-production")
    langfuse_secret: str = os.getenv("LANGFUSE_SECRET", "changeme")
    langfuse_salt: str = os.getenv("LANGFUSE_SALT", "changeme")

    # Langfuse (OPTelemetry)
    otel_exporter_otlp_endpoint : str = f"{tempo_host}:{tempo_port}" # Tempo OTLP gRPC endpoint

    # CORS
    cors_origins: str = os.getenv("CORS_ORIGINS", "NA")

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
