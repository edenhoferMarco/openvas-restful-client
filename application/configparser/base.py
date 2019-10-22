from application.taskparser.base import TaskParserBase

class ConfigParserBase:
    def attach_config_data(self, config_data):
        pass

    def get_hosts(self) -> list:
        pass

    def create_task_parser(self) -> TaskParserBase:
        pass
