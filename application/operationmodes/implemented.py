from application.operationmodes import OperationModeBase

class CreationMode(OperationModeBase):
    def start_execution(self):
        print("START \t-\tCreation Mode")

    def attach_task_data(self, task_data: dict):
        self.task_data = task_data

class ExecutionMode(OperationModeBase):
    def start_execution(self):
        pass

    def attach_task_data(self, task_data: dict):
        self.attach_task_data = task_data