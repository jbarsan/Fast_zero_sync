# SettingsConfigDict serve para ler o arquivo .env
from pydantic_settings import BaseSettings, SettingsConfigDict

"""
O parâmetro extra='ignore', serve para ignorar variáveis extras que não são
utilizadas no sistema.
"""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
