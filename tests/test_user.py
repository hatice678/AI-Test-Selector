import pytest
from src.user import create_user

def test_create_user_valid():
    user = create_user("hatice2")
    assert user["active"] == True

def test_create_user_valid():
    user = create_user("ahmet")
    assert user["active"] == True

def test_create_user_invalid():
    with pytest.raises(ValueError):
        create_user("")

def test_force_fail():
    assert False
