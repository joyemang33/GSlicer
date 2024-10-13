import json


class Config:
    """Utility class for loading the configuration file.
    """
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self):
        with open(self.config_file) as f:
            config = json.load(f)
        return config

    def get_config(self):
        return self.config
    
    def get_algorithms(self, oracle=None, directed=None, paralleledge=None):
        result = []
        if oracle is not None:
            result = [item for item in self.config if item["Oracle"] == oracle]
        else:
            result = self.config
        if directed is not None:
            result = [item for item in result if item["Directed"] == directed or item["Directed"] == ""]
        if paralleledge is not None:
            result = [item for item in result if item["MultiEdges"] == paralleledge or item["MultiEdges"] == ""]
        return result