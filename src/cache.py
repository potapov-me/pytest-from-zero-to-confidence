import json


class CacheError(Exception):
    pass


class FileCache:
    """Простой кеш на файловой системе"""

    def __init__(self, storage_path):
        self.storage_path = storage_path

    def set(self, key, value):
        try:
            file_path = self.storage_path / f"{key}.json"
            file_path.write_text(json.dumps(value))
        except Exception as e:
            raise CacheError(f"Failed to set cache: {e}")

    def invalidate(self, key):
        try:
            file_path = self.storage_path / f"{key}.json"
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            raise CacheError(f"Failed to invalidate cache: {e}")
