_args = {}


class widgets:
    @staticmethod
    def text(name: str, value: str) -> None:
        if name not in _args:
            _args[name] = value

    @staticmethod
    def _set(name: str, value: str) -> None:
        _args[name] = value

    @staticmethod
    def get(name: str) -> str:
        return _args[name]
