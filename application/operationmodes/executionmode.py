from application.operationmodes import OperationModeBase, WorkerBase
from application.taskparser import TaskParserBase
from application.communication import OpenvasCommunicationWrapper
from application.operationmodes import CreationWorker

class ExecutionMode(OperationModeBase):
    def __init__(self, task_to_execute):
        self.task_to_execute = task_to_execute

    def attach_task_parser(self, task_parser: TaskParserBase):
        self.task_parser = task_parser

    def create_worker_for_host(self, host) -> WorkerBase:
        task_data = self.task_parser.get_task_or_none(self.task_to_execute)
        task_parser = self.task_parser.spawn_new_instance()
        
        return ExecutionWorker(task_data, task_parser, host)
    

class ExecutionWorker(WorkerBase):
    def __init__(self, task_data: list, task_parser: TaskParserBase, host: str):
        self.task_data = task_data
        self.task_parser = task_parser
        self.host = host
        self.communication = OpenvasCommunicationWrapper(self.host)

    def execute(self):
        if self.task_data != None:
            name = self.task_parser.get_task_name(self.task_data)
            print(f"START\t-\tExecution Mode with task: {name} on host: {self.host}")

            try:
                if not self.communication.is_alive():
                    return f"Openvas server on host {self.host} unreachable! Thread aborting!"
            
                task_id = self.communication.get_task_id_by_name(name)

                # if no task is found on the openvas server, switch to creation mode
                if not task_id:
                    task_list = list()
                    task_list.append(self.task_data)
                    creation_worker = CreationWorker(task_list, self.task_parser, self.host)
                    creation_worker.execute()

                    task_id = task_id = self.communication.get_task_id_by_name(name)
                    if not task_id:
                        print(f"Could not create task {name} on host {self.host}. Thread Aborting!")
                        return

                self.communication.start_task(task_id)
                print(f"Started task {name} on {self.host}")
            except ConnectionError:
                return f"Host {self.host} unreachable! Thread aborting!"

        else:
            print("Specified task was not found in config.json")

        return f"Host {self.host} finished!"
