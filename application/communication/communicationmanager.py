import requests
from application.communication import ResponseKeywordType
from lxml import etree

class OpenvasCommunicationWrapper():
    def __init__(self, host, port=16334):
        self.host = host
        self.port = port

    def is_alive(self):
        url = self.__make_url("_alive")
        response = requests.get(url=url)

        if self.__server_response_ok(response):
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

    def create_target(self, name, hosts, exclude_hosts, credential, port, port_list) -> str:
        pass

    def create_alert(self, name, credential, path, host, report_format, status) -> str:
        pass

    def create_credential(self, name, login, password) -> str:
        pass


    def __get_id_by_name(self, name, response):
        if self.__server_response_ok(response):
            json = response.json()
            data = json[ResponseKeywordType.DATA.value]
            for entry in data:
                if entry[ResponseKeywordType.NAME.value] == name:
                    return entry[ResponseKeywordType.ID.value]

        return None

    def __server_response_ok(self, response):
        if response.status_code in range (200, 300):
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
