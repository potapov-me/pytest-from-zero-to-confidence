import json
from pathlib import Path


class CacheError(Exception):
    pass


class FileCache:
    """Простой кеш на файловой системе"""

    def __init__(self, storage_path):
        self.storage_path = Path(storage_path)
        # Создаем каталог заранее, чтобы запись не падала из-за отсутствия папок
        self.storage_path.mkdir(parents=True, exist_ok=True)

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
