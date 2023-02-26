from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    def __hash__(self) -> int:
        return 1

    # MongoDB Settings
    mongo_connection_string: str = Field("mongodb://localhost:27017")
    mongo_database_name: str = Field("movie_tracker_db")
