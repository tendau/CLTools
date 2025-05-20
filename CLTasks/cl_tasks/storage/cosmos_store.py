from cl_tasks.storage.base import TaskStore

class CosmosTaskStore(TaskStore):
    def add_task(self, title: str, position: int = None):
        raise NotImplementedError("Cosmos not yet implemented")

    def list_tasks(self):
        raise NotImplementedError("Cosmos not yet implemented")

    def complete_task(self, task_id: int):
        raise NotImplementedError("Cosmos not yet implemented")
        
    def delete_task(self, task_id: int):
        raise NotImplementedError("Cosmos not yet implemented")
        
    def reorder_task(self, task_id: int, new_position: int):
        raise NotImplementedError("Cosmos not yet implemented")
