import pytest
from src.models.primitives.person import PersonPassword
from src.models.exc import AccessError, AttributeValidationError


def test_setup_password_with_null_value():
    with pytest.raises(AttributeValidationError) as e:
        PersonPassword(None)

    assert e.value.message == "Password cannot be None"


def test_setup_password_with_wrong_length():
    with pytest.raises(AttributeValidationError) as e:
        PersonPassword("11")

    assert e.value.message == "Wrong password length"


def test_password_access_only_at_once():
    password = PersonPassword("111")

    assert password.value == "111"

    with pytest.raises(AccessError) as e:
        print(password.value)

    assert e.value.message == "Password value has already been consumed"
