from glob import glob
from typing import Any, Generator
from pydantic import BaseModel, field_validator
from .component import Component

CONFIG_FILE_NAME = "catc.json"


class Config(BaseModel):
    include: list[str]
    out: list[str] | None = None

    @field_validator("out")
    @classmethod
    def transform_if_applicable(cls, v: Any):
        if isinstance(v, str):
            return [v]
        return v


class Concatenator(Component):
    def concat(self, config: dict) -> None:
        config: Config = Config(**config)

        def read_files() -> Generator[str, None, None]:
            for path in config.include:
                for file in glob(path, recursive=True):
                    with open(file, "r") as f:
                        yield f.read()

        concatenated = "".join(read_files())

        for out in config.destinations:
            with open(out, "w") as f:
                f.write(concatenated)
