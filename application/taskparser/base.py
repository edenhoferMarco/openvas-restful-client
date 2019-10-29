class TaskParserBase:

    def spawn_new_instance(self):
        pass

    def get_all_tasks(self) -> list:
        pass

    def get_task_or_none(self, taskname) -> dict:
        pass

    def get_task_name(self, data :dict) -> str:
        pass

    def get_create_params(self, data: dict) -> dict:
        pass

    def get_config_name(self, data: dict) -> str:
        pass

    def get_target(self, data):
        pass

    def get_target_name(self, data: dict):
        pass

    def get_target_hosts(self, data) -> list:
        pass

    def get_target_exclude_hosts(self, data) -> list:
        pass

    def get_target_credential(self, data) -> dict:
        pass

    def get_target_credential_name(self, data) -> str:
        pass

    def get_target_credential_login(self, data) -> str:
        pass

    def get_target_credential_password(self, data) -> str:
        pass

    def get_target_port(self, data) -> str:
        pass

    def get_target_port_list(self, data) -> list:
        pass

    def get_scanner_name(self, data) -> str:
        pass

    def get_alerts(self, data) -> list:
        pass

    def get_alert_name(self, alert) -> str:
        pass

    def get_alert_credential(self, alert) -> dict:
        pass

    def get_alert_credential_name(self, alert) -> str:
        pass

    def get_alert_credential_login(self, alert) -> str:
        pass

    def get_alert_credential_password(self, alert) -> str:
        pass

    def get_alert_path(self, alert) -> str:
        pass

    def get_alert_host(self, alert) -> str:
        pass

    def get_alert_report_format(self, alert) -> str:
        pass

    def get_alert_status(self, alert) -> str:
        pass

    def get_credential(self, data) -> dict:
        pass

    def get_credential_name(self, data) -> str:
        pass

    def get_credential_login(self, data) -> str:
        pass

    def get_credential_password(self, data) -> str:
        pass