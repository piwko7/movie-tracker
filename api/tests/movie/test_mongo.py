import pytest

from api.entities.movie import Movie
from api.repository.movie.mongo import MongoMovieRepository


@pytest.mark.asyncio
async def test_create():
    repo = MongoMovieRepository(
        connection_string="mongodb://localhost:27017",
        database="my-database"
    )
    await repo.create(movie=Movie(
        movie_id="first",
        title="My movie",
        description="My movie descriptions",
        release_year=1991
    ))
    movie = await repo.get("first")
    assert movie == Movie(
        movie_id="first",
        title="My movie",
        description="My movie descriptions",
        release_year=1991
    )
    await repo.delete("first")


@pytest.mark.asyncio
async def test_get():
    pass


@pytest.mark.asyncio
async def test_get_by_title():
    pass


@pytest.mark.asyncio
async def test_update():
    pass


@pytest.mark.asyncio
async def test_delete():
    pass
