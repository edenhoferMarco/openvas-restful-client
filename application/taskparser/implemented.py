from application.taskparser import TaskParserBase

class DefaultTaskParser(TaskParserBase):
    def __init__(self, task_list):
        self.tasks = task_list

    def get_task_or_none(self, taskname: str) -> dict:
        for task in self.tasks:
            if task["name"] == taskname:
                return task

        return None