import requests
from application.communication import ResponseKeywordType, RequestKeywordType, RequestMethodDataType, RequestEventDataType
from lxml import etree

class OpenvasCommunicationWrapper():
    def __init__(self, host, port=16334):
        self.host = host
        self.port = port

    def is_alive(self):
        url = self.__make_url("_alive")
        response = requests.get(url=url)

        if response:
            response_xml = etree.fromstring(response.text)
            openvas_status = int(self.__extract_status_from_xml(response_xml))
            openvas_version = self.__extract_version_from_xml(response_xml)
            if openvas_status == 200:
                print(f"Openvas instance on host {self.host}:{self.port} reachable.\n\tOpenVAS-Version: {openvas_version}")
                return True

        return False

    def get_task_id_by_name(self, name):
        url = self.__make_url_with_param(path="_tasks", param=name)
        response = requests.get(url=url)

        return self.__get_id_by_name(name, response)

    def get_scanner_id_by_name(self, name):
        url = self.__make_url_with_param(path="_scanners", param=name)
        response = requests.get(url=url)

        return self.__get_id_by_name(name, response)

    def get_config_id_by_name(self, name):
        url = self.__make_url_with_param(path="_configs", param=name)
        response = requests.get(url=url)

        return self.__get_id_by_name(name, response)

    def get_target_id_by_name(self, name) -> str:
        url = self.__make_url_with_param(path="_targets", param=name)
        response = requests.get(url=url)

        return self.__get_id_by_name(name, response)

    def get_alert_id_by_name(self, name) -> str:
        url = self.__make_url_with_param(path="_alerts", param=name)
        response = requests.get(url=url)

        return self.__get_id_by_name(name, response)

    def get_credential_id_by_name(self, name) -> str:
        url = self.__make_url_with_param(path="_credentials", param=name)
        response = requests.get(url=url)

        return self.__get_id_by_name(name, response)

    def get_report_format_id_by_name(self, name) -> str:
        url = self.__make_url_with_param(path="_reportformats", param=name)
        response = requests.get(url=url)

        return self.__get_id_by_name(name, response)

    def get_port_list_id_by_name(self, name) -> str:
        url = self.__make_url_with_param(path="_portlists", param=name)
        response = requests.get(url=url)

        return self.__get_id_by_name(name, response)

    def create_target(self, name, hosts: list, exclude_hosts: list, credential, port, port_list) -> str:
        url = self.__make_url(path="_create/target")
        body = {
            RequestKeywordType.NAME.value : name,
            RequestKeywordType.HOSTS.value : hosts,
            RequestKeywordType.EXCLUDE_HOSTS.value : exclude_hosts,
            RequestKeywordType.SSH_CREDENTIAL_ID.value : credential,
            RequestKeywordType.SSH_CREDENTIAIL_PORT.value : port,
            RequestKeywordType.PORT_LIST_ID.value : port_list
        }
        response = requests.post(url=url, json=body)

        return self.__get_id_from_created_object(response)

    def create_task(self, name, config, target, scanner, alerts:list) -> str:
        url = self.__make_url(path="_create/task")
        body = {
            RequestKeywordType.NAME.value : name,
            RequestKeywordType.CONFIG_ID.value : config,
            RequestKeywordType.TARGET_ID.value : target,
            RequestKeywordType.SCANNER_ID.value : scanner,
            RequestKeywordType.ALERT_IDS.value : alerts
        }

        response = requests.post(url=url, json=body)

        return self.__get_id_from_created_object(response)

    def create_alert(self, name, credential, path, host, report_format, status) -> str:
        url = self.__make_url(path="_create/alert/scp")
        body = {
            RequestKeywordType.NAME.value : name,
            RequestMethodDataType.SCP_CREDENTIAL.value : credential,
            RequestMethodDataType.SCP_PATH.value : path,
            RequestMethodDataType.SCP_HOST.value : host,
            RequestMethodDataType.SCP_REPORT_FORMAT.value : report_format,
            RequestEventDataType.STATUS.value : status
        }
        response = requests.post(url=url, json=body)

        return self.__get_id_from_created_object(response)

    def create_credential(self, name, login, password) -> str:
        url = self.__make_url(path="_create/username_password_credential")
        body = {
            RequestKeywordType.NAME.value : name,
            RequestKeywordType.LOGIN.value : login,
            RequestKeywordType.PASSWORD.value : password
        }
        response = requests.post(url=url, json=body)

        return self.__get_id_from_created_object(response)

    def __get_id_by_name(self, name, response):
        if response:
            response_json = response.json()
            if self.__openvas_response_ok(response_json):
                data = response_json[ResponseKeywordType.DATA.value]
                for entry in data:
                    if entry[ResponseKeywordType.NAME.value] == name:
                        return entry[ResponseKeywordType.ID.value]

        return None

    def __get_id_from_created_object(self, response):
        if response:
            response_json = response.json()
            if self.__openvas_response_ok(response_json):
                return response_json[ResponseKeywordType.ID.value]
        
        return None

    def __openvas_response_ok(self, response_json):
        openvas_status = int(response_json[ResponseKeywordType.STATUS.value])
        if openvas_status in range (200, 400):
            return True
        else:
            return False

    def __make_url(self, path):
        return f"http://{self.host}:{self.port}/{path}"

    def __make_url_with_param(self, path, param):
        return f"http://{self.host}:{self.port}/{path}/{param}"

    def __extract_status_from_xml(self, xml_root_element):
        return xml_root_element.get(ResponseKeywordType.STATUS.value)

    def __extract_version_from_xml(self, xml_root_element):
        version = None

        for child in xml_root_element:
            if child.tag == "version":
                version = child.text
        
        return version
