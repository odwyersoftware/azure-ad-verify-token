# azure-ad-verify-token
Verify JWT issued by Azure Active Directory B2C in Python 🐍.

[![Build Status](https://travis-ci.org/ODwyerSoftware/azure-ad-verify-token.svg?branch=master)](https://travis-ci.org/ODwyerSoftware/azure-ad-verify-token) [![PyPI version](https://badge.fury.io/py/azure-ad-verify-token.svg)](https://pypi.org/project/azure-ad-verify-token/)

    Validation steps this library makes:

    1. Accepts an Azure AD B2C JWT.
    2. Extracts `kid` from unverified headers.
    3. Finds `kid` within Azure JWKS.
    4. Obtains RSA key from JWK.
    5. Calls `jwt.decode` with nessary parameters, which inturn validates:

        - Signature
        - Expiration
        - Audience
        - Issuer
        - Key
        - Algorithm

## License

![https://creativecommons.org/licenses/by-nc-nd/4.0/
](https://licensebuttons.net/l/by-nc-nd/4.0/88x31.png)

This work is licensed under a [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License](https://creativecommons.org/licenses/by-nc-nd/4.0/).

For commercial use licenses [contact us](mailto:github@odwyer.software).

## Installation

```bash
pip install azure-ad-verify-token
```

## Usage


First you'll need to get your `azure_ad_app_id`, `azure_ad_issuer` and `azure_ad_jwks_uri`. See below steps to obtain these.

1. For app id. Login to [Azure Portal](https://portal.azure.com/), navigation to Azure AD B2C, Click on the Applications section and your app id should be listed.

2. For Issuer and JWKS URI:

Under the "User Flows", note down the name of yours, this will be needed shortly.

![https://i.imgur.com/uYmghAZ.png](https://i.imgur.com/uYmghAZ.png)

Next, under Azure AD B2C, within the Applications section.

Click on "Endpoints".

Copy the endpoint with the label "OpenID Connect configuration endpoint (v2)"

It will look something like:

`https://exampletenant.b2clogin.com/exampletenant.onmicrosoft.com/<policy-name>/v2.0/.well-known/openid-configuration`

![https://i.imgur.com/3bQGZBn.png](https://i.imgur.com/3bQGZBn.png)

Now replace `<policy-name>` with the name of your User Flow from earlier

`https://exampletenant.b2clogin.com/exampletenant.onmicrosoft.com/B2C_1_app_sign_in/v2.0/.well-known/openid-configuration`

Now visit that URL in your web browser.

You should get a JSON response, note down the values for the keys 'issuer' and 'jwks_uri'.

Now you have those values you can proceed to verify a Azure generated JWT Token.

```python
from azure_ad_verify_token import verify_jwt

azure_ad_app_id = 'b74cd13f-8f79-4c98-b748-7789ecb1111d5'
azure_ad_issuer = 'https://exampletenant.b2clogin.com/0867afa-24e7-40e9-9d27-74bb598zzzzc/v2.0/'
azure_ad_jwks_uri = 'https://exampletenant.b2clogin.com/exampletenant.onmicrosoft.com/B2C_1_app_sign_in/discovery/v2.0/keys'
payload = verify_jwt(
    token='<AZURE_JWT_TO_VERIFY_HERE>',
    valid_audiences=[azure_ad_app_id],
    issuer=azure_ad_issuer,
    jwks_uri=azure_ad_jwks_uri,
    verify=True,
)

print(payload)
{'aud': 'b74cd13f-8f79-4c98-b748-7789ecb1111d5',
 'auth_time': 1591800638,
 'emails': ['bob@example.com'],
 'exp': 1591804238,
 'family_name': 'Exp Admin',
 'given_name': 'Richard',
 'iat': 1591800638,
 'iss': 'https://exampletenant.b2clogin.com/90867afa-24e7-40e9-9d27-74bb598zzzzc/v2.0/',
 'nbf': 1591800638,
 'sub': 'e07bbc53-b812-4572-9edc-4b5d4ac88447',
 'tfp': 'B2C_1_app_sign_in',
 'ver': '1.0'}
```

If something goes wrong, one of the below exceptions will be raised:

```
# If the token is found to be invalid.
azure_ad_verify_token.InvalidAuthorizationToken

# Base exception, raised if the checks which call the Azure server recieve an unhappy response.
azure_ad_verify_token.AzureVerifyTokenError
```
