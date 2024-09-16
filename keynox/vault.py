
import json

class Vault:
	def __init__(self, file_path) -> None:
		# Initialize a Vault instance with a file path.
		self.file_path = file_path

	def store(self, data: dict) -> None:
		# Store data to the file.
		with open(self.file_path, 'w') as file:
			json.dump(data, file)

	def retrieve(self) -> dict:
		# Retrieve data from the file.
		with open(self.file_path) as file:
			return json.load(file)
