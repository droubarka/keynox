
import os, sys

from time import sleep

from vault import Vault


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
				errorlevel = 0
				sleep(0.1)
				print(f"{redcode}[!] Invalid option. Please try again.\n{defcode}")

			choice = input("> ")

			if choice in ("1", "2"):
				level = int(choice)
			elif choice.lower() in ("0", "exit", "quit"):
				break
			else:
				errorlevel = 1

		elif level == 1:
			print("Enter file in which to save the vault:")
			try:
				file_path = input("> ")
				if os.path.isfile(file_path):
					print(f"{file_path} already exists.", file=sys.stderr)
					choice = input("Overwrite (y/N)? ")
					if choice.lower() in ("y", "yes"):
						vault = Vault(file_path)
						vault.store(data={})
				else:
					vault = Vault(file_path)
					vault.store(data={})
			except KeyboardInterrupt:
				level = 0

# reboot section
CLEAR = "cls" if os.name == "nt" else "clear"
defcode, redcode = '\033[0m', '\033[91m'

def main():
	try:
		menu()
	except KeyboardInterrupt:
		print()

if __name__ == "__main__": main()
