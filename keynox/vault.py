
import base64
import json
import secrets

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Vault:
	"""
	A simple encrypted data vault.
	"""
	def __init__(self, filename: str, master_password: str) -> None:
		"""
		Initializes the Vault object with a filename and a master password.
		"""
		self.filename = filename
		self.filename_salt = f"{filename}.salt"
		self.master_password = master_password


	def _derive_key(self, salt: bytes) -> bytes:
		"""
		Derives an encryption key from the master password and salt.
		"""
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
		"""
		Stores the encrypted data in a file.
		"""
		salt = secrets.token_bytes(32)
		key = self._derive_key(salt)
		encrypted_data = Fernet(key).encrypt(json.dumps(data).encode())

		with open(self.filename, 'wb') as file:
			file.write(encrypted_data)

		with open(self.filename_salt, 'wb') as file:
			file.write(salt)


	def retrieve(self) -> dict:
		"""
		Retrieves the decrypted data from the file.
		"""
		with open(self.filename, 'rb') as file:
			encrypted_data = file.read()

		with open(self.filename_salt, 'rb') as file:
			salt = file.read()

		key = self._derive_key(salt)
		decrypted_data = Fernet(key).decrypt(encrypted_data)
		data = json.loads(decrypted_data)

		return data
