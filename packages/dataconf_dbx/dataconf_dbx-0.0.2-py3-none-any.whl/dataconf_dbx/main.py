from dataclasses import MISSING, fields, is_dataclass
from typing import Any, Dict, List, Type

import dataconf.main as dataconf
from dataconf.utils import __env_vars_parse as env_vars_parse

from . import exceptions, utils


class Multi:
    def __init__(self, confs: List[dataconf.ConfigTree], on: Any = None, **kwargs: Dict[str, Any]) -> None:
        self._multi = dataconf.Multi(confs, strict=False, **kwargs)
        self._on = on
        self._validate_on()

        self.confs = confs
        self.kwargs = kwargs

    def _validate_on(self) -> None:
        if self._on is not None and not is_dataclass(self._on):
            raise exceptions.NotDataClass()

    def set_on(self, on: Type) -> "Multi":
        self._on = on
        self._validate_on()
        return Multi(self.confs, on, **self.kwargs)

    def _parse_from_dbx(self, prefix: str, clazz: Type) -> Dict[str, Any]:
        config_dict = {}

        for field in fields(clazz):
            value: Any = None

            if field.name.startswith("_"):
                continue

            name = prefix + field.name

            if is_dataclass(field.type):
                value = self._parse_from_dbx(name + "__", field.type)
                config_dict.update(value)

            else:
                if not isinstance(field.default, type(MISSING)):
                    value = utils.set_and_get_widget(name, field.default)

                elif field.default_factory is not MISSING:
                    value = utils.set_and_get_widget(name, field.default_factory())

                else:
                    value = utils.set_and_get_widget(name, "")

                config_dict[name] = value

        return config_dict

    def dbx(self, prefix: str = "", **kwargs: Dict[str, Any]) -> Any:
        """Generate a dictionary of configurations from dataclass fields
        and dbutils."""

        if self._on is None:
            raise exceptions.MissingArgument("on")

        if not prefix.endswith("_") and prefix != "":
            prefix = f"{prefix}_"

        config_dict = self._parse_from_dbx(prefix, self._on)
        data = env_vars_parse(prefix, config_dict)

        return self.dict(data, **kwargs)

    def __getattr__(self, attr: Any) -> Any:
        """Delegate attribute access to the contained _multi object."""
        if hasattr(self._multi, attr):

            def wrapper(*args: Any, **kwargs: Any) -> Any:
                new_multi = getattr(self._multi, attr)(*args, **kwargs)
                return Multi(self.confs + new_multi.confs, self._on, **self.kwargs)

            return wrapper
        raise exceptions.UnknownDataconfAttribute(attr)

    def get(self) -> Any:
        """Parse the configurations into the dataclass type."""
        return self._multi.on(self._on)
