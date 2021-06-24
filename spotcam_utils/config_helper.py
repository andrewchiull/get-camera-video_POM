from spotcam_utils.file_util import read_yaml_file

class ConfigHelper:

    def __init__(self, config_path):
        self.config = self._read_config(config_path)

    @staticmethod
    def _read_config(config_path):
        return read_yaml_file(config_path)

    def get_username(self):
        return self.config["username"]

    def get_password(self):
        return self.config["password"]

    # for FTP
    def get_FTPIP(self):
        return self.config["FTPIP"]

    def get_FTPPORT(self):
        return self.config["FTPPORT"]

    def get_USERNAME(self):
        return self.config["USERNAME"]

    def get_USERPWD(self):
        return self.config["USERPWD"]

    def get_FTPDIR(self):
        return self.config["FTPDIR"]