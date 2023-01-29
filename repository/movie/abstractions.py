import abc
from typing import Optional, List

from repository.movie.movie import Movie


class RepositoryException(Exception):
    pass


class MovieRepository(abc.ABC):
    def create(self, movie: Movie):
        raise NotImplementedError

    def get(self, movie_id: str) -> Optional[Movie]:
        raise NotImplementedError

    def get_by_title(self, title: str) -> List[Movie]:
        raise NotImplementedError

    def delete(self, movie_id: str):
        raise NotImplementedError

    def update(self, movie_id: str, update_parameters: dict):
        raise NotImplementedError
