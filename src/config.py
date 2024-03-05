from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    # Getting info about Live DB
    POSTGRES_USER_LIVE: str
    POSTGRES_PASSWORD_LIVE: str
    POSTGRES_SERVER_LIVE: str
    POSTGRES_PORT_LIVE: int
    POSTGRES_DB_LIVE: str

    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str
    PGADMIN_PORT: int

    SRC_PORT: int
    DOCKER_PORT: int

    ACCESS_TOKEN_EXPIRE: int = 60 * 60 * 24 * 30  # seconds * minutes * hours * days

    SECRET_KEY: str = 'secret_key :)'
    ALGORITHM: str = 'HS256'

    @property
    def database_url_live(self):
        return f'postgresql://{self.POSTGRES_USER_LIVE}:{self.POSTGRES_PASSWORD_LIVE}@' \
               f'{self.POSTGRES_SERVER_LIVE}:{self.POSTGRES_PORT_LIVE}/{self.POSTGRES_DB_LIVE}'


settings = Settings()
