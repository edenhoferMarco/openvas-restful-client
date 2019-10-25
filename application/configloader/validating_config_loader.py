from application.configloader import ConfigLoaderBase
from application.configloader.errors import ConfigValidationError
from jsonschema import validate, ValidationError
from json.decoder import JSONDecodeError
import json

class ValidatingConfigLoader(ConfigLoaderBase):

    def __init__(self, config_path, schema_path="schemas/openvas_config.schema"):
        self.config_path = config_path
        self.schema_path = schema_path

    def load_config(self) -> dict:
        try:
            schema = self.__open_json(self.schema_path)
            config = self.__open_json(self.config_path)
            validate(instance=config, schema=schema)
            print(f"{self.config_path} is a valid configuration.")
            return config
        except ValidationError as validation_error:
            msg = "\nYour config.json is invalid, for further information, see the error message above."
            raise ConfigValidationError(msg, validation_error)
        except JSONDecodeError as json_error:
            msg = "\nYour config.json is invalid, for further information, see the error message above."
            raise ConfigValidationError(msg, json_error)
        except IOError as io_error:
            msg = "Your config.json is either not readable, or the specified path is incorrect."
            raise ConfigValidationError(msg, io_error)
            

    def __open_json(self, json_path) -> dict:
        json_data = None

        with open(json_path, 'r') as json_file:
            json_data = json.load(json_file)

        return json_data