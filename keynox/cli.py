
"""
Keynox CLI Program

This program provides a command-line interface for managing passwords.
"""

import os
import sys
import time

from colorama import Fore
from getpass import getpass
from io import open
from rich.console import Console
from rich.table import Table

from password_manager import PasswordManager
from utils import genpass
from vault import Vault, InvalidToken


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
		print("\tVault: {}{}{}".format(
			Fore.LIGHTYELLOW_EX,
			os.path.abspath(password_manager.vault.filename),
			Fore.RESET))
		is_sync = password_manager.is_sync()
		print("\tSynchronized: {}{}{}".format(
			[Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX][is_sync],
			is_sync,
			Fore.RESET), end=' ')
		print("| Entries: {}{}{}".format(
			Fore.CYAN,
			len(password_manager.entries),
			Fore.RESET))
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

	sys.stderr.write(Fore.LIGHTRED_EX)
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

	master_password = getpass("\nSet Master Password: ")
	re_entered_master_password = getpass("Retype Master Password: ")

	if master_password != re_entered_master_password:
		raise ValueError("Sorry, master passwords do not match.")

	vault = Vault(filename, master_password)
	vault.store(data=[])

	return vault


def create_vault_menu() -> PasswordManager:
	"""
	Displays the create vault menu for creating a new vault.
	"""

	filename = input("Enter file in which to save the vault: ")

	if os.path.isfile(filename):
		#? check if the file is keynox type

		try:
			# raise an exception: FileExistsError
			open(filename, 'x').close()

		except Exception as error:
			print()
			display_error_message(error)

		choice = input("Overwrite (y/N)? ")

		if choice.lower() in ("y", "yes"):
			return PasswordManager(new_vault(filename))

	else:
		return PasswordManager(new_vault(filename))

	return None


def open_vault(filename: str) -> Vault:
	"""
	Opens an existing vault from the given filename.
	"""

	# Check if the file can be read
	open(filename, 'r').close()

	master_password = getpass("\nMaster Password: ")

	vault = Vault(filename, master_password)
	#~ vault.retrieve()

	return vault


def import_vault_menu() -> PasswordManager:
	"""
	Provides an menu for importing an existing vault.
	"""

	filename = input("Enter the file of the vault to import: ")

	if os.path.isfile(filename):
		try:
			return PasswordManager(open_vault(filename))

		except InvalidToken as error:
			if not error.args:
				error.args = ("Token is invalid or corrupted.",)

			raise InvalidToken(error)

	# Try to open the file (this will raise an exception)
	open(filename).close()


def create_entry() -> None:
	"""
	Creates a new password entry.
	"""

	entry = {'data': {}, 'meta': {}}

	choice = input("Generate password randomly (Y/n)? ")
	print()

	if choice.lower() in ("n", "no"):
		password = getpass("Password : ")

	else:
		policy = {'digit': 1, 'lowercase': 1, 'uppercase': 1, 'special': 1} #?
		password = genpass(32, policy) #?

	entry['data'] = {
		'username': input("Username : "),
		'url'     : input("URL      : "),
		'name'    : input("Name     : "),
		'category': input("Category : "),
		'password': password
	}

	print("\nLet's take some notes!")
	print("Enter your notes (press 'Ctrl+D' to finish):\n") #?

	notes = []
	while True:
		try:
			notes.append(input("Add note : "))

		except EOFError:
			print()
			break

	entry['data']['notes'] = "\n".join(notes)
	entry['meta']['last-update'] = time.strftime("%a %b %H:%M:%S %Z %Y")

	choice = input("\nSave to password manager (Y/n)? ")

	if choice.lower() not in ("n", "no"):
		password_manager.add_entry(entry)


def pause() -> None:
	"""
	Pauses the program execution and waits for the Enter key press.
	"""

	getpass("\nPress Enter to continue ... ")


