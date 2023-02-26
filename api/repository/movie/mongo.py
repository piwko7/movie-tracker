import motor.motor_asyncio

from api.entities.movie import Movie
from api.repository.movie.abstractions import MovieRepository, RepositoryException


class MongoMovieRepository(MovieRepository):
    """
    MongoMovieRepository implements the repository pattern for our Movie
    entity using MongoDB.
    """

    def __init__(
        self,
        connection_string: str,
        database: str,
    ):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
        self._database = self._client[database]
        # movie collections which holds our movie documents.
        self._movies = self._database["movies"]

    async def create(self, movie: Movie):
        await self._movies.insert_one(movie.dict())

    async def get(self, movie_id: str) -> Movie | None:
        document = await self._movies.find_one({"movie_id": movie_id})
        if document:
            return Movie(**document)
        return None

    async def get_by_title(self, title: str) -> list[Movie]:
        return_value = []
        documents_cursor = self._movies.find({"title": title})
        async for document in documents_cursor:
            return_value.append(Movie(**document))

        return return_value

    async def delete(self, movie_id: str):
        await self._movies.delete_one({"movie_id": movie_id})

    async def update(self, movie_id: str, update_parameters: dict):
        if "id" in update_parameters.keys():
            raise RepositoryException("can't update movie id.")
        result = await self._movies.update_one(
            {"movie_id": movie_id},
            {"$set": update_parameters},
        )
        if result.modified_count == 0:
            raise RepositoryException(f"movie: {movie_id} not found")
