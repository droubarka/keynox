
"""
Keynox CLI Program

This program provides a command-line interface for managing passwords.
"""

import os
import sys

from colorama import Fore
from getpass import getpass
from io import open

from password_manager import PasswordManager
from vault import Vault


KEYNOX_LOGO_FILEPATH = './cli/keynox-logo.dat'
MENU_FILEPATH_FORMAT = './cli/menu/lvl-{}.dat'

password_manager = None


def render_logo_and_menu(level: int=None) -> None:
	"""
	Renders the logo and menu files.
	"""

	os.system('cls' if os.name == 'nt' else 'clear')

	try:
		with open(KEYNOX_LOGO_FILEPATH, 'rt') as file:
			print(file.read())

	except Exception: Ellipsis

	if password_manager != None:
		print(f"\tVault: {password_manager.vault.filename}")
		print(f"\tEntries: {len(password_manager.entries)}", end=' ')
		print(f"| Synchronized: {password_manager.is_sync()}")
		print()

	try:
		if level != None:
			with open(MENU_FILEPATH_FORMAT.format(level), 'rt') as file:
				print(file.read())

	except Exception: Ellipsis


def display_error_message(error: Exception) -> None:
	"""
	Displays an error message.
	"""

	sys.stderr.write(Fore.RED)
	sys.stderr.write(f"[!] {type(error).__name__}: {error}\n")
	sys.stderr.write(Fore.RESET)
	print()

	return None


def main_menu() -> int:
	"""
	Displays the main menu.
	"""

	choice = input("> ")

	if choice.lower() in ("0", "exit"):
		sys.exit(0)

	elif choice in ("1", "2"):
		return int(choice)

	else:
		raise ValueError(f"Invalid choice: '{choice}'")


def new_vault(filename: str) -> Vault:
	"""
	Creates a new vault with given filename.
	"""

	# Check if the file can be created
	open(filename, 'w').close()

	master_password = getpass("Master Password: ")

	vault = Vault(filename, master_password)
	vault.store(data=[])

	return vault


def create_vault_menu() -> PasswordManager:
	"""
	Displays the create vault menu for creating a new vault.
	"""

	filename = input("Enter file in which to save the vault: ")

	if os.path.isfile(filename):
		print()
		display_error_message(
			FileExistsError(f"[Errno 17] file exists: '{filename}'"))

		choice = input("Overwrite (y/N)? ")

		if choice.lower() in ("y", "yes"):
			return PasswordManager(new_vault(filename))

	else:
		return PasswordManager(new_vault(filename))

	return None


def display_menu() -> None:
	"""
	Displays the menu and manages user interactions.
	"""

	global password_manager

	level = 0
	error = None

	while True:
		render_logo_and_menu(level)

		if error != None:
			error = display_error_message(error)

		if level == 0:
			try:
				level = main_menu()

			except ValueError as xerr:
				error = xerr

			except EOFError:
				pass

			except KeyboardInterrupt:
				sys.exit(0)

		elif level == 1:
			try:
				password_manager = create_vault_menu()

				if password_manager != None:
					level = 3

			except EOFError:
				pass

			except KeyboardInterrupt:
				level = 0

			except Exception as xerr:
				error = xerr

		else:
			sys.exit(0)


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
