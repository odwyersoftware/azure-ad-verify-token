from http.client import OK, INTERNAL_SERVER_ERROR, BAD_REQUEST, FORBIDDEN
import json

import jwt
import pytest

from azure_ad_verify_token import (
    verify_jwt,
    InvalidAuthorizationToken,
    AzureVerifyTokenError,
)

MODULE = 'azure_ad_verify_token.verify'
APP_ID = 'b74cd13f-8f79-4c98-b748-7789ecb1111d5'
ISS = (
    'https://exampletenant.b2clogin.com'
    '/90867afa-24e7-40e9-9d27-74bb598zzzzc/v2.0/'
)
JWKS_URI = (
    'https://exampletenant.b2clogin.com/exampletenant.onmicrosoft.com/'
    'B2C_1_app_sign_in/discovery/v2.0/keys'
)


@pytest.fixture
def mock_azure_service_jwks_uri_ok_resp(requests_mock):
    requests_mock.get(
        JWKS_URI,
        text=json.dumps(
            {
                'keys': [
                    {
                        'kid': 'X5eXk4xyojNFum1kl2Ytv8dlNP4-c57dO6QGTVBwaNk',
                        'nbf': 1493763266,
                        'use': 'sig',
                        'kty': 'RSA',
                        'e': 'AQAB',
                        'n': (
                            'tVKUtcx_n9rt5afY_2WFNvU6PlFMggCatsZ3l4RjKxH0jgdL'
                            'q6CScb0P3ZGXYbPzXvmmLiWZizpb-h0qup5jznOvOr-Dhw99'
                            '08584BSgC83YacjWNqEK3urxhyE2jWjwRm2N95WGgb5mzE5X'
                            'mZIvkvyXnn7X8dvgFPF5QwIngGsDG8LyHuJWlaDhr_EPLMW4'
                            'wHvH0zZCuRMARIJmmqiMy3VD4ftq4nS5s8vJL0pVSrkuNojto'
                            'kp84AtkADCDU_BUhrc2sIgfnvZ03koCQRoZmWiHu86SuJZYk'
                            'DFstVTVSR0hiXudFlfQ2rOhPlpObmku68lXw-7V-P7jwrQ'
                            'RFfQVXw'
                        ),
                    }
                ]
            }
        ),
        status_code=OK,
    )
    yield


@pytest.fixture
def azure_access_token():
    return (
        'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ilg1ZVhrNHh5b2pORnVtMWts'
        'Mll0djhkbE5QNC1jNTdkTzZRR1RWQndhTmsifQ.eyJle'
        'HAiOjE1OTE4MDQyMzgsIm5iZi'
        'I6MTU5MTgwMDYzOCwidmVyIjoiMS4wIiwiaXNzIjoiaH'
        'R0cHM6Ly9qaGhkZXYuYjJjbG9'
        'naW4uY29tLzkwODY3YWZhLTI0ZTctNDBlOS05ZDI3LTc'
        '0YmI1OTg1YzE4Yy92Mi4wLyIs'
        'InN1YiI6ImUwN2JiYzUzLWI4MTItNDU3Mi05ZWRjLTRi'
        'NWQ0YWM4ODQ0NyIsImF1ZCI6I'
        'mI3NGNkMTNmLThmNzktNGM5OC1iNzQ4LTc3ODllY2I4O'
        'DFkNSIsImlhdCI6MTU5MTgwMDY'
        'zOCwiYXV0aF90aW1lIjoxNTkxODAwNjM4LCJnaXZlbl9'
        'uYW1lIjoiUmljaGFyZCIsImZhb'
        'WlseV9uYW1lIjoiRXhwIEFkbWluIiwiZW1haWxzIjpbI'
        'nJvXHUwMDI3ZHd5ZXIrZXhwYWR'
        'taW5AamF3Ym9uZWhlYWx0aC5jb20iXSwidGZwIjoiQjJ'
        'DXzFfamhoX3NpZ25faW4ifQ.aa'
        'jznqUZOz1H_yL237GfcwyOWSAa59bRMZ_tRhdhF_4-xz'
        'm9Vny8qXYxnLg71xl7XKTkI8gX'
        'eDzw7Q4J7A2IC664fRv9Iz4UCM7go9iB01-zMLmRUt69'
        'ZIGdwYpUPKAfeRtxlMLFoyu3wv'
        'PBkMXX7qkO1EA27P2hxlrHtRncjolj9XX7bvbJatNC3b'
        'ay9YQ-Z_z9GHfKJShsjxSqtnb-'
        'ZvBCMwJqgeRrFDpSR_nW9d39PkOgteguYyuR_sXjtxC5'
        '1QnmgIJt0SsS2AfDYxnHrwLTph'
        'QXT6lHhTOYhWe3XNIRMHTU4EXwT3FVFrbvyLZR5W3amuTWBss0VeKnOO__dw'
    )


