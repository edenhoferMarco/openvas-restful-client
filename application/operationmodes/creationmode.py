from application.operationmodes import OperationModeBase, WorkerBase
from application.taskparser import TaskParserBase
from application.communication import OpenvasCommunicationWrapper
from requests.exceptions import ConnectionError

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
        self.communication = OpenvasCommunicationWrapper(self.host)

    def execute(self):
        try:
            if not self.communication.is_alive():
                return f"Openvas server on host {self.host} unreachable! Thread aborting!"
        
            for task in self.task_data:
                print(f"Creating Task: {task['name']} on host {self.host}")

                scanner_name = "OpenVAS Default"

                scannerid = self.communication.get_scanner_id_by_name(scanner_name)
                if scannerid:
                    print(f"Scanner with name {scanner_name} on host {self.host} has ID {scannerid}")
                else:
                    print(f"No scanner with name {scanner_name} on host {self.host} found")

                config_name = "Discovery"

                config_id = self.communication.get_config_id_by_name(config_name)
                if scannerid:
                    print(f"Config with name {config_name} on host {self.host} has ID {config_id}")
                else:
                    print(f"No config with name {config_name} on host {self.host} found")



            return f"Host {self.host} finished!"
        except ConnectionError:
            return f"Host {self.host} unreachable! Thread aborting!"
        

        


    