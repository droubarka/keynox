
import string

from secrets import choice, SystemRandom


def generate_password(length: int, policy: dict) -> str:

	if length < sum(policy.values()):
		raise ValueError("Length must be greater than or equal to the sum of policy values.")

	chars = string.digits + string.ascii_letters + string.punctuation

	password = []

	for char_type, count in policy.items():
		if char_type == "digit":
			password.extend([choice(string.digits) for _ in range(count)])
		elif char_type == "lowercase":
			password.extend([choice(string.ascii_lowercase) for _ in range(count)])
		elif char_type == "uppercase":
			password.extend([choice(string.ascii_uppercase) for _ in range(count)])
		elif char_type == "special":
			password.extend([choice(string.punctuation) for _ in range(count)])
		else:
			raise ValueError(f"Invalid policy type '{char_type}' - use digit, lowercase, uppercase, special.")

	password.extend([choice(chars) for _ in range(length - sum(policy.values()))])

	SystemRandom().shuffle(password)

	return "".join(password)
