import json
from os.path import join
from pydantic import BaseModel


class Config(BaseModel):
    files: list[str]
    output: str | list[str] | None = None
    separator: str = "\n"

    @property
    def destinations(self) -> list[str] | None:
        return [self.output] if isinstance(self.output, str) else self.output

    @classmethod
    def from_file(cls, path: str) -> "Config":
        with open(join(path), "r") as f:
            return cls(**json.load(f))
