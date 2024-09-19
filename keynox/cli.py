
import os, sys

from time import sleep

from vault import Vault


def show_error(errorlevel: int, **args) -> None:

	defcode, redcode = '\033[0m', '\033[91m' #?

	print(f"{redcode}", end='', file=sys.stderr)

	if errorlevel == -99:
		input("#? XError: ???")

	elif errorlevel == 400:
		print("[!] Invalid option. Please try again.", file=sys.stderr)
	elif errorlevel == :
		print("[]", file=sys.stderr)

	sleep(0.1)
	print(defcode, file=sys.stderr)


def new_vault(filename: str) -> Vault:
	vault = Vault(filename)
	vault.store(data=[])
	return vault

def level_1() -> tuple:
	errorlevel = 200
	level = 1
	try:
		filename = input("Enter file in which to save the vault: ")

		if os.path.isfile(filename):
			show_error(403, filename=filename)

			choice = input("Overwrite (y/N)? ")

			if choice.lower() in ("y", "yes"):
				new_vault()

		else:
			new_vault()

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

	return errorlevel, level


def level_0() -> tuple:
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
	errorlevel = 0
	level = 0
	choice = None
	filename = None
	while True:
		# Clear the terminal screen
		os.system("cls" if os.name == "nt" else "clear")

		try:
			# Displays the Keynox logo
			with open('./cli/keynox-logo.ascii') as file:
				print(file.read())

			# Displays the menu at the specified level
			with open(f'./cli/menu/menu-{level}.x') as file:
				print(file.read())

		except FileNotFoundError:
			Ellipsis

		if errorlevel in (400,):
			errorlevel = show_error(errorlevel, choice=choice)

		if errorlevel in (401, 402, 403, 404):
			errorlevel = show_error(errorlevel, filename=filename)

		try:
			if level == 0:
				errorlevel, level = level_0()
			elif level == 1:
				errorlevel, level = level_1()
			else:
				raise KeyboardInterrupt

		except KeyboardInterrupt:
			raise
		except Exception as error:
			show_error(-99, error=error) #?


def main():
	try:
		menu()

	except KeyboardInterrupt:
		print("\n#? Exiting ...")
	except Exception as error:
		show_error(-99, error=error) #?


if __name__ == "__main__": main()
