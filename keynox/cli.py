
import os

from time import sleep


def show_logo():
	# Displays the Keynox logo
	print(open('./cli/keynox-logo.ascii').read())

def show_menu(level: int=0):
	# Displays the menu at the specified level
	print(open(f'./cli/menu/menu-{level}.x').read())


# reboot section
clear = ["clear", "cls"][os.name == "nt"]
defcode, redcode = '\033[0m', '\033[91m'


def menu():
	level = 0
	errorlevel = 0
	while True:
		os.system(clear)
		show_logo()
		show_menu(level)

		if errorlevel == 1:
			sleep(0.1)
			print(f"{redcode}[!] Invalid option. Please try again.\n{defcode}")
			errorlevel = 0
		choice = input("> ")
		if choice.lower() in ("0", "exit", "quit"):
			break

		if level == 0:
			if choice == "1":
				pass #create
			elif choice == "2":
				pass #import
			else:
				errorlevel = 1
		else:
			pass
	return 0;

def main(): menu()

if __name__ == "__main__": main()
