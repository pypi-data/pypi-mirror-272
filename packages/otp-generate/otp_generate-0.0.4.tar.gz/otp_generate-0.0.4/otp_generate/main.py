import hashlib
import time


def generate_otp(secret_key, interval=None):
    _secret_key = str(secret_key)
    minutes = 60
    if interval:
        interval = interval * minutes

    if interval == 0:
        return {"error": True, "message": "0 minute was not allowed"}

    else:
        interval = 2 * minutes
    """
    Generate a time-based OTP using SHA-256 hashing algorithm.
    Args:
    secret_key (str): Secret key used for hashing.
    interval (int): Time interval in seconds for OTP validity. Default is 300 seconds (5 minutes).
    Returns:
    str: Generated OTP.
    """
    current_time = int(time.time() / interval)
    otp = hashlib.sha256((str(current_time) + _secret_key).encode()).hexdigest()
    return otp[:6]  # Return the first 6 characters as the OTP

def package_check():
    print("Hello from otp-package")
