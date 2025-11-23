# Todo demo для курса по pytest

Мини-приложение списка задач с кешем и синхронизацией через удалённый сервис. Используется в курсе [Pytest: From Zero to Confidence](https://potapov.me/ru/education/courses/pytest-from-zero-to-confidence) Константина Потапова для демонстрации подходов к тестированию.

## Что важно знать
- Требуется Python 3.10+.
- В основной ветке оставлены намеренные ошибки для практики.
- Исправленная версия находится в ветке `fixed`.

## Установка
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[test]
```

## Запуск тестов
```bash
pytest
```

## Структура
- `src/app.py` — логика работы с задачами и синхронизация.
- `src/cache.py` — заглушка кеша.
- `src/remote.py` — имитация удалённого сервиса.
- `tests/` — набор тестов для уроков.
