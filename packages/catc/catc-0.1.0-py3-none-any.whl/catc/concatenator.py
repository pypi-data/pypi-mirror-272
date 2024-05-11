from os import makedirs
from os.path import dirname, join
from glob import glob
from typing import Generator
from .component import Component
from .config import Config


class Concatenator(Component):
    def concat(self, cwd: str, config: Config) -> None:
        def read_files() -> Generator[str, None, None]:
            for path in config.files:
                for file in glob(join(cwd, path), recursive=True):
                    with open(file, "r") as f:
                        yield f.read()

        concatenated = config.separator.join(read_files())

        if config.destinations is None:
            self.logger.info(concatenated)

        for out in config.destinations:
            out_path = join(cwd, out)
            makedirs(dirname(out_path), exist_ok=True)
            with open(out_path, "w") as f:
                f.write(concatenated)
