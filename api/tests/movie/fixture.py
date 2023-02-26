import asyncio
import secrets

import pytest

from api.repository.movie.mongo import MongoMovieRepository


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
