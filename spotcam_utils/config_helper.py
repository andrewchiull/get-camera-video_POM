from spotcam_utils.file_util import read_yaml_file

class ConfigHelper:

    def __init__(self, config_path):
        self.config = self._read_config(config_path)

    @staticmethod
    def _read_config(config_path):
        return read_yaml_file(config_path)

    # def get_firefix_binary_path(self):
    #     return self.config["firefox_binary"]

    def get_username(self):
        return self.config["username"]

    def get_password(self):
        return self.config["password"]