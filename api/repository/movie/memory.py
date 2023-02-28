from api.entities.movie import Movie
from api.repository.movie.abstractions import MovieRepository, RepositoryException


class MemoryMovieRepository(MovieRepository):
    """
    MemoryMovieRepository implements the repository pattern by using
    a simple in memory database.
    """

    def __init__(self):
        self._storage = {}

    async def create(self, movie: Movie):
        self._storage[movie.id] = movie

    async def get(self, movie_id: str) -> Movie | None:
        return self._storage.get(movie_id)

    async def get_by_title(
        self,
        title: str,
        offset: int = 0,
        limit: int = 1000,
    ) -> list[Movie]:
        return_value = []
        for _, value in self._storage.items()[offset : offset + limit]:
            if title == value.title:
                return_value.append(value)
        if limit == 0:
            return return_value[offset:]
        return return_value[offset : offset + limit]

    async def delete(self, movie_id: str):
        self._storage.pop(movie_id, None)

    async def update(self, movie_id: str, update_parameters: dict):
        movie = self._storage.get(movie_id)
        if movie is None:
            raise RepositoryException(f"movie: {movie_id} not found")
        for key, value in update_parameters.items():
            if key == "id":
                raise RepositoryException("can't update movie id")
            if hasattr(movie, key):
                # update the Movie entity field
                setattr(movie, key, value)
