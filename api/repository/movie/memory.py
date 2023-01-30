import motor.motor_asyncio

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

    async def get_by_title(self, title: str) -> list[Movie]:
        return_value = []
        for _, value in self._storage.items():
            if title == value.title:
                return_value.append(value)
        return return_value

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
                setattr(movie, f"_{key}", value)


class MongoMovieRepository(MovieRepository):
    """
    MongoMovieRepository implements the repository pattern for our Movie
    entity using MongoDB.
    """

    def __init__(self, connection_string: str = "mongodb://localhost:27017"):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
        self._database = self._client["movie_tracker_db"]
        # movie collections which holds our movie documents.
        self._movies = self._database["movies"]

    async def create(self, movie: Movie):
        pass

    async def get(self, movie_id: str) -> Movie | None:
        pass

    async def get_by_title(self, title: str) -> list[Movie]:
        pass

    async def delete(self, movie_id: str):
        pass

    async def update(self, movie_id: str, update_parameters: dict):
        pass
