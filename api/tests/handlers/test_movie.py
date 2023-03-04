import functools
import uuid

import pytest
from starlette import status

from api.entities.movie import Movie
from api.handlers.movie import movie_repository
from api.repository.movie.memory import MemoryMovieRepository
from api.tests.fixture import test_client  # type: ignore


def memory_repository_dependency(dependency):
    return dependency


@pytest.mark.asyncio()
async def test_create_movie(test_client):
    # Setup
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    test_client.app.dependency_overrides[movie_repository] = patched_dependency

    # Test
    result = test_client.post(
        "/api/v1/movies",
        json={
            "movie_id": str(uuid.uuid4()),
            "title": "My Movie",
            "description": "string",
            "release_year": 2000,
            "watched": False,
        },
    )

    # Assertion
    assert result.status_code == status.HTTP_201_CREATED
    movie_id = result.json()
    movie = await repo.get(movie_id=movie_id)
    assert movie is not None


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "movie_json",
    [
        {
            "movie_id": str(uuid.uuid4()),
            "description": "string",
            "release_year": 2000,
            "watched": False,
        },
        {
            "movie_id": str(uuid.uuid4()),
            "title": "My Movie",
            "release_year": 2000,
            "watched": False,
        },
        {
            "movie_id": str(uuid.uuid4()),
            "title": "My Movie",
            "description": "string",
            "release_year": 1,
            "watched": False,
        },
    ],
)
async def test_create_movie_validation_error(test_client, movie_json):
    # Setup
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    test_client.app.dependency_overrides[movie_repository] = patched_dependency

    # Test
    result = test_client.post(
        "/api/v1/movies",
        json=movie_json,
    )

    # Assertion
    assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "movie_seed, movie_id, expected_status_code, expected_result",
    [
        ([], "random", 404, "Movie with id random is not exist"),
        (
            [
                Movie(
                    movie_id="found",
                    title="My movie",
                    description="Movie description",
                    release_year=2000,
                ),
            ],
            "found",
            200,
            '{"movie_id":"found","release_year":2000,"title":"My '
            'movie","description":"Movie description","watched":false}',
        ),
    ],
)
async def test_get_movie(
    test_client,
    movie_seed,
    movie_id,
    expected_status_code,
    expected_result,
):
    # Setup
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    test_client.app.dependency_overrides[movie_repository] = patched_dependency

    for movie in movie_seed:
        await repo.create(movie)

    # test
    result = test_client.get(f"/api/v1/movies/{movie_id}")

    # assert
    assert result.status_code == expected_status_code
    assert result.text == expected_result


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "movie_seed, movie_title, offset, limit, expected_result",
    [
        ([], "movie_title", 0, 1000, []),
        (
            [
                Movie(
                    movie_id="1",
                    title="My movie",
                    description="Movie description",
                    release_year=2000,
                ),
                Movie(
                    movie_id="2",
                    title="My movie",
                    description="Movie description",
                    release_year=2001,
                ),
                Movie(
                    movie_id="3",
                    title="My movie",
                    description="Movie description",
                    release_year=2002,
                ),
            ],
            "My movie",
            0,
            1000,
            [
                {
                    "description": "Movie description",
                    "movie_id": "1",
                    "release_year": 2000,
                    "title": "My movie",
                    "watched": False,
                },
                {
                    "description": "Movie description",
                    "movie_id": "2",
                    "release_year": 2001,
                    "title": "My movie",
                    "watched": False,
                },
                {
                    "description": "Movie description",
                    "movie_id": "3",
                    "release_year": 2002,
                    "title": "My movie",
                    "watched": False,
                },
            ],
        ),
    ],
)
async def test_get_movie_by_title(
    test_client,
    movie_seed,
    movie_title,
    offset,
    limit,
    expected_result,
):
    # Setup
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    test_client.app.dependency_overrides[movie_repository] = patched_dependency

    for movie in movie_seed:
        await repo.create(movie)

    # test
    result = test_client.get(f"/api/v1/movies/?title={movie_title}")

    # assertion
    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected_result


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "update_parameters, updated_movie",
    [
        (
            {"title": "My Title Update", "id": "test"},
            Movie(
                movie_id="top_movie",
                title="My Title Update",
                description="Needs Update",
                release_year=2000,
            ),
        ),
        (
            {"description": "My Desc Update", "random": "test"},
            Movie(
                movie_id="top_movie",
                title="Needs Update",
                description="My Desc Update",
                release_year=2000,
            ),
        ),
        (
            {"release_year": 3000},
            Movie(
                movie_id="top_movie",
                title="Needs Update",
                description="Needs Update",
                release_year=3000,
            ),
        ),
        (
            {"watched": True},
            Movie(
                movie_id="top_movie",
                title="Needs Update",
                description="Needs Update",
                release_year=2000,
                watched=True,
            ),
        ),
    ],
)
async def test_patch_update_movie(test_client, update_parameters, updated_movie):
    # Setup
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)

    test_client.app.dependency_overrides[movie_repository] = patched_dependency
    await repo.create(
        Movie(
            movie_id="top_movie",
            title="Needs Update",
            description="Needs Update",
            release_year=2000,
        )
    )

    # Test
    result = test_client.patch(f"/api/v1/movies/top_movie", json=update_parameters)

    # Assertion
    assert result.status_code == status.HTTP_200_OK
    assert result.json() == {"message": "Movie successfully updated"}
    if updated_movie is not None:
        assert await repo.get(movie_id="top_movie") == updated_movie


@pytest.mark.asyncio()
async def test_patch_update_movie_not_found(test_client):
    # Setup
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)

    test_client.app.dependency_overrides[movie_repository] = patched_dependency
    # Test
    result = test_client.patch(
        "/api/v1/movies/top_movie", json={"title": "Title Update"}
    )

    # Assertion
    assert result.status_code == status.HTTP_400_BAD_REQUEST
    assert result.text == "movie: top_movie not found"


@pytest.mark.asyncio()
async def test_delete_movie(test_client):
    # Setup
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)

    test_client.app.dependency_overrides[movie_repository] = patched_dependency
    await repo.create(
        Movie(
            movie_id="top_movie",
            title="Needs Update",
            description="Needs Update",
            release_year=2000,
        ),
    )

    # Test
    result = test_client.delete("/api/v1/movies/top_movie")

    # Assertion
    assert result.status_code == status.HTTP_204_NO_CONTENT
    assert await repo.get(movie_id="top_movie") is None


@pytest.mark.asyncio()
async def test_delete_movie_not_found(test_client):
    # Setup
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)

    test_client.app.dependency_overrides[movie_repository] = patched_dependency
    await repo.create(
        Movie(
            movie_id="top_movie",
            title="Needs Update",
            description="Needs Update",
            release_year=2000,
        ),
    )

    # Test
    result = test_client.delete("/api/v1/movies/not_found")

    # Assertion
    assert result.status_code == status.HTTP_400_BAD_REQUEST
