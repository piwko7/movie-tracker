from typing import Optional

from pydantic import BaseModel, validator


class Movie(BaseModel):
    movie_id: str
    release_year: int
    title: str
    description: str
    watched: bool = False

    @validator("title")
    def title_length_gt_three(cls, v):
        if len(v) < 4:
            raise ValueError("Title length must be greater than 3 characters")
        return v

    @validator("description")
    def description_length_gt_three(cls, v):
        if len(v) < 4:
            raise ValueError("Description length must be greater than 3 characters")
        return v

    @validator("release_year")
    def release_year_gt_1900(cls, v):
        if v < 1900:
            raise ValueError("Release year must be greater than 1900")
        return v

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


class UpdateMovie(BaseModel):
    release_year: Optional[int]
    title: Optional[str]
    description: Optional[str]
    watched: Optional[bool]
