from application.taskparser.base import TaskParserBase
class OperationModeBase:
    def start_execution(self):
        pass

    def attach_task_parser(self, task_parser: TaskParserBase):
        pass