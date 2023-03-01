import functools
import uuid

import pytest

from api.handlers.movie import movie_repository
from api.repository.movie.memory import MemoryMovieRepository
from api.tests.fixture import test_client


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
    assert result.status_code == 201
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
    assert result.status_code == 422


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "movie_seed, movie_id, expected_status_code, expected_result",
    [
        ([], "random", 404, "Movie with id random is not exist"),
    ],
)
async def test_get_movie(
    test_client, movie_seed, movie_id, expected_status_code, expected_result,
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
