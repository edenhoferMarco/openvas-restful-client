from application.operationmodes import OperationModeBase
from application.taskparser import TaskParserBase

class ExecutionMode(OperationModeBase):
    def __init__(self, task_to_execute):
        self.task_to_execute = task_to_execute

    def attach_task_parser(self, task_parser: TaskParserBase):
        self.task_parser = task_parser

    def create_worker_for_host(self, host):
        task_data = self.task_parser.get_task_or_none(self.task_to_execute)
        task_parser = self.task_parser.spawn_new_instance()
        return ExecutionWorker(task_data, task_parser, host)
    

class ExecutionWorker:
    def __init__(self, task_data: list, task_parser: TaskParserBase, host: str):
        self.task_data = task_data
        self.task_parser = task_parser
        self.host = host

    def execute(self):
        if self.task_data != None:
            print(f"START\t-\tExecution Mode with task: {self.task_data['name']} on host: {self.host}")
        else:
            print("Specified task was not found in config.json")

        return f"Host {self.host} finished!"
