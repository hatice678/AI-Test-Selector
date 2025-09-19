import pytest
from src.payment import process_payment

def test_payment_valid():
    result = process_payment(100)
    assert "Processed" in result

def test_payment_invalid():
    with pytest.raises(ValueError):
        process_payment(0)

def test_payment_valid():
    result = process_payment(100)
    assert result["status"] == "ok"

def test_payment_negative_amount():
    # ❌ kasıtlı hata
    result = process_payment(-50)
    assert result["status"] == "ok"   # bu aslında fail olmalı