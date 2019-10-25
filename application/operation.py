from application.configloader.base import ConfigLoaderBase
from application.configparser.base import ConfigParserBase
from application.taskparser.base import TaskParserBase
from application.operationmodes import OperationModeBase, ExecutionWorker
from concurrent.futures import ThreadPoolExecutor, wait


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
        workers = self.__create_worker_per_host(hosts)
        futures = self.__start_workers(workers)

        # wait for completion
        wait(futures)
        for future in futures:
            print(future.result())

    def __create_worker_per_host(self, hosts):
        workers = list()
        for host in hosts:
            print(host)
            workers.append(self.operation_mode.create_worker_for_host(host))
            
        return workers

    def __start_workers(self, workers: list):
        futures = list()
        with ThreadPoolExecutor() as executor:
            for worker in workers:
                futures.append(executor.submit(worker.execute))

        return futures

        