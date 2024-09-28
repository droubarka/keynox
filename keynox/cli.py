
from io import open


KEYNOX_LOGO_FILEPATH = './cli/keynox-logo.dat'
MENU_FILEPATH_FORMAT = './cli/menu/lvl-{}.dat'


def render_logo_and_menu() -> None:
	"""
	Renders the logo and menu files.
	"""

	try:
		with open(KEYNOX_LOGO_FILEPATH, 'rt') as file:
			print(file.read())

	except FileNotFoundError: Ellipsis

	if password_manager != None:
		print(f"\tVault: {password_manager.vault.filename}")
		is_synchronized = password_manager.sync_fingerprint == password_manager.calculate_sync_fingerprint()
		print(f"\tSynchronized: {is_synchronized}", end=' | ')
		print(f"Entries: {len(password_manager.entries)}", end='')
		print("\n")

	try:
		with open(MENU_FILEPATH_FORMAT.format(level), 'rt') as file:
			print(file.read())

	except FileNotFoundError: Ellipsis


def display_error_message() -> None:
	"""
	Displays an error message based on the given error level.
	"""

	pass


level = 0

password_manager = None
