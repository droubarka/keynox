
import os

from getpass import getpass

from password_manager import PasswordManager

def reboot():
	os.system('cls' if os.name == 'nt' else 'clear')
	show_logo()

def show_logo():
	keynox_logo = open('./cli/keynox-logo.ascii').read()
	print(keynox_logo)

def main():
	reboot()
	

if __name__ == "__main__":
	main()
