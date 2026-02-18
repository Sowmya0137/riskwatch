import re

def check_pii(text):
    score = 0

    # Email detection
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.search(email_pattern, text):
        score += 30

    # Phone number detection
    phone_pattern = r'\b\d{10}\b'
    if re.search(phone_pattern, text):
        score += 30

    # Credit card detection (16 digits)
    card_pattern = r'\b\d{16}\b'
    if re.search(card_pattern, text):
        score += 40

    return score
