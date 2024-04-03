# Django Ninja OAuth2

**Django Ninja OAuth2** package enables support of OAuth2 / OpenID Connect "Authorization Code Flow" for your swagger
documentation.

### Requirements

- Python >= 3.8
- django >= 3.1
- pydantic >= 2.0
- Django-Ninja >= 1.1.0

## Installation

```
pip install django-ninja-oauth2
```

After installation, change settings.py file. Locally it only worked with None. On a real domain it should work with
"same-origin-allow-popups".

```Python 
# in <myapp>/settings.py
SECURE_CROSS_ORIGIN_OPENER_POLICY = None  # or "same-origin-allow-popups"
```

## Usage

Initialize NinjaAPIOAuth2 wherever you would initialize the original Django Ninja api.

Set your authorization, token and public key url

By default, if no HTTP Authorization header is provided, required for OAuth2 authentication, it will automatically cancel the request and send the client an error.

If auto_error is set to False, when the HTTP Authorization header is not available, instead of erroring out, the dependency result will be None.

```Python
from ninja_oauth2 import NinjaAPIOAuth2, SwaggerOAuth2
from ninja_oauth2.security.oauth2 import OAuth2AuthorizationCodeBearer

oauth2 = OAuth2AuthorizationCodeBearer(
    authorization_url="https://test.com/auth/realms/<realm>/protocol/openid-connect/auth",
    token_url="https://test.com/auth/realms/<realm>/protocol/openid-connect/token",
    public_key_url="https://test.com/auth/realms/<realm>",
    auto_error=True # Default True
)

api = NinjaAPIOAuth2(
    docs=SwaggerOAuth2(
        auth={"clientId": "<client_id>"}
    ),
    auth=oauth2) # Use auth for all endpoints, optional

@api.get("/add", tags=["Main"], auth=oauth2) # Use auth for specific endpoint
def add(request, a: int, b: int):
    return {"result": a + b}
```