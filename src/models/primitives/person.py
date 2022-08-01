from src.models.exc import AttributeValidationError, AccessError
from copy import deepcopy


class PersonPassword:
    MIN_LENGTH = 3
    MAX_LENGTH = 240

    def __init__(self, value: str):
        if value is None:
            raise AttributeValidationError("Password cannot be None")

        if len(value) < self.MIN_LENGTH or len(value) > self.MIN_LENGTH:
            raise AttributeValidationError("Wrong password length")

        self._value = value

    @property
    def value(self):
        if self._value is None:
            raise AccessError("Password value has already been consumed")

        pass_ = deepcopy(self._value)

        self._value = None

        return pass_

    def __repr__(self):
        return f"<Password value=********>"
