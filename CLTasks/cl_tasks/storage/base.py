from abc import ABC, abstractmethod

class TaskStore(ABC):
    @abstractmethod
    def add_task(self, title: str, position: int = None):
        pass

    @abstractmethod
    def start_task(self, task_id: int):
        pass
        
    @abstractmethod
    def pause_task(self, task_id: int):
        pass

    @abstractmethod
    def list_tasks(self):
        pass

    @abstractmethod
    def complete_task(self, task_id: int):
        pass

    @abstractmethod
    def delete_task(self, task_id: int):
        pass
        
    @abstractmethod
    def reorder_task(self, task_id: int, new_position: int):
        pass