from cryptography.hazmat.primitives import serialization
import time
import components
from jose import jwt
import keys

JWT_ALGORITHM = 'RS256'


def encode(component, data=None):

    # Claims
    timestamp = time.time()
    claims = {
        "iss": components.NAME,
        "aud": component,
        "iat": timestamp,
        "exp": timestamp + 60
    }
    if data:
        claims["data"] = data

    # Signing key
    pem = keys.private_key().private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode("ascii")

    return jwt.encode(claims, pem, algorithm=JWT_ALGORITHM)


def decode(token):

    # Get the public key
    claims = jwt.get_unverified_claims(token)
    issuer = claims["iss"] if "iss" in claims else None
    key_id = claims["kid"] if "kid" in claims else None
    pem = components.get_key(issuer, key_id) if issuer and key_id else None

    if pem:
        # Verify the token
        payload = jwt.decode(token, pem,
                             algorithms=[JWT_ALGORITHM],
                             audience=components.NAME,
                             issuer=components.components)
        return payload["data"] if "data" in payload else None
    else:
        raise ValueError("Unable to get a public key for issuer " + issuer + " and key ID " + key_id)
