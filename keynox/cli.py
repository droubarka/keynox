
"""
Keynox CLI Program

This program provides a command-line interface for managing passwords.
"""

import os
import pyperclip
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


PROGRAM_DIR = os.path.dirname(os.path.abspath(__file__))
KEYNOX_LOGO_FILEPATH = f"{PROGRAM_DIR}/cli/keynox-logo.dat"
MENU_FILEPATH_FORMAT = f"{PROGRAM_DIR}/cli/menu/lvl-{'{}'}.dat"

password_manager = None


class Notification(Exception):
	"""
	Custom exception for notifications.
	"""

	def __init__(self, message: str=str()) -> None:
		"""
		Initializes a Notification object.
		"""

		self.message = message


	def __str__(self) -> str:
		"""
		Returns the notification message as a string.
		"""

		return self.message



def render_logo_and_menu(level: int=None) -> None: #?
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


def display_notification_message(message: Exception) -> None:
	"""
	Displays a notification message.
	"""

	sys.stdout.write(Fore.LIGHTGREEN_EX)
	sys.stdout.write(f"[+] {message}\n")
	sys.stdout.write(Fore.RESET)
	print()


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


def set_master_password() -> str:
	"""
	Sets and confirms a master password.
	"""

	master_password = getpass("\nSet Master Password: ")
	confirm_master_password = getpass("Retype Master Password: ")

	if master_password != confirm_master_password:
		raise ValueError("Sorry, master passwords do not match.")

	return master_password


def new_vault(filename: str) -> Vault:
	"""
	Creates a new vault with given filename.
	"""

	# Check if the file can be created
	open(filename, 'w').close()

	master_password = set_master_password()
	print("\n{}Creating secure vault ... {}".format(
		Fore.LIGHTYELLOW_EX,
		Fore.RESET), end='') #?
	sys.stdout.flush()

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
	print("\n{}Importing the secure vault ... {}".format(
		Fore.LIGHTYELLOW_EX,
		Fore.RESET), end='') #?
	sys.stdout.flush()

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
		raise Notification("Password entry created and saved successfully!")


def show_entries() -> None: #?
	"""
	Displays password manager entries.
	"""

	console = Console()

	len_entries = len(password_manager.entries)

	if not len_entries:
		raise Notification("No entries found.")

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

		getpass("\nPress Enter to continue ... ")
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
		raise Notification("Entry password removed successfuly!")

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


def change_master_password() -> None:
	"""
	Changes the master password.
	"""

	password_manager.vault.master_password = set_master_password()

	raise Notification("Master password changed successfuly!")


def sync_vault() -> None:
	"""
	Synchronizes the password manager's vault.
	"""

	print("{}Synchronizing the vault ... {}".format(
		Fore.LIGHTYELLOW_EX,
		Fore.RESET), end='') #?
	sys.stdout.flush()
	password_manager.sync_vault()
	raise Notification("Vault synchronized successfully!")


def reveal_password(password: str) -> None:
	"""
	Displays password exposure warning and prompts user to confirm.
	"""

	os.system('cls' if os.name == 'nt' else 'clear')

	console = Console()

	console.print("Warning: Password Exposure", style="bold yellow")
	console.print("""
| You are about to reveal your password in plain text in the terminal,
| which could put it at risk of being seen or stolen by others.
| Be aware that anyone with access to your terminal or screen may be
| able to see your password ...
""")
	console.print("SO ONLY PROCEED IN A SECURE AND TRUSTED ENVIRONMENT.", style="bold red underline")

	choice = input("\nReveal the password (y/N)? ")

	if choice.lower() in ("y", "yes"):
		print("\nPassword:", password)
		print()
		for i in range(6):
			print('\r', end='')
			console.print(f"The password will be hidden after {5-i} ...", style="bold yellow", end='')
			time.sleep(1.)
		os.system('cls' if os.name == 'nt' else 'clear')

	else:
		console.print('\nShatter your limitations and break free from password prison!', style="bold magenta")

