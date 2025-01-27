import yaml


class ProcedureFile:
    def Open(self, path: str):
        try:
            with open(path, 'r', encoding='utf-8') as input_file:
                config = yaml.safe_load(input_file)
                return config
        except FileNotFoundError as e:
            return None

    def Save(self, path: str, procedure: list):
        if not path.endswith(".yml"):
            path += ".yml"
        with open(path, 'w', encoding='utf-8') as output_file:
            yaml.dump(procedure, output_file)
