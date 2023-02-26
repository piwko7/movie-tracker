import uuid
from functools import lru_cache

from fastapi import APIRouter, Depends
from starlette import status

from api.entities.movie import Movie
from api.repository.movie.mongo import MongoMovieRepository
from api.settings import Settings

router = APIRouter(prefix="/api/v1/movie", tags=["movies"])


@lru_cache()
def settings_instance():
    return Settings()


@lru_cache()
def movie_repository(settings: Settings = Depends(settings_instance)):
    return MongoMovieRepository(
        connection_string=settings.mongo_connection_string,
        database=settings.mongo_database_name,
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_movie(
    movie: Movie,
    repo: MongoMovieRepository = Depends(
        movie_repository,
    ),
):
    movie.movie_id = str(uuid.uuid4())
    await repo.create(movie)
    return movie.movie_id
