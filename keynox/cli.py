
import os

from time import sleep

from vault import Vault


def show_logo() -> None:
	# Displays the Keynox logo
	with open('./cli/keynox-logo.ascii') as file:
		print(file.read())

def show_menu(level: int) -> None:
	# Displays the menu at the specified level
	with open(f'./cli/menu/menu-{level}.x') as file:
		print(file.read())


def menu() -> None:
	level = errorlevel = 0
	while True:
		os.system(CLEAR); show_logo(); show_menu(level)

		if level == 0:
			if errorlevel == 1:
				errorlevel = 0
				sleep(0.1)
				print(f"{redcode}[!] Invalid option. Please try again.\n{defcode}")

			choice = input("> ")

			if choice.lower() in ("0", "exit", "quit"):
				break
			if choice.lower() in ("?", "help"):
				print("\n#? help"); sleep(0.5)

			elif choice == "1":
				level = 1
			elif choice == "2":
				level = 2
			else:
				errorlevel = 1

		elif level == 1:
			print("Enter file in which to save the vault:")
			try:
				file_path = input("\t> ")
				if os.path.isfile(file_path):
					choice = input("The file already exists. Overwrite (y/N): ") or "no"
					if choice.lower() in ("y", "yes"):
						pass
				else:
					pass
			except:
				level = 0

# reboot section
CLEAR = "cls" if os.name == "nt" else "clear"
defcode, redcode = '\033[0m', '\033[91m'

def main():
	try:
		menu()
	except:
		print()
		pass

if __name__ == "__main__": main()
