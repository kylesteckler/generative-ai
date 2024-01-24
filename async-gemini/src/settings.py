from pydantic_settings import BaseSettings, SettingsConfigDict

class GoogleCloudSettings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, validate_default=False, env_prefix='GCP_')
    PROJECT_ID: str
    REGION: str = "us-central1"

# Env variable GCP_PROJECT_ID must be set or this will throw an exception
gcp_settings = GoogleCloudSettings() # type: ignore
