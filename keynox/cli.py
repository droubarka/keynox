
import os
import sys
import time

from io import open

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

	global error

	try:
		vault = Vault(filename)
		vault.store(data=[])

	except:
		error = filename
		raise

	return vault


def create_vault_menu() -> None:
	"""
	Display the create vault menu for creating a new vault.
	"""

	global error, level, errorlevel, vault

	try:
		filename = input("Enter file in which to save the vault: ")

		if os.path.isfile(filename):
			handle_error(error:=filename, errorlevel:=403) #: FileAlreadyExists

			choice = input("Overwrite (y/N)? ")

			if choice.lower() in ("y", "yes"):
				vault = new_vault(filename)
				level = 3

		else:
			vault = new_vault(filename)
			level = 3

	except KeyboardInterrupt:
		level = 0


#! Un/Stable code


def display_menu() -> None: #?

	global error, errorlevel

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
				pass

			elif level == 3:
				input()
				pass

			else:
				pass

		except KeyboardInterrupt:
			if level == 0:
				sys.exit(0)

			pass

		except PermissionError:
			errorlevel = 401
		except IsADirectoryError:
			errorlevel = 402
		except FileNotFoundError:
			errorlevel = 404
		except Exception as error:
			error, errorlevel = error, -1 #: XError


#~ ctrl-keys

#! Un/Stable code

error = None

level = 0
errorlevel = 200

vault = None

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
