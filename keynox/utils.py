
import string

from secrets import SystemRandom


def choices(population: list, *args, **kwargs) -> list:
	"""
	Return a k sized list of population elements chosen with replacement.

	If the relative weights or cumulative weights are not specified,
	the selections are made with equal probability.
	"""
	return SystemRandom().choices(population, *args, **kwargs)


def shuffle(x: list) -> None:
	"""
	Shuffle list x in place, and return None.
	"""
	return SystemRandom().shuffle(x)


def genpass(length: int, policy: dict) -> str:
	"""
	Generates a password based on the given policy.
	"""

	if length < sum(policy.values()):
		raise ValueError(
			"Length must be greater than or equal to the sum of policy values."
		)

	password = []

	chars = string.digits + string.ascii_letters + string.punctuation

	password.extend(
		choices(chars, k=(length - sum(policy.values())))
	)

	for char_type, count in policy.items():
		if char_type == "digit":
			password.extend(
				choices(string.digits, k=count)
			)
		elif char_type == "lowercase":
			password.extend(
				choices(string.ascii_lowercase, k=count)
			)
		elif char_type == "uppercase":
			password.extend(
				choices(string.ascii_uppercase, k=count)
			)
		elif char_type == "special":
			password.extend(
				choices(string.punctuation, k=count)
			)
		else:
			raise ValueError(
					f"Invalid policy type '{char_type}'"
					" - use digit, lowercase, uppercase or special."
			)

	shuffle(password)

	return "".join(password)
