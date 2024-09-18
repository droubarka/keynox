
import os, sys

from time import sleep

from vault import Vault

CLEAR = "cls" if os.name == "nt" else "clear"
defcode, redcode = '\033[0m', '\033[91m'

def show_error(errorlevel: int, *args, **kwargs) -> int:
	if errorlevel == 0:
		sleep(0.1)
		print(f"{redcode}[!] Invalid option. Please try again.\n", file=sys.stderr)
	elif errorlevel == 100:
		print(f"{redcode}{kwargs['filename']} already exists.", file=sys.stderr)
	elif errorlevel == 200:
		sleep(0.1)
		print(f"{redcode}[!] `{kwargs['filename']}` file not found. Please try again.\n", file=sys.stderr)
	else:
		input("XXX")
	print(defcode, end='')
	return 0

def show_logo() -> None:
	# Displays the Keynox logo
	with open('./cli/keynox-logo.ascii') as file:
		print(file.read())

def show_menu(level: int) -> None:
	os.system(CLEAR); show_logo()
	# Displays the menu at the specified level
	with open(f'./cli/menu/menu-{level}.x') as file:
		print(file.read())

def help() -> None:
	pass

def about() -> None:
	pass

def menu() -> None:
	level = errorlevel = 0
	while True:
		show_menu(level)


		if level == 0:
			if errorlevel == 1:
				errorlevel = show_error(0)

			choice = input("> ")

			if choice in ("1", "2"):
				level = int(choice)
			elif choice.lower() in ("0", "exit", "quit"):
				break
			else:
				errorlevel = 1

		elif level == 1:
			try:
				filename = input("Enter file in which to save the vault: ")

				if os.path.isfile(filename):
					show_error(100, filename=filename)

					choice = input("Overwrite (y/N)? ")
					if choice.lower() in ("y", "yes"):
						errorlevel = 2
				else:
					errorlevel = 2

				if errorlevel == 2:
					vault = Vault(filename); vault.store(data=[])
					errorlevel = 0
					level = 3
			except KeyboardInterrupt:
				level = 0
			except:
				show_error(-1024)
				pass
		elif level == 2:
			try:
				if errorlevel == 1:
					errorlevel = show_error(200, filename=filename)

				filename = input("Enter the file of the vault to import: ")
				if os.path.isfile(filename):
					vault = Vault(filename); vault.retrieve()
					level = 3
				else:
					errorlevel = 1
			except KeyboardInterrupt:
				level = 0
			except:
				show_error(-1024)
				pass
		elif level == 3:
			try:
				input("what's next? ")
				level = -1
			except:
				pass
		elif level == -1:
			input("[!] not finished yet.")
			pass

def main():
	try:
		menu()
	except KeyboardInterrupt:
		print()

if __name__ == "__main__": main()
