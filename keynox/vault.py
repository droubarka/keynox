
import json

class Vault:
	def __init__(self, filename: str, master_password=None, salt=None) -> None:
		self.filename = filename

	def store(self, data: dict) -> None:
		# Store data to the file.
		with open(self.filename, 'w') as file:
			json.dump(data, file)

	def retrieve(self) -> dict:
		# Retrieve data from the file.
		with open(self.filename) as file:
			return json.load(file)
