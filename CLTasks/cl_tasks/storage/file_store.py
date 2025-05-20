import time
import json
import os
from cl_tasks.storage.base import TaskStore

FILE_PATH = os.path.expanduser("~/.taskcli_tasks.json")

class FileTaskStore(TaskStore):
    def __init__(self):
        if not os.path.exists(FILE_PATH):
            with open(FILE_PATH, "w") as f:
                json.dump([], f)

    def _load_tasks(self):
        with open(FILE_PATH) as f:
            return json.load(f)

    def _save_tasks(self, tasks):
        with open(FILE_PATH, "w") as f:
            json.dump(tasks, f, indent=2)

    def add_task(self, title: str, position: int = None):
        tasks = self._load_tasks()
        new_id = len(tasks) + 1
        task = {"id": new_id, "title": title, "completed": False}
        
        # If position is specified, insert at that position and reorder
        if position is not None and position > 0:
            # If position is greater than the list length, just append
            if position > len(tasks) + 1:
                tasks.append(task)
            else:
                # Insert at the specified position
                tasks.insert(position - 1, task)
                
                # Reorder IDs
                for i, t in enumerate(tasks):
                    t["id"] = i + 1
        else:
            tasks.append(task)
            
        self._save_tasks(tasks)
        return task
    
    def start_task(self, task_id: int):
        tasks = self._load_tasks()
        for task in tasks:
            if task["id"] == task_id:
                task["start_time"] = time.time()
                self._save_tasks(tasks)
                return True
        return False

    def list_tasks(self):
        return self._load_tasks()

    def complete_task(self, task_id: int):
        tasks = self._load_tasks()
        for task in tasks:
            if task["id"] == task_id:
                task["completed"] = True
                task["end_time"] = time.time()
                duration = task["end_time"] - task["start_time"] if "start_time" in task else 0
                # convert duration to a human-readable format
                task["duration"] = time.strftime("%H:%M:%S", time.gmtime(duration))
                self._save_tasks(tasks)
                return True
        return False
    
    def delete_task(self, task_id: int):
        deleted_task = False
        tasks = self._load_tasks()
        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                del tasks[i]
                deleted_task = True
                break  # Add break to exit loop after deletion

        # reorder the task IDs after deletion
        if deleted_task:
            for i, task in enumerate(tasks):
                task["id"] = i + 1
            self._save_tasks(tasks)
        
        return deleted_task
    
    def reorder_task(self, task_id: int, new_position: int):
        """Reorder a task to a new position.
        
        Args:
            task_id: ID of the task to reorder
            new_position: New position to move the task to (1-based)
            
        Returns:
            bool: Whether the reordering was successful
        """
        tasks = self._load_tasks()
        
        # Find the task with the given ID
        task_to_move = None
        task_index = None
        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                task_to_move = task
                task_index = i
                break
        
        if task_to_move is None:
            return False  # Task not found
        
        # Remove the task from the current position
        tasks.pop(task_index)
        
        # If new position is greater than list length, append to the end
        if new_position > len(tasks) + 1:
            tasks.append(task_to_move)
        else:
            # Insert at the new position (adjust for 0-based index)
            tasks.insert(new_position - 1, task_to_move)
        
        # Reorder all task IDs to maintain consistency
        for i, task in enumerate(tasks):
            task["id"] = i + 1
        
        self._save_tasks(tasks)
        return True
    
    def pause_task(self, task_id: int):
        """Pause a task and record the paused duration.

        Args:
            task_id: The ID of the task to pause

        Returns:
            bool: True if the task was successfully paused, False otherwise
        """
        tasks = self._load_tasks()
        for task in tasks:
            if task["id"] == task_id:
                if "start_time" not in task or task.get("completed", False):
                    # Task is not running or already completed
                    return False

                # Calculate the elapsed time since the task was started
                elapsed_time = time.time() - task["start_time"]
                task["paused_duration"] = task.get("paused_duration", 0) + elapsed_time

                # Remove the start_time to indicate the task is paused
                del task["start_time"]
                self._save_tasks(tasks)
                return True
        return False
