from application.operationmodes import OperationModeBase, WorkerBase
from application.taskparser import TaskParserBase

class ValidationMode(OperationModeBase):
    def start_execution(self):
        print("START\t-\tCreation Mode")

    def attach_task_parser(self, task_parser: TaskParserBase):
        self.task_parser = task_parser

    def create_worker_for_host(self, host) -> WorkerBase:
        return ValidationWorker(host)

class ValidationWorker(WorkerBase):
    def __init__(self, host: str):
        self.host = host

    def execute(self):
        return f"Validation needs no execution on host {self.host}"