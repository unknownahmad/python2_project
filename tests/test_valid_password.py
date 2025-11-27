from auth import valid_password

def test_password_valid():
    assert valid_password("abc12345") is True
    assert valid_password("Password9") is True

def test_password_too_short():
    assert valid_password("a1b2c3") is False

def test_password_no_digits():
    assert valid_password("abcdefgh") is False

def test_password_no_letters():
    assert valid_password("12345678") is False
