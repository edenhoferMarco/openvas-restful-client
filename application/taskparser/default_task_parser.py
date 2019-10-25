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