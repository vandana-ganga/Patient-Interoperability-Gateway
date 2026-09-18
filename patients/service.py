from cryptography.fernet import Fernet
from django.conf import settings


def get_cipher():
    key = settings.FIELD_ENCRYPTION_KEY

    if not key:
        raise ValueError("FIELD_ENCRYPTION_KEY is not configured")

    return Fernet(key.encode())


def encrypt_value(value):
    if not value:
        return None

    cipher = get_cipher()

    return cipher.encrypt(value.encode()).decode()


def decrypt_value(value):
    if not value:
        return None

    cipher = get_cipher()

    return cipher.decrypt(value.encode()).decode()


def mask_ssn(ssn):
    if not ssn:
        return None

    digits = "".join(
        character for character in ssn
        if character.isdigit()
    )

    if len(digits) != 9:
        return "***"

    return f"***-**-{digits[-4:]}"


def extract_identifier(data, system):
    identifiers = data.get("identifier", [])

    for identifier in identifiers:
        if identifier.get("system") == system:
            return identifier.get("value")

    return None