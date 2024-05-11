import json
from os.path import join, dirname
from ._model import Config


def generate():
    with open(join(dirname(__file__), "schema.json"), "w") as f:
        f.write(json.dumps(Config.model_json_schema(), indent=2))


if __name__ == "__main__":
    generate()
