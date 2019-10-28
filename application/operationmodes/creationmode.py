from application.operationmodes import OperationModeBase, WorkerBase
from application.taskparser import TaskParserBase

class CreationMode(OperationModeBase):
    def start_execution(self):
        print("START\t-\tCreation Mode")

    def attach_task_parser(self, task_parser: TaskParserBase):
        self.task_parser = task_parser

    def create_worker_for_host(self, host) -> WorkerBase:
        task_data = self.task_parser.get_all_tasks()
        task_parser = self.task_parser.spawn_new_instance()
        
        return CreationWorker(task_data, task_parser, host)

class CreationWorker(WorkerBase):
    def __init__(self, task_data: list, task_parser: TaskParserBase, host: str):
        self.task_data = task_data
        self.task_parser = task_parser
        self.host = host

    def execute(self):
        for task in self.task_data:
            print(f"Creating Task: {task['name']} on host {self.host}")

        return f"Host {self.host} finished!"