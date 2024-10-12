
import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


def fernet_encrypt(key: bytes, data: bytes) -> bytes:
	token = Fernet(key).encrypt(data)
	return token

def fernet_decrypt(key: bytes, token: bytes, ttl=None) -> bytes:
	data = Fernet(key).decrypt(token, ttl)
	return data

def scrypt_derive_key(key_material: bytes, salt: bytes, length: int, n: int, r: int, p: int) -> bytes:
	kdf = Scrypt(salt, length, n, r, p)
	key = base64.urlsafe_b64encode(
		kdf.derive(key_material)
	)
	return key

def scrypt_derive_keys(key_material: bytes, salts: list[bytes], length: int, n: int, r: int, p: int) -> list[bytes]:
	keys = []
	for salt in salts:
		keys.append(
			scrypt_derive_key(key_material, salt, length, n, r, p)
		)
	return keys

def pbkdf2_derive_key(key_material: bytes, salt: bytes, length: int, algorithm: hashes.HashAlgorithm, iterations: int) -> bytes:
	kdf = PBKDF2HMAC(algorithm, length, salt, iterations)
	key = base64.urlsafe_b64encode(
		kdf.derive(key_material)
	)
	return key

def pbkdf2_derive_keys(key_material: bytes, salts: list[bytes], length: int, algorithm: hashes.HashAlgorithm, iterations: int) -> list[bytes]:
	keys = []
	for salt in salts:
		keys.append(
			pbkdf2_derive_key(key_material, salt, length, algorithm, iterations)
		)
	return keys
