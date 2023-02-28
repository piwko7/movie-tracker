import pytest

from api.entities.movie import Movie
from api.repository.movie.abstractions import RepositoryException

# noinspection PyUnresolvedReferences
from api.tests.fixture import mongo_movie_repo_fixture


@pytest.mark.asyncio
async def test_create(mongo_movie_repo_fixture):
    await mongo_movie_repo_fixture.create(
        movie=Movie(
            movie_id="first",
            title="My movie",
            description="My movie descriptions",
            release_year=1991,
        )
    )
    movie = await mongo_movie_repo_fixture.get("first")
    assert movie == Movie(
        movie_id="first",
        title="My movie",
        description="My movie descriptions",
        release_year=1991,
    )


@pytest.mark.parametrize(
    "initial_movies, movie_id, expected_result",
    [
        pytest.param([], "any", None, id="empty-case"),
        pytest.param(
            [
                Movie(
                    movie_id="first",
                    title="My movie",
                    description="My movie descriptions",
                    release_year=1991,
                ),
                Movie(
                    movie_id="second",
                    title="My second movie",
                    description="My second movie descriptions",
                    release_year=1991,
                ),
            ],
            "second",
            Movie(
                movie_id="second",
                title="My second movie",
                description="My second movie descriptions",
                release_year=1991,
            ),
            id="movie-found-case",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get(mongo_movie_repo_fixture, initial_movies, movie_id, expected_result):
    for movie in initial_movies:
        await mongo_movie_repo_fixture.create(movie)
    movie = await mongo_movie_repo_fixture.get(movie_id)
    assert movie == expected_result


@pytest.mark.parametrize(
    "initial_movies, searched_title, expected_result",
    [
        pytest.param([], "random title", [], id="empty-case"),
        pytest.param(
            [
                Movie(
                    movie_id="first",
                    title="My movie",
                    description="My movie descriptions",
                    release_year=1991,
                ),
                Movie(
                    movie_id="second",
                    title="My second movie",
                    description="My second movie descriptions",
                    release_year=1991,
                ),
                Movie(
                    movie_id="first_remake",
                    title="My movie",
                    description="My movie descriptions remake of the first movie from 2022",
                    release_year=2025,
                ),
            ],
            "My movie",
            [
                Movie(
                    movie_id="first",
                    title="My movie",
                    description="My movie descriptions",
                    release_year=1991,
                ),
                Movie(
                    movie_id="first_remake",
                    title="My movie",
                    description="My movie descriptions remake of the first movie from 2022",
                    release_year=2025,
                ),
            ],
            id="found-movies",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_title(
    mongo_movie_repo_fixture,
    initial_movies,
    searched_title,
    expected_result,
):
    for movie in initial_movies:
        await mongo_movie_repo_fixture.create(movie)
    movies = await mongo_movie_repo_fixture.get_by_title(title=searched_title)
    assert movies == expected_result


@pytest.mark.asyncio
async def test_update(mongo_movie_repo_fixture):
    initial_movie = Movie(
        movie_id="first",
        title="My movie",
        description="My movie descriptions",
        release_year=1991,
    )
    await mongo_movie_repo_fixture.create(initial_movie)
    await mongo_movie_repo_fixture.update(
        movie_id="first",
        update_parameters={"title": "Update title"},
    )
    updated_movie = await mongo_movie_repo_fixture.get(movie_id="first")
    assert updated_movie == Movie(
        movie_id="first",
        title="Update title",
        description="My movie descriptions",
        release_year=1991,
    )


@pytest.mark.asyncio
async def test_update_fail(mongo_movie_repo_fixture):
    initial_movie = Movie(
        movie_id="first",
        title="My movie",
        description="My movie descriptions",
        release_year=1991,
    )
    await mongo_movie_repo_fixture.create(initial_movie)
    with pytest.raises(RepositoryException):
        await mongo_movie_repo_fixture.update(
            movie_id="first",
            update_parameters={"id": "Not allowed"},
        )


@pytest.mark.asyncio
async def test_delete(mongo_movie_repo_fixture):
    initial_movie = Movie(
        movie_id="first one",
        title="My movie",
        description="My movie descriptions",
        release_year=1991,
    )
    await mongo_movie_repo_fixture.create(initial_movie)
    await mongo_movie_repo_fixture.delete(movie_id="first one")
    assert await mongo_movie_repo_fixture.get(movie_id="first one") is None
