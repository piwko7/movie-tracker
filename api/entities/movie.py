from pydantic import BaseModel


class Movie(BaseModel):
    movie_id: str
    title: str
    description: str
    release_year: int
    watched: bool = False

    # def __init__(
    #     self,
    #     *,
    #     movie_id: str,
    #     title: str,
    #     description: str,
    #     release_year: int,
    #     watched: bool = False,
    # ):
    #     if movie_id is None:
    #         raise ValueError("Move id is required!")
    #     self._id = movie_id
    #     self._title = title
    #     self._description = description
    #     self._release_year = release_year
    #     self._watched = watched

    @property
    def id(self) -> str:
        return self.movie_id

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Movie):
            return False
        return (
            self.id == o.id
            and self.title == o.title
            and self.description == o.description
            and self.release_year == o.release_year
            and self.watched == o.watched
        )
