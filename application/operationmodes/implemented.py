from application.operationmodes import OperationModeBase

class CreationMode(OperationModeBase):
    def start_execution(self):
        print("START\t-\tCreation Mode")

    def attach_task_data(self, task_data: dict):
        self.task_data = task_data

class ExecutionMode(OperationModeBase):
    def __init__(self, task_to_execute):
        self.task_to_execute = task_to_execute

    def start_execution(self):
        print(f"START\t-\tExecution Mode with task: {self.task_to_execute}")

    def attach_task_data(self, task_data: dict):
        self.attach_task_data = task_data