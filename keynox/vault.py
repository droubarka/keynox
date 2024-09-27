
import base64
import json
import pathlib
import secrets

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


class Vault:
	"""
	A simple encrypted data vault.
	"""
	def __init__(self, filename: str, master_password: str) -> None:
		"""
		Initializes the Vault object with a filename and a master password.
		"""
		self.filename = filename
		self.filename_salt = pathlib.Path(filename).with_suffix('.salt')
		self.master_password = master_password


	def _derive_key(self, salt: bytes) -> bytes:
		"""
		Derives an encryption key from the master password and salt.
		"""
		#! memory required: 128 * N * r * p == 64MB (67108864 Bytes)
		kdf = Scrypt(salt=salt, length=32, n=2**16, r=8, p=1)
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
