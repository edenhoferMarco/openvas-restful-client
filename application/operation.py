from application.configloader.base import ConfigLoaderBase
from application.configparser.base import ConfigParserBase
from application.taskparser.base import TaskParserBase
from application.operationmodes import OperationModeBase


class OperationManager:
    def __init__(self, config_loader: ConfigLoaderBase, operation_mode: OperationModeBase, config_parser: ConfigParserBase):
        config = config_loader.load_config()
        self.config_parser = config_parser
        config_parser.attach_config_data(config)
        task_parser = config_parser.create_task_parser()

        self.operation_mode = operation_mode
        self.operation_mode.attach_task_parser(task_parser)
        
    def start_operation(self):
        hosts = self.config_parser.get_hosts()
        self.operation_mode.start_execution()
        

    
        