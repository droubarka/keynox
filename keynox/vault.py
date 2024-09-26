
import base64
import json
import os
import secrets

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Vault:
	def __init__(self, filename: str, master_password: str) -> None:
		self.filename = filename
		self.master_password = master_password


	def derive_key(self, salt: bytes) -> bytes:
		kdf = PBKDF2HMAC(
			algorithm=hashes.SHA256(),
			length=32,
			salt=salt,
			iterations=341291,
		)
		key = base64.urlsafe_b64encode(
			kdf.derive(self.master_password.encode())
		)
		return key


	def store(self, data: dict) -> None:

		salt = secrets.token_bytes(32)
		key = self.derive_key(salt)
		encrypted_data = Fernet(key).encrypt(json.dumps(data).encode())

		with open(self.filename, 'wb') as file:
			file.write(encrypted_data)

		with open(self.filename + '.salt', 'wb') as file:
			file.write(salt)


	def retrieve(self) -> dict:

		with open(self.filename, 'rb') as file:
			encrypted_data = file.read()

		with open(self.filename + '.salt', 'rb') as file:
			salt = file.read()

		key = self.derive_key(salt)
		decrypted_data = Fernet(key).decrypt(encrypted_data)
		data = json.loads(decrypted_data)

		return data