@pytest.mark.usefixtures('mock_azure_service_jwks_uri_ok_resp')
def test_returns_payload_if_token_successfully_verified(
    mocker, azure_access_token, requests_mock
):
    mocker.patch(
        f'{MODULE}.jwt.decode',
        return_value={
            'exp': 1591804238,
            'nbf': 1591800638,
            'ver': '1.0',
            'iss': ISS,
            'sub': 'e07bbc53-b812-4572-9edc-4b5d4ac88447',
            'aud': APP_ID,
            'iat': 1591800638,
            'auth_time': 1591800638,
            'given_name': 'Richard',
            'family_name': 'Exp Admin',
            'emails': ['bob@example.com'],
            'tfp': 'B2C_1_app_sign_in',
        },
    )

    data = verify_jwt(
        token=azure_access_token,
        valid_audiences=[APP_ID],
        issuer=ISS,
        jwks_uri=JWKS_URI,
    )

    assert data == {
        'exp': 1591804238,
        'nbf': 1591800638,
        'ver': '1.0',
        'iss': ISS,
        'sub': 'e07bbc53-b812-4572-9edc-4b5d4ac88447',
        'aud': APP_ID,
        'iat': 1591800638,
        'auth_time': 1591800638,
        'given_name': 'Richard',
        'family_name': 'Exp Admin',
        'emails': [mocker.ANY],
        'tfp': 'B2C_1_app_sign_in',
    }


@pytest.mark.usefixtures('mock_azure_service_jwks_uri_ok_resp')
@pytest.mark.parametrize(
    'exception',
    [
        jwt.exceptions.PyJWTError('something went wrong'),
        jwt.exceptions.InvalidSignatureError('something went wrong'),
        jwt.exceptions.InvalidIssuerError('something went wrong'),
        jwt.exceptions.InvalidAlgorithmError('something went wrong'),
        jwt.exceptions.ImmatureSignatureError('something went wrong'),
    ],
)
def test_raises_if_decode_fails(mocker, exception, azure_access_token):
    mocker.patch(
        f'{MODULE}.jwt.decode', side_effect=exception,
    )

    with pytest.raises(InvalidAuthorizationToken) as exc:
        verify_jwt(
            token=azure_access_token,
            valid_audiences=[APP_ID],
            issuer=ISS,
            jwks_uri=JWKS_URI,
        )
    exc.match(exception.__class__.__name__)


@pytest.mark.parametrize(
    'status_code', [INTERNAL_SERVER_ERROR, BAD_REQUEST, FORBIDDEN]
)
def test_raises_if_azure_server_unhappy_response(
    requests_mock, status_code, azure_access_token
):
    requests_mock.get(JWKS_URI, text='{}', status_code=status_code)

    with pytest.raises(AzureVerifyTokenError) as exc:
        verify_jwt(
            token=azure_access_token,
            valid_audiences=[APP_ID],
            issuer=ISS,
            jwks_uri=JWKS_URI,
        )

    assert exc.match(f'Received {status_code} response code from {JWKS_URI}')


def test_raises_if_azure_server_returns_non_json(
    requests_mock, azure_access_token
):
    requests_mock.get(JWKS_URI, text='', status_code=OK)

    with pytest.raises(AzureVerifyTokenError) as exc:
        verify_jwt(
            token=azure_access_token,
            valid_audiences=[APP_ID],
            issuer=ISS,
            jwks_uri=JWKS_URI,
        )

    assert exc.match(f'Received malformed response from {JWKS_URI}')
