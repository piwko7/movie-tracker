import abc

from api.entities.movie import Movie


class RepositoryException(Exception):
    pass


class MovieRepository(abc.ABC):
    async def create(self, movie: Movie):
        raise NotImplementedError

    async def get(self, movie_id: str) -> Movie | None:
        raise NotImplementedError

    async def get_by_title(self, title: str) -> list[Movie]:
        raise NotImplementedError

    async def delete(self, movie_id: str):
        raise NotImplementedError

    async def update(self, movie_id: str, update_parameters: dict):
        raise NotImplementedError
