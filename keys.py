from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from public_keys import add_key


# Set up an ephemeral key-pair for this instance
__key_pair = None


def private_key():
    return __key_pair


def public_key():
    return __key_pair.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode("ascii")


def generate_key():
    global __key_pair
    if __key_pair is None:
        print("Generating ephemeral instance key-pair...")
        __key_pair = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4094,
            backend=default_backend()
        )
        key_id = add_key(public_key())
        print(" - Public key id is: " + repr(key_id))
        print(" - Public key is:\n" + public_key())
        print("Done.")
