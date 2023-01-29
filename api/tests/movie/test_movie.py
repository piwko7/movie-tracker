import pytest

from api.entities.movie import Movie
from api.repository.movie.abstractions import RepositoryException
from api.repository.movie.memory import MemoryMovieRepository


def test_create():
    repo = MemoryMovieRepository()
    movie = Movie(
        movie_id="test",
        title="My movie",
        description="My description",
        release_year=1991,
    )
    repo.create(movie)

    assert repo.get("test") is movie


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
                )
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
def test_get(movies_seed, movie_id, expected_result):
    repo = MemoryMovieRepository()
    for movie in movies_seed:
        repo.create(movie)
    movie = repo.get(movie_id=movie_id)

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
                )
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
                )
            ],
            "My movie",
            [
                Movie(
                    movie_id="my-id-2",
                    title="My movie",
                    description="My description",
                    release_year=1991,
                )
            ],
            id="results",
        ),
    ],
)
def test_get_by_title(movies_seed, movie_title, expected_result):
    repo = MemoryMovieRepository()
    for movie in movies_seed:
        repo.create(movie)
    result = repo.get_by_title(title=movie_title)
    assert result == expected_result


def test_update():
    repo = MemoryMovieRepository()
    repo.create(
        Movie(
            movie_id="my-id-2",
            title="My movie",
            description="My description",
            release_year=1991,
        )
    )
    repo.update(
        movie_id="my-id-2",
        update_parameters={
            "title": "updated-title",
            "description": "updated-description",
            "release_year": 2099,
            "watched": True,
        },
    )
    movie = repo.get("my-id-2")
    assert movie == Movie(
        movie_id="my-id-2",
        title="updated-title",
        description="updated-description",
        release_year=2099,
        watched=True,
    )


def test_update_fail():
    repo = MemoryMovieRepository()
    repo.create(
        Movie(
            movie_id="my-id-2",
            title="My movie",
            description="My description",
            release_year=1991,
        )
    )
    with pytest.raises(RepositoryException):
        repo.update(movie_id="my-id-2", update_parameters={"id": "fail"})


def test_delete():
    repo = MemoryMovieRepository()
    repo.create(
        Movie(
            movie_id="my-id-2",
            title="My movie",
            description="My description",
            release_year=1991,
        )
    )
    repo.delete("my-id-2")
    assert repo.get("my-id-2") is None
