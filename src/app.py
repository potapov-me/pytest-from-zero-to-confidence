import uuid
from typing import Dict, Any


class TodoApp:
    """Приложение для задач с кешем и удаленной синхронизацией"""

    def __init__(self, cache, remote):
        self.cache = cache
        self.remote = remote
        self.tasks: Dict[str, Dict] = {}

    def add_task(self, text: str) -> str:
        task_id = str(uuid.uuid4())
        task = {"id": task_id, "text": text.strip(), "done": False}
        if not task["text"]:
            raise ValueError("Task text is empty")

        self.tasks[task_id] = task
        self.cache.set(f"task_{task_id}", task)
        try:
            self.remote.sync_task(task)
        except Exception:
            # Удаленная синхронизация не критична для сохранения задачи
            pass
        return task_id

    def complete_task(self, task_id: str) -> Dict[str, Any]:
        # 🛡️ Кеш может быть недоступен
        try:
            self.cache.invalidate(f"task_{task_id}")
        except Exception:
            self.remote.log("cache_unavailable", task_id=task_id)

        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        task["done"] = True
        try:
            self.remote.sync_task(task)
        except Exception:
            pass
        return task

    def list_tasks(self) -> list:
        return list(self.tasks.values())
