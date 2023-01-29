from typing import List, Optional

from repository.movie.abstractions import MovieRepository, RepositoryException
from repository.movie.movie import Movie


class MemoryMovieRepository(MovieRepository):
    def __init__(self):
        self._storage = {}

    def create(self, movie: Movie):
        self._storage[movie.id] = movie

    def get(self, movie_id: str) -> Optional[Movie]:
        return self._storage.get(movie_id)

    def get_by_title(self, title: str) -> List[Movie]:
        return_value = []
        for _, value in self._storage.items():
            if title == value.tittle:
                return_value.append(value)
            return return_value

    def delete(self, movie_id: str):
        self._storage.pop(movie_id, None)

    def update(self, movie_id: str, update_parameters: dict):
        movie = self._storage.get(movie_id)
        if movie is None:
            raise RepositoryException(f"movie: {movie_id} not found")
        for key, value in update_parameters.items():
            if key == "id":
                raise RepositoryException(f"movie: {movie_id} not found")
            if hasattr(movie, key):
                # update the Movie entity field
                setattr(movie, key, value)
                movie.key = value