def clip_password(password: str) -> None:
	"""
	Copy the given password to the clipboard and clear it after a certain timeout.
	"""

	os.system('cls' if os.name == 'nt' else 'clear')

	console = Console()

	console.print("Warning: Password Copying", style="bold yellow")
	console.print("""
| You are about to copy your password to the clipboard in plain text,
| which could put it at risk of being accessed or stolen by others.
| Be aware that anyone with access to your clipboard or system may be
| able to retrieve your password ...
""")
	console.print("SO ONLY PROCEED IN A SECURE AND TRUSTED ENVIRONMENT.", style="bold red underline")

	choice = input("\nCopy the password to the clipboard (y/N)? ")

	if choice.lower() in ("y", "yes"):
		pyperclip.copy(password)
		print("\nPassword copied to clipboard.")
		print()
		for i in range(6):
			print('\r', end='')
			console.print(f"The password will be cleared after {5-i} ...", style="bold yellow", end='')
			time.sleep(1.)
		pyperclip.copy('')
		os.system('cls' if os.name == 'nt' else 'clear')

	else:
		console.print('\nShatter your limitations and break free from password prison!', style="bold magenta")


def show_entry() -> None:
	"""
	"""

	index = int(input("Entry index : "))
	entry = password_manager.entries[index] #?

	print("""\
last-update : {}

category    : {}
name        : {}
username    : {}
url         : {}
note (main) : {}
""".format(
		entry['meta']['last-update']          or 'N/A',
		entry['data']['category']             or 'N/A',
		entry['data']['name']                 or 'N/A',
		entry['data']['username']             or 'N/A',
		entry['data']['url']                  or 'N/A',
		entry['data']['notes'].split('\n')[0] or 'N/A',
	))

	choice = input("Show all the notes (y/N)? ")

	if choice.lower() in ("y", "yes"):
		print('\n| '.join([''] + entry['data']['notes'].split('\n')))
		print()

	password = entry['data']['password']

	choice = input("Show the password (y/N)? ")

	if choice.lower() in ("y", "yes"):
		reveal_password(password)
		print()

	choice = input("Copy the password to the clipboard (y/N)? ")

	if choice.lower() in ("y", "yes"):
		clip_password(password)

	getpass("\nPause ... ")
	pass


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

	elif choice == "4":
		change_master_password()

	elif choice == "5":
		sync_vault()

	elif choice == "6":
		show_entry()

	elif choice == "0":
		if not password_manager.is_sync():
			print("\nSync the vault before exiting (Y/n)? ")

		else:
			pass

	else:
		raise ValueError(f"Invalid choice: '{choice}'")


def display_menu() -> None:
	"""
	Displays the menu and manages user interactions.
	"""

	global password_manager

	level = 0
	xcept = None

	while True:
		render_logo_and_menu(level)

		if xcept != None:
			if isinstance(xcept, Notification):
				display_notification_message(xcept)

			else:
				display_error_message(xcept)

			xcept = None

		if level == 0:
			try:
				level = main_menu()

			except EOFError:
				pass

			except KeyboardInterrupt:
				print()
				sys.exit(0)

			except Exception as error:
				xcept = error

		elif level == 1:
			try:
				password_manager = create_vault_menu()

				if password_manager != None:
					level = 3

			except EOFError:
				pass

			except KeyboardInterrupt:
				level = 0

			except Exception as error:
				xcept = error

		elif level == 2:
			try:
				password_manager = import_vault_menu()
				level = 3

			except EOFError:
				pass

			except KeyboardInterrupt:
				level = 0

			except Exception as error:
				xcept = error

		elif level == 3:
			try:
				password_manager_menu()

			except EOFError:
				pass

			except KeyboardInterrupt:
				pass

			except (Notification, Exception) as error:
				xcept = error

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
