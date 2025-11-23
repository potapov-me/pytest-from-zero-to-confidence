import requests


class RemoteService:
    """Клиент для удаленного API задач"""

    def __init__(self, base_url):
        self.base_url = base_url

    def sync_task(self, task):
        response = requests.post(f"{self.base_url}/tasks/sync", json=task, timeout=10)
        response.raise_for_status()

    def log(self, event, **data):
        requests.post(
            f"{self.base_url}/logs", json={"event": event, "data": data}, timeout=5
        )
