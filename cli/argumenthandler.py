import argparse
from application.operationmodes import OperationModeBase, ExecutionMode, CreationMode

class ArgumentHandler():
    __arg_config = "config"

    def __init__(self):
        self.args = self.__handle_arguments()

    def __handle_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(self.__arg_config, help="The config.json file you want to use for the client")
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-x", "--execute", help="Execute the specified Task and create all missing dependencies on the way", metavar="TASKNAME")
        group.add_argument("-c", "--create", help="Creates all in the conifg.json specified tasks and dependencies", action="store_true")
        
        return parser.parse_args()

    def get_operating_mode(self) -> OperationModeBase:
        args = self.__handle_arguments()
        if args.execute:
            return ExecutionMode(args.execute)
        elif args.create:
            return CreationMode()
        else:
            return OperationModeBase()

    def get_config_path(self):
        return self.args.config