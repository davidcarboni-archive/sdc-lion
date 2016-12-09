import components
import requests
import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


# Set up an ephemeral key-pair for this instance
key = None
if key is None:
    print("Generating ephemeral instance key-pair...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4094,
        backend=default_backend()
    )
    print("Done.")


def private_key():
    return key


def public_key():
    return key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode("ascii")
