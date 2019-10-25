from application.taskparser.base import TaskParserBase
class OperationModeBase:

    def attach_task_parser(self, task_parser: TaskParserBase):
        pass

    def create_worker_for_host(self, host):
        pass