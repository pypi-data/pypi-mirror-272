import configparser
from abc import ABC, abstractmethod

from common.customException import NodeNameNotCorrectError
from common.setting import FilePath


class CaseSensitiveConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr


class BaseConfig(ABC):
    def __init__(self, file_path=None):
        if file_path is None:
            self.__file_path = FilePath.CONFIG
        else:
            self.__file_path = file_path

        self.conf = CaseSensitiveConfigParser()
        try:
            self.conf.read(self.__file_path, encoding="utf-8")
        except Exception as e:
            print(e)

    def get_section_for_data(self, section, option):
        '''

        :param section: init头部值
        :param option: 选项值key
        :return:
        '''
        try:
            return self.conf.get(section, option)
        except Exception as e:
            print(e)

    @abstractmethod
    def get_api_host(self):
        pass

    def write_section_for_data(self, section, option, value):
        self.conf[section] = {}
        self.conf[section][option] = value
        with open(file=self.__file_path, mode="w") as f:
            self.conf.write(f)
        return self.get_section_for_data(section, option)

    def modify_api_host(self, value):
        self.write_section_for_data("api_env", "host", value)

    def modify_section_for_data(self, section, opetion, value):
        self.conf.set(section, opetion, value)
        with open(file=self.__file_path, mode="w") as f:
            self.conf.write(f)


class OperationConfig(BaseConfig):
    def get_api_host(self):
        env = self.get_section_for_data("api_env", "env")
        if env == "dev":
            return self.get_section_for_data("poms-dev", "host")
        elif env == "fat":
            return self.get_section_for_data("poms-fat", "host")
        else:
            raise NodeNameNotCorrectError


class XXLJobConfig(BaseConfig):
    def __init__(self):
        super().__init__(FilePath.XXL_JOB_CONFIG)
        self.env = OperationConfig().get_section_for_data("api_env", "env")
        if self.env == "dev":
            self.section = "xxl_job_dev"
        elif self.env == "fat":
            self.section = "xxl_job_fat"

    def get_api_host(self):
        return self.get_section_for_data(self.section, "host")


class OpenApiConfig(BaseConfig):
    def __init__(self):
        super().__init__(FilePath.OPENAPI_CONFIG)
        self.env = OperationConfig().get_section_for_data("api_env", "env")
        if self.env == "dev":
            self.section = "openApi_dev"
        elif self.env == "fat":
            self.section = "openApi_fat"

    def get_api_host(self):
        return self.get_section_for_data(self.section, "host")

    def get_access_key(self, key):
        return self.get_section_for_data(self.section, key)
