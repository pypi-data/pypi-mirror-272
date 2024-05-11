import hashlib
import time


def generate_otp(secret_key, interval=120, length=6, only_digits=True):
    """
    Generate a time-based OTP using SHA-256 hashing algorithm.

    Args:
    secret_key (str): Secret key used for hashing.
    interval (int): Time interval in seconds for OTP validity. Default is 120 seconds (2 minutes).
    length (int): Length of OTP. Default is 6 (6 digits). Maximum 8 digits.

    Returns:
    str: Generated OTP.
    """
    length = length if length < 9 else 6
    current_time = int(time.time() / interval)
    otp_hash = hashlib.sha256((str(current_time) + secret_key).encode()).hexdigest()
    otp_numeric = ''.join(char for char in otp_hash if char.isdigit())
    otp = otp_numeric[:length] if only_digits else otp_hash[:length]  # Return the first 6 characters as the OTP
    return otp
