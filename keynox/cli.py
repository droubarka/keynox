
import os
import sys
import time

from io import open


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


def display_error_message(*args) -> None:
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

	sys.stderr.write("[!] {}".format(error_lookup[errorlevel]))

	if args:
		sys.stderr.write(": {}".format(*args)) #?

	sys.stderr.write("\n")


def handle_error() -> None:
	"""
	Handles error levels and displays appropriate error messages.
	"""

	global error, errorlevel

	redcode = '\033[91m'
	defcode = '\033[0m'

	if errorlevel == 403:
		print()

	sys.stderr.write(f"{redcode}")
	display_error_message(error)
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
		error, errorlevel = choice, 400 #: InvalidOption


#! Un/Stable code


def display_menu() -> None: #?

	while True:

		os.system('cls' if os.name == 'nt' else 'clear')

		render_logo_and_menu()

		if errorlevel != 200:
			handle_error() #?

		try:
			if level == 0:
				main_menu()
			elif level == 1:
				pass
			else:
				pass

		except KeyboardInterrupt:
			pass
		except Exception as error:
			pass


#! Un/Stable code

error = None

level = 0
errorlevel = 200

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
