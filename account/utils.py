import secrets


def generate_otp_code():
    return ''.join(secrets.choice("0123456789") for _ in range(5))
