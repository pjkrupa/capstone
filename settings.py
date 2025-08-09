from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, field_validator, PostgresDsn
from typing import Optional 

class Settings(BaseSettings):
    pg_host: str
    pg_port: int
    pg_user: str 
    pg_database: str
    pg_password: Optional[str] = ""
    model: Optional[str] = "openai/gpt-4o"
    api_key: Optional[str] = ""
    path: Optional[str] = ""
    runs: Optional[int] = 0
    run_id: Optional[str] = ""
    function: Optional[dict] = {}
    function_path: Optional[str] = ""
    model_config = SettingsConfigDict(env_file='.env')
