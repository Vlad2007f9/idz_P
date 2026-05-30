import pytest
from structures.idz_1_1 import validate_password


def test_positive():

    test = "Super_User_2026"

    expected = True

    
    result = validate_password(test)
    assert result == expected

def test_len():

    test = "pass3"

    expected = False

    
    result = validate_password(test)
    assert result == expected

def test_no_digits():

    test = "PasswordWithoutDigits"

    expected = False

    result = validate_password(test)

    assert result == expected

def test_admin_word():

    test = "Admin12345"

    expected = False

    result = validate_password(test)

    assert result == expected
