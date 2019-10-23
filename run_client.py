import json
from json.decoder import JSONDecodeError
from jsonschema import validate, ValidationError
from cli import ArgumentHandler
from application.operationmodes import CreationMode, ExecutionMode, OperationModeBase
from application.configloader import ValidatingConfigLoader, ConfigValidationError
from application.configparser import DefaultConfigParser
from application.operation import OperationManager


def run():
    try:
        argument_handler = ArgumentHandler()
        operation_mode = argument_handler.get_operating_mode()
        config_path = argument_handler.get_config_path()
        config_loader = ValidatingConfigLoader(config_path)
        config_parser = DefaultConfigParser()

        operator = OperationManager(config_loader, operation_mode, config_parser)
        operator.start_operation()
    except ConfigValidationError as config_error:
        config_error.print()


if __name__ == "__main__":
    # execute only if run as a script
    run()