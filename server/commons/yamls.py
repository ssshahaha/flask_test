import yaml

from threading import Lock


class YamlHelper:
    @staticmethod
    def to_dict(file_path):
        with open(file_path, 'r') as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    @staticmethod
    def to_save(file_path, dict_data):
        with Lock() as lock:
            with open(file_path, 'w', encoding='utf-8') as w_f:
                yaml.dump(dict_data, w_f)
