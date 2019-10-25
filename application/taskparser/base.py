class TaskParserBase:

    def spawn_new_instance(self):
        pass

    def get_all_tasks(self) -> list:
        pass

    def get_task_or_none(self, taskname) -> dict:
        pass