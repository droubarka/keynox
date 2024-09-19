
import os, sys

from time import sleep

from vault import Vault

def level_0() -> tuple:
	try:
		choice = input("> ")

		if choice in ("1", "2"):
			level = int(choice)
		elif choice.lower() in ("0", "exit", "quit"):
			raise KeyboardInterrupt
		else:
			# Set error level to 100 if invalid choice
			errorlevel = 100

	except KeyboardInterrupt:
		raise
	except Exception as error:
		show_error(-99, error=error) #?
	finally:
		return errorlevel, level


def menu() -> None:
	errorlevel = 0
	level = 0
	while True:
		if errorlevel in (100,):
			errorlevel = show_error(errorlevel)

		try:
			if level == 0:
				errorlevel, level = level_0()

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



def _menu() -> None:
	level = errorlevel = 0
	choice = filename = str()
	vault = Vault(filename)

	while True:
		show_menu(level)

		# level-0: Main menu
		if level == 0: pass

		# level-1: Create a new vault
		elif level == 1:
			try:
				if errorlevel in (201, 202, 203):
					errorlevel = show_error(errorlevel, filename=filename)

				filename = input("Enter file in which to save the vault: ")

				if os.path.isfile(filename):

					# Show error message if file exists
					show_error(200, filename=filename)

					choice = input("Overwrite (y/N)? ")

					if choice.lower() in ("y", "yes"):
						errorlevel = 10

				else:
					# Set error level to 10 if file does not exist
					errorlevel = 10

				# Create a new vault if file does not exist
				if errorlevel == 10:
					vault = Vault(filename)
					vault.store(data=[])
					level = 3
					errorlevel = 0

			except KeyboardInterrupt:
				# Go back to main menu if user interrupts
				level = 0
			except FileNotFoundError:
				errorlevel = 201
			except PermissionError:
				errorlevel = 202
			except IsADirectoryError:
				errorlevel = 203
			except Exception as error:
				show_error(-99, error=error, **globals())

		# level-2: Import a vault
		elif level == 2:
			try:
				if errorlevel in (201, 202, 203):
					errorlevel = show_error(errorlevel, filename=filename)

				filename = input("Enter the file of the vault to import: ")

				if os.path.isfile(filename):
					vault = Vault(filename)
					vault.retrieve()
					level = 3
				else:
					# Try to open the file (this will raise an exception)
					open(filename)

			except KeyboardInterrupt:
				# Go back to main menu if user interrupts
				level = 0
			except FileNotFoundError:
				errorlevel = 201
			except PermissionError:
				errorlevel = 202
			except IsADirectoryError:
				errorlevel = 203
			except Exception as error:
				show_error(-99, error=error, **globals())

		# level-3: Next step (not implemented)
		elif level == 3:
			try:
				if errorlevel == 100:
					errorlevel = show_error(errorlevel)

				choice = input("> ")

				if choice == "1":
					level = -1
				elif choice in ("2", "3", "4"):
					level = -1
				else:
					# Set error level to 100 if invalid choice
					errorlevel = 100

			except KeyboardInterrupt as error:
				pass
			except Exception as error:
				show_error(-99, error=error, **globals())

		# blackhole: Not finished yet
		elif level == -1:
			input("[!] not finished yet.")
			pass

def show_error(errorlevel: int, **args) -> None:

	defcode, redcode = '\033[0m', '\033[91m'

	print(f"{redcode}", end='', file=sys.stderr)

	if errorlevel == -99:
		input("XError: ???")

	elif errorlevel == 100:
		print("[!] Invalid option. Please try again.", file=sys.stderr)
	elif errorlevel == 200:
		print(file=sys.stderr)
		print("[!] The file already exists.", file=sys.stderr)
	elif errorlevel == 201:
		print("[!] FileNotFoundError: `{file}`".format(file=args["filename"]), file=sys.stderr)
	elif errorlevel == 202:
		print("[!] PermissionError: `{file}`".format(file=args["filename"]), file=sys.stderr)
	elif errorlevel == 203:
		print("[!] IsADirectoryError: `{file}`".format(file=args["filename"]), file=sys.stderr)

	sleep(0.1)
	print(defcode, file=sys.stderr)

def show_logo() -> None:
	# Displays the Keynox logo
	with open('./cli/keynox-logo.ascii') as file:
		print(file.read())

def show_menu(level: int) -> None:
	# Clear the terminal screen
	os.system("cls" if os.name == "nt" else "clear")
	# Displays the Keynox logo
	show_logo()
	# Displays the menu at the specified level
	try:
		with open(f'./cli/menu/menu-{level}.x') as file:
			print(file.read())
	except Exception:
		pass

