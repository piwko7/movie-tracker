import pytest

from api.entities.movie import Movie
from api.repository.movie.abstractions import RepositoryException
from api.repository.movie.memory import MemoryMovieRepository


@pytest.mark.asyncio
async def test_create():
    repo = MemoryMovieRepository()
    movie = Movie(
        movie_id="test",
        title="My movie",
        description="My description",
        release_year=1991,
    )

    await repo.create(movie)
    assert await repo.get("test") is movie


@pytest.mark.parametrize(
    "movies_seed, movie_id, expected_result",
    [
        pytest.param([], "my-id", None, id="empty"),
        pytest.param(
            [
                Movie(
                    movie_id="my-id",
                    title="My movie",
                    description="My description",
                    release_year=1991,
                ),
            ],
            "my-id",
            Movie(
                movie_id="my-id",
                title="My movie",
                description="My description",
                release_year=1991,
            ),
            id="actual-movie",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get(movies_seed, movie_id, expected_result):
    repo = MemoryMovieRepository()
    for movie in movies_seed:
        await repo.create(movie)

    # noinspection PyTypeChecker
    movie = await repo.get(movie_id=movie_id)
    assert movie == expected_result


@pytest.mark.parametrize(
    "movies_seed, movie_title, expected_result",
    [
        pytest.param([], "some-title", [], id="empty-results"),
        pytest.param(
            [
                Movie(
                    movie_id="my-id",
                    title="My movie",
                    description="My description",
                    release_year=1991,
                ),
            ],
            "some-title",
            [],
            id="empty-results-2",
        ),
        pytest.param(
            [
                Movie(
                    movie_id="my-id-2",
                    title="My movie",
                    description="My description",
                    release_year=1991,
                ),
            ],
            "My movie",
            [
                Movie(
                    movie_id="my-id-2",
                    title="My movie",
                    description="My description",
                    release_year=1991,
                ),
            ],
            id="results",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_title(movies_seed, movie_title, expected_result):
    repo = MemoryMovieRepository()
    for movie in movies_seed:
        await repo.create(movie)
    # noinspection PyTypeChecker
    result = await repo.get_by_title(title=movie_title)
    assert result == expected_result


@pytest.mark.asyncio
async def test_update():
    repo = MemoryMovieRepository()
    await repo.create(
        Movie(
            movie_id="my-id-2",
            title="My movie",
            description="My description",
            release_year=1991,
        ),
    )
    await repo.update(
        movie_id="my-id-2",
        update_parameters={
            "title": "updated-title",
            "description": "updated-description",
            "release_year": 2099,
            "watched": True,
        },
    )
    movie = await repo.get("my-id-2")
    assert movie == Movie(
        movie_id="my-id-2",
        title="updated-title",
        description="updated-description",
        release_year=2099,
        watched=True,
    )


# @pytest.mark.asyncio
# def test_update_fail():
#     repo = MemoryMovieRepository()
#     await repo.create(
#         Movie(
#             movie_id="my-id-2",
#             title="My movie",
#             description="My description",
#             release_year=1991,
#         ),
#     )
#     with pytest.raises(RepositoryException):
#         await repo.update(movie_id="my-id-2", update_parameters={"id": "fail"})
#
#
# @pytest.mark.asyncio
# def test_delete():
#     repo = MemoryMovieRepository()
#     await repo.create(
#         Movie(
#             movie_id="my-id-2",
#             title="My movie",
#             description="My description",
#             release_year=1991,
#         ),
#     )
#     await repo.delete("my-id-2")
#     assert await repo.get("my-id-2") is None
