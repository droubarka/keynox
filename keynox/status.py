
import sys

from time import sleep

def show_error(errorlevel: int, **args) -> int:
	defcode, redcode = '\033[0m', '\033[91m' #?

	print("{}[!] ".format(redcode), end='', file=sys.stderr)

	if errorlevel == -99:
		print("#? XError: {}".format(args["error"]), file=sys.stderr)
		sys.exit(1)

	elif errorlevel == 400:
		print("Invalid choice.", file=sys.stderr)
	elif errorlevel == 401:
		print("PermissionError: {}".format(args["filename"]), file=sys.stderr)
	elif errorlevel == 402:
		print("IsADirectoryError: {}".format(args["filename"]), file=sys.stderr)
	elif errorlevel == 403:
		print("Already exists: {}".format(args["filename"]), file=sys.stderr)
	elif errorlevel == 404:
		print("FileNotFoundError: {}".format(args["filename"]), file=sys.stderr)

	sleep(0.1)
	print(defcode, file=sys.stderr)
	return 200
