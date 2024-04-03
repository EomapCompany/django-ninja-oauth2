from typing import Any, Optional

import jwt
import requests
from ninja.errors import HttpError
from ninja.openapi.docs import HttpRequest
from ninja.security.base import AuthBase


class OAuth2AuthorizationCodeBearer(AuthBase):
    openapi_type = "oauth2"

    def __init__(self, authorization_url: str, token_url: str, public_key_url: str, auto_error: bool = True) -> None:
        self.public_key_url = public_key_url
        self.auto_error = auto_error
        self.public_key = self._get_public_key()
        self.openapi_flows = {
            "authorizationCode": {"scopes": {}, "authorizationUrl": authorization_url, "tokenUrl": token_url}
        }

        super().__init__()

    def __call__(self, request: HttpRequest) -> Optional[Any]:
        authorization = request.headers.get("Authorization")

        if not authorization:
            if self.auto_error:
                raise HttpError(403, "Not authenticated")
            else:
                return None

        parts = authorization.split(" ")

        if not authorization or (len(parts) != 2 and parts[0].lower() != "bearer"):
            if self.auto_error:
                raise HttpError(403, "Not authenticated")
            else:
                return None

        token = parts[1]

        try:
            token_info = jwt.decode(token, self.public_key, audience="account", algorithms=["RS256"])
        except Exception as e:
            if self.auto_error:
                raise HttpError(401, "Invalid token") from e
            else:
                return None

        return self.authenticate(request, token_info)

    def _get_public_key(self) -> str:
        try:
            response = requests.get(self.public_key_url)
            response.raise_for_status()

            content = response.json()
            public_key = content.get("public_key")

            if public_key:
                return f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
            else:
                raise ValueError("Public key not found in the response.")

        except requests.RequestException as e:
            raise Exception(f"Get public key failed with the following error: {e}.") from e

    def authenticate(self, request: HttpRequest, token_info: dict) -> Optional[Any]:
        return token_info
