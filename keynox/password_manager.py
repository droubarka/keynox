
from vault import Vault


class PasswordManager:
	def __init__(self, vault: Vault) -> None:
		self.vault, self.entries = vault, vault.retrieve()

	def add_entry(self, entry: dict) -> None:
		self.entries.append(entry)

	def remove_entry(self, entry: dict) -> None:
		self.entries.remove(entry)

	def get_entry(self, key: str, value: str) -> dict:
		for entry in self.entries:
			if key in entry.keys():
				if entry[key] == value:
					return entry
		return None

	def get_entry_list(self, key: str, value: str) -> list:
		list = []
		for entry in self.entries:
			if key in entry.keys():
				if entry[key] == value:
					list.append(entry)
		return list
