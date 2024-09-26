
import os
import sys
import time

from getpass import getpass
from io import open

from password_manager import PasswordManager
from utils import genpass
from vault import Vault


KEYNOX_LOGO_FILEPATH = './cli/keynox-logo.dat'
MENU_FILEPATH_FORMAT = './cli/menu/lvl-{}.dat'


def render_logo_and_menu() -> None:
	"""
	Renders the logo and menu files.
	"""

	try:
		with open(KEYNOX_LOGO_FILEPATH) as file:
			print(file.read())

	except FileNotFoundError: Ellipsis

	if vault != None:
		print(f"\t    Vault: {vault}\n") #?

	try:
		with open(MENU_FILEPATH_FORMAT.format(level)) as file:
			print(file.read())

	except FileNotFoundError: Ellipsis


def display_error_message() -> None:
	"""
	Displays an error message based on the given error level.
	"""

	error_lookup = {
		-1 : 'XError',
		400: 'InvalidOption',
		401: 'PermissionError',
		402: 'IsADirectoryError',
		403: 'FileAlreadyExists',
		404: 'FileNotFoundError'
	}

	sys.stderr.write(error_lookup[errorlevel])

	if error != None:

		sys.stderr.write(": {}".format(error))

	sys.stderr.write("\n")


def handle_error(*args: None, **kwargs: None) -> None: #?
	"""
	Handles error levels and displays appropriate error messages.
	"""

	global error, errorlevel

	redcode = '\033[91m'
	defcode = '\033[0m'

	if errorlevel == 403:
		print()

	sys.stderr.write(f"{redcode}[!] ")

	display_error_message()

	sys.stderr.write(f"{defcode}")
	print()

	time.sleep(0.1)

	error, errorlevel = None, 200


def main_menu() -> None:
	"""
	Displays the main menu and handles user input.
	"""

	global error, level, errorlevel

	choice = input("> ")

	if choice in ("1", "2"):
		level = int(choice)

	elif choice.lower() in ("0", "exit"):
		sys.exit(0)

	else:
		error, errorlevel = f"'{choice}'", 400 #: InvalidOption


def new_vault(filename: str) -> Vault:
	"""
	Creates a new vault with the given filename.
	"""

	global error, errorlevel

	try:
		master_password = getpass("Master Password: ")

		vault = Vault(filename, master_password)
		vault.store(data=[])

	except (PermissionError, IsADirectoryError, FileNotFoundError):
		error = f"'{filename}'"
		raise

	except Exception as xerr: #? pass
		handle_error(
				error:=f"Failed to create vault in {filename}: {xerr}",
				errorlevel:=-1)
		sys.exit(1)

	return vault


def create_vault_menu() -> None:
	"""
	Display the create vault menu for creating a new vault.
	"""

	global error, level, errorlevel, vault, password_manager

	filename = input("Enter file in which to save the vault: ")

	if os.path.isfile(filename):
		handle_error(error:=filename, errorlevel:=403) #: FileAlreadyExists

		choice = input("Overwrite (y/N)? ")

		if choice.lower() in ("y", "yes"):
			vault = new_vault(filename)
			password_manager = PasswordManager(vault)
			level = 3

	else:
		vault = new_vault(filename)
		password_manager = PasswordManager(vault)
		level = 3


def open_vault(filename: str) -> Vault:
	"""
	Opens an existing vault from the given filename.
	"""

	global error, errorlevel

	try:
		master_password = getpass("Master Password: ")

		vault = Vault(filename, master_password)
		vault.retrieve()

	except PermissionError:
		error = f"'{filename}'"
		raise

	except Exception as xerr: #? pass
		handle_error(
				error:=f"Failed to import vault in {filename}: {xerr}",
				errorlevel:=-1)
		sys.exit(1)

	return vault


def import_vault_menu() -> None:
	"""
	Provides a menu for importing an existing vault.
	"""

	global error, level, vault, password_manager

	filename = input("Enter the file of the vault to import: ")

	if os.path.isfile(filename):
		vault = open_vault(filename)
		password_manager = PasswordManager(vault)
		level = 3

	else:
		error = f"'{filename}'"
		# Try to open the file (this will raise an exception)
		open(filename).close()


def create_entry() -> dict:
	"""
	Creates a new entry for a password manager.
	"""

	entry = {"data": dict(), "meta": dict()}

	choice = input("Generate password randomly (Y/n)? ")
	print()

	if choice.lower() in ("n", "no"):
		password = getpass("Password : ")

	else:
		policy = {"digit": 1, "lowercase": 1, "uppercase": 1, "special": 1} #?
		password = genpass(32, policy) #?

	entry["data"] = {
		"username": input("Username : "),
		"url"     : input("URL      : "),
		"name"    : input("Name     : "),
		"category": input("Category : ")
	}

	print("\nLet's take some notes!")
	print("Enter your notes (press 'Ctrl+D' to finish):\n") #?

	notes = []

	while True:
		try:
			user_note = input("Add note : ")
		except EOFError:
			print()
			break

	entry["data"]["notes"] = "\n".join(notes)
	entry["data"]["password"] = password
	entry["meta"]["last-update"] = time.strftime("%a %b %H:%M:%S %Z %Y")

	return entry


#! Un/Stable code


def password_manager_menu() -> None:
	"""
	Displays the password manager menu, allowing user to modify the vault.
	"""

	global error, errorlevel

	try:
		choice = input("> ")
		print() #?

		if choice == "1":
			entry = create_entry()
			choice = input("\nSave to password manager (Y/n)? ")
			if choice.lower() not in ("n", "no"):
				password_manager.add_entry(entry)
			pass #? is_saved


		else:
			error, errorlevel = f"'{choice}'", 400 #: FileAlreadyExists

	except KeyboardInterrupt: #?
		sys.exit(1)


def display_menu() -> None: #?

	global error, errorlevel, level

	while True:

		os.system('cls' if os.name == 'nt' else 'clear')

		render_logo_and_menu()

		if errorlevel != 200:
			handle_error() #?

		try:
			if level == 0:
				main_menu()

			elif level == 1:
				create_vault_menu()

			elif level == 2:
				import_vault_menu()

			elif level == 3:
				password_manager_menu()
				pass

			else:
				pass

		except KeyboardInterrupt:
			if level == 0:
				sys.exit(0)
			elif level in (1, 2):
				level = 0
			else:
				pass

		except EOFError:
			input("catched") #?

		except SystemExit:
			raise

		except PermissionError:
			errorlevel = 401
		except IsADirectoryError:
			errorlevel = 402
		except FileNotFoundError:
			errorlevel = 404
		except Exception as xerr:
			handle_error(error:=xerr, errorlevel:=-1)
			sys.exit(1)

#~ ctrl-keys

#! Un/Stable code

error = None

level = 0
errorlevel = 200

vault = None
password_manager = None

def main() -> int:
	"""
	Main entry point for the program.
	"""

	exit_status = 0

	try:
		display_menu()
		pass

	except SystemExit as exc:
		exit_status = exc.code

	return exit_status


if __name__ == '__main__':
	exit_status = main()
	sys.exit(exit_status)
