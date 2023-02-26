import uuid
from functools import lru_cache

from fastapi import APIRouter, Depends
from starlette import status

from api.entities.movie import Movie
from api.repository.movie.mongo import MongoMovieRepository
from api.settings import Settings
from build.lib.api.responses.detail import DetailResponse

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
) -> str:
    movie.movie_id = str(uuid.uuid4())
    await repo.create(movie)
    return movie.movie_id


@router.get(
    "/{movie_id}",
)
async def get_movie_by_id(
    movie_id=str,
    repo: MongoMovieRepository = Depends(
        movie_repository,
    ),
) -> Movie:
    movie = await repo.get(movie_id=movie_id)
    if movie is None:
        return DetailResponse(message=f"Movie with id {movie_id} is not exist")
    return movie


@router.get(
    "/{title}",
)
async def get_movie_by_title(
    title=str,
    repo: MongoMovieRepository = Depends(
        movie_repository,
    ),
) -> list[Movie]:
    movie = await repo.get_by_title(title=title)
    if movie is None:
        return DetailResponse(message=f"Movie with title {title} is not exist")
    return movie
