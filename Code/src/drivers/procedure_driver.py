import yaml


class Procedure:
    def Open(self, path: str):
        with open(path, 'r', encoding='utf-8') as output_file:
            config = yaml.safe_load(output_file)
            return config

    def Save(self, path: str, procedure: list):
        if not path.endswith(".yml"):
            path += ".yml"
        with open(path, 'w', encoding='utf-8') as output_file:
            yaml.dump(procedure, output_file)
