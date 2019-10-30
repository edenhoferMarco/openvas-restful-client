from application.taskparser import TaskParserBase
import copy

class DefaultTaskParser(TaskParserBase):
    def __init__(self, task_list):
        self.tasks = task_list

    def spawn_new_instance(self) -> TaskParserBase:
        return DefaultTaskParser(self.tasks)

    def get_all_tasks(self) -> list:
        return copy.deepcopy(self.tasks)

    def get_task_or_none(self, taskname: str) -> dict:
        for task in self.tasks:
            if task["name"] == taskname:
                return copy.deepcopy(task)

        return None

    def get_task_name(self, data :dict) -> str:
        return data["name"]

    def get_create_params(self, data: dict) -> dict:
        return data["create_params"]

    def get_config_name(self, data: dict) -> str:
        create_params = self.get_create_params(data)
        return create_params["config"]

    def get_target(self, data):
        create_params = self.get_create_params(data)
        return create_params["target"]

    def get_target_name(self, data: dict):
        target = self.get_target(data)
        return target["name"]

    def get_target_hosts(self, data) -> list:
        target = self.get_target(data)
        return target["hosts"]

    def get_target_exclude_hosts(self, data) -> list:
        target = self.get_target(data)
        return target["exclude_hosts"]

    def get_target_credential(self, data) -> dict:
        target = self.get_target(data)
        return self.get_credential(target)

    def get_target_credential_name(self, data) -> str:
        credential = self.get_target_credential(data)
        return self.get_credential_name(credential)

    def get_target_credential_login(self, data) -> str:
        credential = self.get_target_credential(data)
        return self.get_credential_login(credential)

    def get_target_credential_password(self, data) -> str:
        credential = self.get_target_credential(data)
        return self.get_credential_password(credential)

    def get_target_port(self, data) -> str:
        target = self.get_target(data)
        return target["port"]

    def get_target_port_list(self, data) -> str:
        target = self.get_target(data)
        return target["port_list"]

    def get_scanner_name(self, data) -> str:
        create_params = self.get_create_params(data)
        return create_params["scanner"]

    def get_alerts(self, data) -> list:
        create_params = self.get_create_params(data)
        return create_params["alerts"]

    def get_alert_name(self, alert) -> str:
        return alert["name"]

    def get_alert_credential(self, alert) -> dict:
        return self.get_credential(alert)

    def get_alert_credential_name(self, alert) -> str:
        credential = self.get_alert_credential(alert)
        return self.get_credential_name(credential)

    def get_alert_credential_login(self, alert) -> str:
        credential = self.get_alert_credential(alert)
        return self.get_credential_login(credential)

    def get_alert_credential_password(self, alert) -> str:
        credential = self.get_alert_credential(alert)
        return self.get_credential_password(credential)

    def get_alert_path(self, alert) -> str:
        return alert["path"]

    def get_alert_host(self, alert) -> str:
        return alert["host"]

    def get_alert_report_format(self, alert) -> str:
        return alert["report_format"]

    def get_alert_status(self, alert) -> str:
        return alert["status"]

    def get_credential(self, data) -> dict:
        return data["credential"]

    def get_credential_name(self, credential) -> str:
        return credential["name"]

    def get_credential_login(self, credential) -> str:
        return credential["login"]

    def get_credential_password(self, credential) -> str:
        return credential["password"]
