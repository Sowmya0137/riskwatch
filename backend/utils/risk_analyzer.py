import re


def detect_aadhaar(text):
    aadhaar_pattern = re.compile(r'\b\d{4}\s?\d{4}\s?\d{4}\b')
    return aadhaar_pattern.findall(text)


def detect_phone_number(text):
    phone_pattern = re.compile(r'\b\d{10}\b')
    return phone_pattern.findall(text)


def detect_email(text):
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    return email_pattern.findall(text)


def detect_bank_details(text):
    bank_pattern = re.compile(r'\b\d{9,18}\b')  # Simulated pattern for bank account numbers
    return bank_pattern.findall(text)


def detect_password(text):
    password_pattern = re.compile(r'\b[a-zA-Z0-9@#$%^&+!=]{8,}\b')  # Simulated password pattern
    return password_pattern.findall(text)


def calculate_risk_score(text):
    risk_score = 0
    detected_items = {'Aadhaar': detect_aadhaar(text), 'Phone Numbers': detect_phone_number(text), 'Emails': detect_email(text), 'Bank Details': detect_bank_details(text), 'Passwords': detect_password(text)}

    if detected_items['Aadhaar']:
        risk_score += 30
    if detected_items['Phone Numbers']:
        risk_score += 20
    if detected_items['Emails']:
        risk_score += 15
    if detected_items['Bank Details']:
        risk_score += 40
    if detected_items['Passwords']:
        risk_score += 35

    # Cap the risk score at 100
    risk_score = min(risk_score, 100)

    risk_level = 'Low'
    if risk_score > 50:
        risk_level = 'Medium'
    if risk_score > 75:
        risk_level = 'High'

    return {'risk_score': risk_score, 'risk_level': risk_level, 'detected_items': detected_items}

# Example of usage
if __name__ == '__main__':
    sample_text = "..."  # Add sample text here
    result = calculate_risk_score(sample_text)
    print(result)