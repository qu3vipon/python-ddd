class ValueObjectEnumError(Exception):
    def __str__(self):
        return "Value Object got invalid value."


class BaseMsgException(Exception):
    message: str

    def __str__(self):
        return self.message
