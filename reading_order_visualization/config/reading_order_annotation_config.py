import json

class ReadingOrderAnnotationConfig:

    def __init__(self):
        self._config_file_name = ("reading_order_visualization/"
                                  "config/config.json")
        self._config_data = self._load_config_file()

    def _load_config_file(self):
        file = open(self._config_file_name)
        config_data = json.load(file)
        file.close()
        return config_data

    def is_generated_latex_dataset(self):
        return self._config_data["is-generated-latex-dataset"]

    def get_data_path(self):
        return self._config_data["data-path"]

    def get_annotated_data_path(self):
        return self._config_data["annotated-data-path"]
