
import sys

def show_error(errorlevel: int, **argv):
	defcode, redcode = '\033[0m', '\033[91m' #?

	print(f"{redcode}[!] ", end='', file=sys.stderr)

	if errorlevel == -99:
		input("#? XError: ???")

	elif errorlevel == 400:
		print(f"Invalid choice: {args['choice']}", file=sys.stderr)
	elif errorlevel == 401:
		print(f"PermissionError: {args['filename']}", file=sys.stderr)
	elif errorlevel == 402:
		print(f"IsADirectoryError: {args['filename']}", file=sys.stderr)
	elif errorlevel == 403:
		print(f"Already exists: {args['filename']}", file=sys.stderr)
