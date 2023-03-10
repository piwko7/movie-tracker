import asyncio
import secrets

import pytest
from starlette.testclient import TestClient

from api.api import create_app
from api.repository.movie.mongo import MongoMovieRepository


@pytest.fixture()
def test_client():
    return TestClient(app=create_app())


@pytest.fixture()
def mongo_movie_repo_fixture():
    random_database_name = secrets.token_hex(5)
    repo = MongoMovieRepository(
        connection_string="mongodb://localhost:27017",
        database=random_database_name,
    )
    yield repo
    loop = asyncio.get_event_loop()
    loop.run_until_complete(repo._client.drop_database(random_database_name))
