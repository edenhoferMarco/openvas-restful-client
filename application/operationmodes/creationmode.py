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
                self.__create_task(task)

            return f"Host {self.host} finished!"
        except ConnectionError:
            return f"Host {self.host} unreachable! Thread aborting!"

    def __create_task(self, data) -> str:
        task_name = self.task_parser.get_task_name(data)
        task_id = self.communication.get_task_id_by_name(task_name)
        if task_id:
            print(f"Task with name {task_name} on host {self.host} already found! Task has ID {task_id}")
        else:
            print(f"Creating Task: {task_name} on host {self.host}")
            config_id = self.__get_config(data)
            if not config_id:
                return

            target_id = self.__get_or_create_target(data)
            if not target_id:
                return
            

            scanner_id = self.__get_scanner(data)
            if not scanner_id:
                return

            alert_ids = self.__get_or_create_alerts(data)
            for id in alert_ids:
                if not id:
                    return

            task_id = self.communication.create_task(task_name, config_id, target_id, scanner_id, alert_ids)
            if not task_id:
                return

            print(f"Created task {task_name} on host {self.host} with ID {task_id}")


    def __get_config(self, data) -> str:
        config_name = self.task_parser.get_config_name(data)

        config_id = self.communication.get_config_id_by_name(config_name)
        if config_id:
            print(f"Config with name {config_name} on host {self.host} has ID {config_id}")
            return config_id
        else:
            print(f"No config with name {config_name} on host {self.host} found")

            return None

    def __get_or_create_target(self, data) -> str:
        target_name = self.task_parser.get_target_name(data)

        target_id = self.communication.get_target_id_by_name(target_name)
        if target_id:
            print(f"Target with name {target_name} on host {self.host} has ID {target_id}")
            return target_id
        else:
            print(f"No target with name {target_name} on host {self.host} found")

            target_id = self.__create_target(data)
            return target_id

    def __create_target(self, data) -> str:
        name = self.task_parser.get_target_name(data)

        print(f"Creating target {name} on host {self.host}...")

        hosts = self.task_parser.get_target_hosts(data)
        exclude_hosts = self.task_parser.get_target_exclude_hosts(data)
        credential_data = self.task_parser.get_target_credential(data)
        credential = self.__get_or_create_credential(credential_data)
        if not credential:
            return None

        port = self.task_parser.get_target_port(data)
        port_list = self.__get_port_list(data)
        if not port_list:
            return None
        
        target_id = self.communication.create_target(name, hosts, exclude_hosts, credential, port, port_list)
        print(f"Created target {name} on host {self.host} with ID {target_id}")
        return target_id
        
    def __get_scanner(self, data) -> str:
        scanner_name = self.task_parser.get_scanner_name(data)
        scannerid = self.communication.get_scanner_id_by_name(scanner_name)
        if scannerid:
            print(f"Scanner with name {scanner_name} on host {self.host} has ID {scannerid}")
            return scannerid
        else:
            print(f"No scanner with name {scanner_name} on host {self.host} found")
            return None

    def __get_port_list(self, data):
        port_list_name = self.task_parser.get_target_port_list(data)
        port_list_id = self.communication.get_port_list_id_by_name(port_list_name)
        if port_list_id:
            print(f"Scanner with name {port_list_name} on host {self.host} has ID {port_list_id}")
            return port_list_id
        else:
            print(f"No scanner with name {port_list_name} on host {self.host} found")
            return None

    def __get_or_create_alerts(self, data) -> list:
        alerts = self.task_parser.get_alerts(data)
        alert_ids = list()

        for alert in alerts:
            alert_name = self.task_parser.get_alert_name(alert)
            alert_id = self.communication.get_alert_id_by_name(alert_name)

            if alert_id:
                print(f"Alert with name {alert_name} on host {self.host} has ID {alert_id}")
                alert_ids.append(alert_id)
            else:
                print(f"No alert with name {alert_name} on host {self.host} found")
                alert_id = self.__create_alert(alert)
                alert_ids.append(alert_id)

        return alert_ids

    def __create_alert(self, alert) -> str:
        name = self.task_parser.get_alert_name(alert)

        print(f"Creating alert {name} on host {self.host}...")
        
        credential_data = self.task_parser.get_alert_credential(alert)
        credential = self.__get_or_create_credential(credential_data)
        if not credential:
            return None

        path = self.task_parser.get_alert_path(alert)
        host = self.task_parser.get_alert_host(alert)
        report_format = self.__get_report_format(alert)
        if not report_format:
            return None

        status = self.task_parser.get_alert_status(alert)

        alert_id = self.communication.create_alert(name, credential, path, host, report_format, status)
        print(f"Created alert {name} on host {self.host} with ID {alert_id}")
        return alert_id

    def __get_report_format(self, alert) -> str:
        format_name = self.task_parser.get_alert_report_format(alert)
        format_id = self.communication.get_report_format_id_by_name(format_name)
        if format_id:
            print(f"Report format with name {format_name} on host {self.host} has ID {format_id}")
            return format_id
        else:
            print(f"No scanner with name {format_name} on host {self.host} found")
            return None


    def __get_or_create_credential(self, credential) -> str:
        credential_name = self.task_parser.get_credential_name(credential)
        credential_id = self.communication.get_credential_id_by_name(credential_name)

        if credential_id:
            print(f"Credential with name {credential_name} on host {self.host} has ID {credential_id}")
            return credential_id
        else:
            print(f"No credential with name {credential_name} on host {self.host} found")
            credential_id = self.__create_credential(credential)
            return credential_id

    def __create_credential(self, credential) -> str:
        name = self.task_parser.get_credential_name(credential)

        print(f"Creating credential {name} on host {self.host}...")

        login = self.task_parser.get_credential_login(credential)
        password = self.task_parser.get_credential_password(credential)

        credential_id = self.communication.create_credential(name, login, password)
        print(f"Created credential {name} on host {self.host} with ID {credential_id}")
        return credential_id
