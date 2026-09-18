from cryptography.fernet import Fernet
from django.conf import settings


def get_encryption_key():
	key = settings.FIELD_ENCRYPTION_KEY
	if not key:
		raise ValueError("FIELD_ENCRYPTION_KEY is not configured")
	return Fernet(key.encode())


def encrypt_value(value):
	if not value:
		return None
	key = get_encryption_key()
	return key.encrypt(value.encode()).decode()


def decrypt_value(value):
	if not value:
		return None
	key = get_encryption_key()
	return key.decrypt(value.encode()).decode()


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
