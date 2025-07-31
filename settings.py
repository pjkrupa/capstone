from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional 

class Settings(BaseSettings):
    pg_host: str
    pg_port: int
    pg_user: str 
    pg_password: Optional[str] = ""

    model_config = SettingsConfigDict(env_file='.env')
