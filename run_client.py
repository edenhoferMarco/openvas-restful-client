import json
from json.decoder import JSONDecodeError
from jsonschema import validate, ValidationError
from application.operationmodes import CreationMode, ExecutionMode, OperationModeBase
import argparse
from application.configloader.implemented import ValidatingConfigLoader, ConfigValidationError
from application.configparser.implemented import DefaultConfigParser
from application.operation import OperationManager



class ArgumentHandler():
    __arg_config = "config"

    def __init__(self):
        self.args = self.__handle_arguments()

    def __handle_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(self.__arg_config, help="The config.json file you want to use for the client")
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-e", "--execute", help="Execute the specified Task and create all missing dependencies on the way", metavar="TASKNAME")
        group.add_argument("-c", "--create", help="Creates all in the conifg.json specified tasks and dependencies", action="store_true")
        
        return parser.parse_args()

    def get_operating_mode(self) -> OperationModeBase:
        args = self.__handle_arguments()
        if args.execute:
            return ExecutionMode()
        elif args.create:
            return CreationMode()
        else:
            return OperationModeBase()

    def get_config_path(self):
        return self.args.config

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