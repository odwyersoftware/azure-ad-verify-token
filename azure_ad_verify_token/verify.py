import logging

import requests
import jwt

from .crypto import rsa_pem_from_jwk

logger = logging.getLogger(__name__)


class AzureVerifyTokenError(Exception):
    pass


class InvalidAuthorizationToken(AzureVerifyTokenError):
    def __init__(self, details=''):
        super().__init__(f'Invalid authorization token: {details}')


def verify_jwt(*, token, valid_audiences, jwks_uri, issuer):
    public_key = get_public_key(token=token, jwks_uri=jwks_uri)
    try:
        decoded = jwt.decode(
            token,
            public_key,
            verify=True,
            algorithms=['RS256'],
            audience=valid_audiences,
            issuer=issuer,
        )
    except jwt.exceptions.PyJWTError as exc:
        raise InvalidAuthorizationToken(exc.__class__.__name__)
    else:
        return decoded


def get_kid(token):
    headers = jwt.get_unverified_header(token)
    if not headers:
        raise InvalidAuthorizationToken('headers missing')
    try:
        return headers['kid']
    except KeyError:
        raise InvalidAuthorizationToken('kid missing from headers')


def get_jwk(kid, jwks_uri):
    resp = requests.get(jwks_uri)
    if not resp.ok:
        raise AzureVerifyTokenError(
            f'Received {resp.status_code} response code from {jwks_uri}'
        )
    try:
        jwks = resp.json()
    except (ValueError, TypeError):
        raise AzureVerifyTokenError(
            f'Received malformed response from {jwks_uri}'
        )
    for jwk in jwks.get('keys'):
        if jwk.get('kid') == kid:
            return jwk
    raise InvalidAuthorizationToken('kid not recognized')


def get_public_key(*, token, jwks_uri):
    kid = get_kid(token)
    jwk = get_jwk(kid=kid, jwks_uri=jwks_uri)
    return rsa_pem_from_jwk(jwk)
