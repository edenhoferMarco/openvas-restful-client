from application.configparser import ConfigParserBase
from application.taskparser import TaskParserBase, DefaultTaskParser

class DefaultConfigParser(ConfigParserBase):

    def attach_config_data(self, config_data):
        self.raw_config_data = config_data

    def get_hosts(self) -> list:
        return self.raw_config_data["hosts"]

    def get_tasks(self) -> list:
        return self.raw_config_data["tasks"]

    def create_task_parser(self) -> TaskParserBase:
        return DefaultTaskParser(self.get_tasks())

