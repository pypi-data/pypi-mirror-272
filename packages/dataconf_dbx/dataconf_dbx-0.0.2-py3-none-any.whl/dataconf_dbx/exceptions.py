class NotDataClass(ValueError):
    def __init__(self) -> None:
        self.message = "`on` is not a dataclass."
        super().__init__(self.message)


class MissingArgument(ValueError):
    def __init__(self, arg: str) -> None:
        self.message = f"Argument `{arg}` must be defined."
        super().__init__(self.message)


class UnknownDataconfAttribute(AttributeError):
    def __init__(self, attr: str) -> None:
        self.message = f"Attribute `{attr}` not found in Multi."
        super().__init__(self.message)
