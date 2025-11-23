import os
import pytest
from src.app import TodoApp
from src.cache import FileCache


class TestTodoAppHappyPath:
    """Когда всё работает"""

    def test_add_task(self, app):
        task_id = app.add_task("Learn integration testing")
        tasks = app.list_tasks()
        assert len(tasks) == 1
        assert tasks[0]["text"] == "Learn integration testing"
        assert tasks[0]["done"] is False

    def test_complete_task(self, app_with_sample_tasks):
        app, task_ids = app_with_sample_tasks
        task = app.complete_task(task_ids[0])
        assert task["done"] is True
        tasks = app.list_tasks()
        assert tasks[0]["done"] is True


class TestTodoAppErrorHandling:
    """Обработка ошибок"""

    def test_cache_degradation(self, temp_storage, spy_remote):
        cache = FileCache(temp_storage)
        app = TodoApp(cache, spy_remote)
        task_id = app.add_task("Important task")

        os.chmod(temp_storage, 0o000)  # Ломаем доступ к кешу
        try:
            task = app.complete_task(task_id)
        finally:
            os.chmod(temp_storage, 0o755)
        assert task["done"] is True
        assert spy_remote.assert_log_contains("cache_unavailable")

    def test_remote_unavailable(self, working_cache, broken_remote):
        app = TodoApp(working_cache, broken_remote)
        task_id = app.add_task("Offline task")
        assert task_id is not None
        tasks = app.list_tasks()
        assert len(tasks) == 1

    def test_complete_missing_task(self, app):
        with pytest.raises(ValueError, match="Task unknown not found"):
            app.complete_task("unknown")


class TestTodoAppEdgeCases:
    """Граничные случаи"""

    @pytest.mark.parametrize("text", [
        "  task with spaces  ",
        "very-long-task-" * 10,
        "task with 🎉 emoji",
        "",  # Пустая задача
    ])
    def test_add_various_tasks(self, app, text):
        if not text.strip():
            with pytest.raises(ValueError):
                app.add_task(text)
        else:
            task_id = app.add_task(text)
            assert task_id is not None
            tasks = app.list_tasks()
            assert tasks[0]["text"] == text.strip()
