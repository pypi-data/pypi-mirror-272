import importlib.util
from typing import Any

found = importlib.util.find_spec("dbutils")


if not found:
    from .mocks import dbutils


def set_and_get_widget(name: str, default: Any) -> str:
    dbutils.widgets.text(name, default)
    return dbutils.widgets.get(name)
