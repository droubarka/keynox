
import sys

from time import sleep


def show_error(errorlevel: int, **args) -> int:
	defcode, redcode = '\033[0m', '\033[91m' #?

	sys.stderr.write(f"{redcode}")

	if errorlevel == -99:
		sys.stderr.write("[#?] XError: {}\n".format(args["error"]))
		sys.exit(1)

	elif errorlevel == 400:
		sys.stderr.write("[!] Invalid choice.\n")
	elif errorlevel == 401:
		sys.stderr.write("[!] PermissionError: {}\n".format(args["filename"]))
	elif errorlevel == 402:
		sys.stderr.write("[!] IsADirectoryError: {}\n".format(args["filename"]))
	elif errorlevel == 403:
		sys.stderr.write("\n[!] Already exists: {}\n".format(args["filename"]))
	elif errorlevel == 404:
		sys.stderr.write("[!] FileNotFoundError: {}\n".format(args["filename"]))

	sleep(0.1)
	sys.stderr.write(f"{defcode}\n")
	return 200
