
from vault import Vault

entry = {
	"category": "Social Networking sites for Programmers"
	"url":      "https://github.com",
	"username": "droubarka",
	"password": "!password"
	"name":     "MY GITHUB ACCOUNT"
	"notes":    "last-update: Tue Sep 17 17:21:00 EDT 2024"
}

class PasswordManager:
	def __init__(self, vault: Vault) -> None:
		self.vault, self.entries = vault, vault.retrieve()

	def add_entry(self, entry: dict) -> None:
		self.entries.append(entry)

	def remove_entry(self, entry: dict) -> None:
		self.entries.remove(entry)

	def get_entry(self, key: str, value: str) -> dict:
		for entry in self.entries:
			if entry.get(key) == value:
				return entry
