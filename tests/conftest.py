import pytest
from unittest.mock import Mock
from src.app import TodoApp
from src.cache import FileCache


@pytest.fixture
def temp_storage(tmp_path):
    return tmp_path / "cache"


@pytest.fixture
def working_cache(temp_storage):
    return FileCache(temp_storage)


@pytest.fixture
def broken_cache():
    cache = Mock()
    cache.set.side_effect = Exception("Cache storage failed")
    cache.invalidate.side_effect = Exception("Cache invalidation failed")
    return cache


@pytest.fixture
def fake_remote():
    remote = Mock()
    remote.sync_task.return_value = None
    remote.log.return_value = None
    return remote


@pytest.fixture
def spy_remote():
    remote = Mock()
    remote.calls = []

    def record_sync(task):
        remote.calls.append(("sync_task", task))

    def record_log(event, **data):
        remote.calls.append(("log", event, data))

    remote.sync_task.side_effect = record_sync
    remote.log.side_effect = record_log

    remote.assert_sync_called = lambda: remote.sync_task.called
    remote.assert_log_contains = lambda text: any(text in str(call) for call in remote.calls)
    return remote


@pytest.fixture
def broken_remote():
    remote = Mock()
    remote.sync_task.side_effect = Exception("Network error")
    remote.log.side_effect = Exception("Log service unavailable")
    return remote


@pytest.fixture
def app(working_cache, fake_remote):
    return TodoApp(working_cache, fake_remote)


@pytest.fixture
def app_with_sample_tasks(app):
    task1_id = app.add_task("Learn pytest")
    task2_id = app.add_task("Write tests")
    return app, [task1_id, task2_id]
