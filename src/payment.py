def process_payment(amount):
    if amount <= 0:
        raise ValueError("Invalid payment amount")
    return f"Processed {amount} TL"
