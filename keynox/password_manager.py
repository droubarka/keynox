
import hashlib

from vault import Vault

class PasswordManager:
	"""
	A class to manage password entries stored in a vault.
	"""

	def __init__(self, vault: Vault) -> None:
		"""
		Initializes the PasswordManager object with a vault.
		"""
		self.vault = vault
		self.entries = vault.retrieve()
		self.update_sync_fingerprint()


	def calculate_sync_fingerprint(self) -> bytes:
		"""
		Calculates the sync fingerprint based on the current entries.
		"""
		entries = [str(sorted(entry.items())) for entry in self.entries]
		sync_fingerprint = hashlib.sha256(''.join(entries).encode()).digest()

		return sync_fingerprint


	def update_sync_fingerprint(self) -> None:
		"""
		Updates the internal sync fingerprint to match the current entries.
		"""
		self.sync_fingerprint = self.calculate_sync_fingerprint()


	def add_entry(self, entry: dict) -> None:
		"""
		Adds a new entry to the list os password entries.
		"""
		self.entries.append(entry)


	def remove_entry(self, entry: dict) -> None:
		"""
		Removing an existing entry from the list of password entries.
		"""
		self.entries.remove(entry)


	def remove_entry_by_index(self, index: int) -> None:
		"""
		Removes an entry from the list by its index.
		"""
		self.remove_entry(self.entries[index])


	def sync_vault(self) -> None:
		"""
		Syncs the vault with the internal state of the PasswordManager object.
		"""
		self.vault.store(data=self.entries)
		self.update_sync_fingerprint()


	def get_entry(self, key: str, value: str) -> dict:
		"""
		Retrieves a single entry that matches the given key-value pair.
		"""
		for entry in self.entries:
			if key in entry["data"].keys():
				if entry["data"][key] == value:
					return entry
		return None


	def get_entry_list(self, key: str, value: str) -> list:
		"""
		Retrieves a list of entries that match the given key-value pair.
		"""
		list = []
		for entry in self.entries:
			if key in entry["data"].keys():
				if entry["data"][key] == value:
					list.append(entry)
		return list
