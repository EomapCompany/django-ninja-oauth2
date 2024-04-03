from unittest import mock
from unittest.mock import Mock

import pytest
from ninja import Swagger
from ninja.testing import TestClient

from ninja_oauth2 import NinjaAPIOAuth2, SwaggerOAuth2
from ninja_oauth2.openapi.utils import get_oauth2_redirect_url
from ninja_oauth2.security.oauth2 import OAuth2AuthorizationCodeBearer


@pytest.fixture
def mock_response(public_pem_key):
    mock_resp = Mock()
    mock_resp.raise_for_status.side_effect = None
    mock_resp.json.return_value = {"public_key": public_pem_key}
    return mock_resp


@mock.patch("ninja_oauth2.security.oauth2.OAuth2AuthorizationCodeBearer._get_public_key")
def test_swagger_docs(mock_get_public_key, public_pem_key):
    mock_get_public_key.return_value = public_pem_key

    oauth2 = OAuth2AuthorizationCodeBearer(
        authorization_url="https://test.com/auth/realms/test/protocol/openid-connect/auth",
        token_url="https://test.com/auth/realms/test/protocol/openid-connect/token",
        public_key_url="https://test.com/auth/realms/test"
    )

    api = NinjaAPIOAuth2(
        docs=SwaggerOAuth2(
            auth={"clientId": "test"}
        ), auth=oauth2)

    assert isinstance(api.docs, Swagger)

    client = TestClient(api)

    response = client.get("/docs")
    assert response.status_code == 200
    assert '"oauth2RedirectUrl": "docs/oauth2-redirect.html"' in str(response.content)
    assert '"clientId": "test"' in str(response.content)


@mock.patch("ninja_oauth2.security.oauth2.OAuth2AuthorizationCodeBearer._get_public_key")
def test_swagger_oauth2_redirect(mock_get_public_key, public_pem_key):
    mock_get_public_key.return_value = public_pem_key

    oauth2 = OAuth2AuthorizationCodeBearer(
        authorization_url="https://test.com/auth/realms/test/protocol/openid-connect/auth",
        token_url="https://test.com/auth/realms/test/protocol/openid-connect/token",
        public_key_url="https://test.com/auth/realms/test"
    )

    api = NinjaAPIOAuth2(
        docs=SwaggerOAuth2(
            auth={"clientId": "test"}
        ), auth=oauth2)

    assert isinstance(api.docs, Swagger)

    client = TestClient(api)

    response = client.get("/docs/oauth2-redirect.html")
    assert response.status_code == 200


def test_get_oauth2_redirect_url():
    docs_url = "/docs/"

    result = get_oauth2_redirect_url(docs_url)

    assert result == "docs/oauth2-redirect.html"
