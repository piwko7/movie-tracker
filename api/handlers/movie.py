import uuid

from fastapi import APIRouter, Depends
from starlette import status

from api.entities.movie import Movie
from api.repository.movie.mongo import MongoMovieRepository

router = APIRouter(prefix="/api/v1/movie", tags=["movies"])


def movie_repository():
    return MongoMovieRepository()


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
