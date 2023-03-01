import uuid
from collections import namedtuple
from functools import lru_cache

from fastapi import APIRouter, Depends, Query
from starlette import status
from starlette.responses import Response

from api.entities.movie import Movie, UpdateMovie
from api.repository.movie.abstractions import RepositoryException
from api.repository.movie.mongo import MongoMovieRepository
from api.responses.detail import DetailResponse
from api.settings import Settings

router = APIRouter(prefix="/api/v1/movies", tags=["movies"])


@lru_cache()
def settings_instance():
    return Settings()


@lru_cache()
def movie_repository(settings: Settings = Depends(settings_instance)):
    return MongoMovieRepository(
        connection_string=settings.mongo_connection_string,
        database=settings.mongo_database_name,
    )


def pagination_params(offset: int = Query(0, qe=0), limit: int = Query(1000, le=1000)):
    Pagination = namedtuple("Pagination", ["offset", "limit"])
    return Pagination(offset=offset, limit=limit)


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
    "/title",
)
async def get_movie_by_title(
    title: str = Query(..., description="The title of the movie.", min_length=3),
    pagination=Depends(pagination_params),
    repo: MongoMovieRepository = Depends(
        movie_repository,
    ),
):
    movie = await repo.get_by_title(
        title=title,
        offset=pagination.offset,
        limit=pagination.limit,
    )
    if movie is None:
        return DetailResponse(message=f"Movie with title {title} is not exist")
    return movie


@router.get(
    "/{movie_id}",
)
async def get_movie_by_id(
    movie_id: str,
    repo: MongoMovieRepository = Depends(
        movie_repository,
    ),
):
    movie = await repo.get(movie_id=movie_id)
    if movie is None:
        return DetailResponse(message=f"Movie with id {movie_id} is not exist")
    return movie


@router.patch("/{movie_id}")
async def update_movie(
    movie_id: str,
    update_parameters: UpdateMovie,
    repo: MongoMovieRepository = Depends(
        movie_repository,
    ),
):
    try:
        await repo.update(
            movie_id=movie_id,
            update_parameters=update_parameters.dict(exclude_unset=True),
        )
        return DetailResponse(message="Movie successfully updated")
    except RepositoryException as exc:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=exc.args[0])


@router.delete(
    "/{movie_id}",
)
async def delete_movie_by_id(
    movie_id: str,
    repo: MongoMovieRepository = Depends(
        movie_repository,
    ),
):
    deleted_movie = await repo.delete(movie_id=movie_id)
    if deleted_movie.deleted_count == 0:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Specified movies does not exist",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
