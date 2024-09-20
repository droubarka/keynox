
import os, sys

from time import sleep

from vault import Vault
from status import show_error


def level_3(vault: Vault) -> tuple:
	#? Next step (not implemented)
	errorlevel = 200
	level = 3
	try:
		choice = input("> ")

		if choice == "1":
			level = 0 #?

		elif choice in ("2", "3", "4"):
			level = 0 #?
		else:
			errorlevel = 400

	except KeyboardInterrupt:
		level = 0 #?
	except Exception as error:
		show_error(-99, error=error) #?


	return errorlevel, level


def open_vault(filename: str) -> Vault:
	vault = Vault(filename)
	vault.retrieve()

	return vault

def import_vault() -> tuple:
	#! Import a vault
	errorlevel = 200
	level = 2
	filename = None
	vault = None
	try:
		filename = input("Enter the file of the vault to import: ")

		if os.path.isfile(filename):
			vault = open_vault(filename)
			level = 3

		else:
			# Try to open the file (this will raise an exception)
			open(filename).close()

	except KeyboardInterrupt:
		level = 0
	except PermissionError:
		errorlevel = 401
	except IsADirectoryError:
		errorlevel = 402
	except FileNotFoundError:
		errorlevel = 404
	except Exception as error:
		show_error(-99, error=error) #?

	return errorlevel, level, filename, vault


def new_vault(filename: str) -> Vault:
	vault = Vault(filename)
	vault.store(data=[])

	return vault

def create_vault() -> tuple:
	errorlevel = 200
	level = 1
	filename = None
	vault = None
	try:
		filename = input("Enter file in which to save the vault: ")

		if os.path.isfile(filename):
			# Show error message if file already exists
			show_error(403, filename=filename)

			choice = input("Overwrite (y/N)? ")

			if choice.lower() in ("y", "yes"):
				vault = new_vault(filename)
				level = 3

		else:
			vault = new_vault(filename)
			level = 3

	except KeyboardInterrupt:
		level = 0
	except PermissionError:
		errorlevel = 401
	except IsADirectoryError:
		errorlevel = 402
	except FileNotFoundError:
		errorlevel = 404
	except Exception as error:
		show_error(-99, error=error) #?

	return errorlevel, level, filename, vault


def main_menu() -> tuple:
	errorlevel = 200
	level = 0
	try:
		choice = input("> ")

		if choice in ("1", "2"):
			level = int(choice)
		elif choice.lower() in ("0", "exit", "quit"):
			raise KeyboardInterrupt
		else:
			errorlevel = 400

	except KeyboardInterrupt:
		raise
	except Exception as error:
		show_error(-99, error=error) #?

	return errorlevel, level


def menu() -> None:
	errorlevel = 200
	level = 0
	filename = None
	vault = None
	while True:
		# Clear the terminal screen
		os.system("cls" if os.name == "nt" else "clear")

		try:
			# Displays the Keynox logo
			with open('./cli/keynox-logo.ascii') as file:
				print(file.read())

		except FileNotFoundError:
			Ellipsis

		try:
			# Displays the menu at the specified level
			with open(f'./cli/menu/menu-{level}.x') as file:
				print(file.read())

		except FileNotFoundError:
			Ellipsis

		if errorlevel in (400,):
			errorlevel = show_error(errorlevel)

		if errorlevel in (401, 402, 403, 404):
			errorlevel = show_error(errorlevel, filename=filename)

		try:
			if level == 0:
				errorlevel, level = main_menu()
			elif level == 1:
				errorlevel, level, filename, vault = create_vault()
			elif level == 2:
				errorlevel, level, filename, vault = import_vault()
			elif level == 3:
				errorlevel, level = level_3(vault)
			else:
				raise KeyboardInterrupt #?

		except KeyboardInterrupt:
			raise
		except Exception as error:
			show_error(-99, error=error) #?


def main():
	try:
		menu()

	except KeyboardInterrupt:
		print("\n#? Exiting ...")
		sys.exit(0)
	except Exception as error:
		show_error(-99, error=error) #?


if __name__ == "__main__": main()
