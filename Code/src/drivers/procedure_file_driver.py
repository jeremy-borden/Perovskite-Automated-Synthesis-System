import yaml
import logging

class ProcedureFile:
    def Open(self, path: str):
        print("DEBUG: path is", path, type(path))
        try:
            with open(path, 'r', encoding='utf-8') as input_file:
                config = yaml.safe_load(input_file)
                return config
        except FileNotFoundError as e:
            return None

    def Save(self, path: str, procedure):
        if not path.endswith(".yml"):
            path += ".yml"
        with open(path, 'w', encoding='utf-8') as output_file:
            yaml.dump(procedure, output_file, default_flow_style=None, Dumper=ProcedureDumper)

class ProcedureDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(ProcedureDumper, self).increase_indent(flow, False)
    