def show_entries() -> None: #?
	"""
	Displays password manager entries.
	"""

	console = Console()

	len_entries = len(password_manager.entries)

	if not len_entries:
		print("No entries found.")
		pause()

	rows_per_page = 32 #?
	index = 0

	while index < len_entries:
		os.system('cls' if os.name == 'nt' else 'clear')

		table = Table(title=f"Password Manager Entries\n", box=None)

		table.add_column("ID", justify="right", no_wrap=True)
		table.add_column("Category")
		table.add_column("Name")
		table.add_column("Username")
		table.add_column("URL")
		table.add_column("Note", no_wrap=True)

		for id in range(index, min(index + rows_per_page, len_entries)):
			entry = password_manager.entries[id]
			table.add_row(
				str(id),
				entry['data']['category']             or 'N/A',
				entry['data']['name']                 or 'N/A',
				entry['data']['username']             or 'N/A',
				entry['data']['url']                  or 'N/A',
				entry['data']['notes'].split("\n")[0] or 'N/A',
			)

		console.print(table)

		#! This raises an exception when using 'console.print(table)'
		#! IndexError: list index out of range
		#~ table.rows.clear()

		pause()
		index += rows_per_page


def update_entries() -> None:
	"""
	Updates an existing entry in the password manager.
	"""

	index = int(input("Entry id: "))
	entry = password_manager.entries[index].copy()

	choice = input("Update or Remove (U/r)? ")

	if choice.lower() == "r":
		password_manager.remove_entry_by_index(index)
		print("\nEntry password removed successfuly!")
		pause()
		return None

	print()

	keys = ['username', 'url', 'name', 'category']
	for key in keys:
		old_value = entry['data'][key]
		prompt = "{key} ({old_value}): ".format(
			key=key.capitalize() if key != 'url' else key.upper(),
			old_value=old_value or 'N/A'
		)
		new_value = input(prompt) or old_value
		entry['data'][key] = new_value

	choice = input("\nUpdate the password (y/N)? ")

	if choice.lower() in ("y", "yes"):
		choice = input("Generate password randomly (Y/n)? ")

		if choice.lower() in ("n", "no"):
			print()
			password = getpass("Password: ")

		else:
			policy = {'digit': 1, 'lowercase': 1, 'uppercase': 1, 'special': 1} #?
			password = genpass(32, policy) #?

		entry['data']['password'] = password

	choice = input("\nUpdate the notes (y/N)? ")

	if choice.lower() in ("y", "yes"):
		print("Enter your notes (press 'Ctrl+D' to finish):\n") #?

		notes = []
		while True:
			try:
				notes.append(input("Add note : "))

			except EOFError:
				print()
				break

		entry['data']['notes'] = "\n".join(notes)

	choice = input("\nSave to password manager (Y/n)? ")

	if choice.lower() not in ("n", "no"):
		entry['meta']['last-update'] = time.strftime("%a %b %H:%M:%S %Z %Y")
		password_manager.entries[index] = entry


def password_manager_menu() -> None:
	"""
	Displays the password manager menu, allowing user to modify the vault.
	"""

	choice = input("> ")
	print()

	if choice == "1":
		create_entry()

	elif choice == "2":
		show_entries()

	elif choice == "3":
		update_entries()

	elif choice == "0":
		print("Sync the vault ... ", end=''); sys.stdout.flush()
		password_manager.sync_vault()

	else:
		raise ValueError(f"Invalid choice: '{choice}'")


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

			except EOFError:
				pass

			except KeyboardInterrupt:
				print()
				sys.exit(0)

			except Exception as xerr:
				error = xerr

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

		elif level == 2:
			try:
				password_manager = import_vault_menu()
				level = 3

			except EOFError:
				pass

			except KeyboardInterrupt:
				level = 0

			except Exception as xerr:
				error = xerr

		elif level == 3:
			try:
				password_manager_menu()

			except EOFError:
				pass

			except KeyboardInterrupt:
				pass

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
