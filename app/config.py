from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_DESC: str = "Data Center Infrastructure Management API"
    API_ROUTE: str = "/api/v1"

    DATABASE_DRIVER: str
    DATABASE_SERVER: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_PORT: str = "5432"

    @property
    def DATABASE_URL(self):
        return f"{self.DATABASE_DRIVER}://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_SERVER}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    class Config:
        env_file = ".env"

settings = Settings()
