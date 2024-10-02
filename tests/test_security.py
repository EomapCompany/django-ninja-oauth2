from unittest import mock
from unittest.mock import Mock, patch

import pytest
from django.http import HttpRequest
from ninja.errors import HttpError
from requests import RequestException
from requests.models import Response

from ninja_oauth2.security.oauth2 import OAuth2AuthorizationCodeBearer


class TestOAuth2AuthorizationCodeBearer:
    @pytest.fixture
    @mock.patch("ninja_oauth2.security.oauth2.OAuth2AuthorizationCodeBearer._get_public_key")
    def oauth2(self, mock_get_public_key, public_pem_key):
        mock_get_public_key.return_value = public_pem_key

        return OAuth2AuthorizationCodeBearer(
            authorization_url="https://example.com/auth",
            token_url="https://example.com/token",
            public_key_url="https://example.com/public_key",
        )

    @pytest.fixture
    @mock.patch("ninja_oauth2.security.oauth2.OAuth2AuthorizationCodeBearer._get_public_key")
    def oauth2_no_auto_error(self, mock_get_public_key, public_pem_key):
        mock_get_public_key.return_value = public_pem_key

        return OAuth2AuthorizationCodeBearer(
            authorization_url="https://example.com/auth",
            token_url="https://example.com/token",
            public_key_url="https://example.com/public_key",
            auto_error=False,
        )

    def test_init(self, oauth2):
        assert oauth2.public_key_url == "https://example.com/public_key"
        assert oauth2.auto_error is True
        assert hasattr(oauth2, "public_key")
        assert hasattr(oauth2, "openapi_flows")

    @patch("requests.get")
    def test_get_public_key_failure(self, mock_get, oauth2):
        mock_get.side_effect = RequestException()

        with pytest.raises(Exception):  # noqa: B017
            oauth2._get_public_key()

    @patch("requests.get")
    def test_get_public_key_success(self, mock_get, oauth2):
        mock_response = Mock(spec=Response)
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"public_key": "test_public_key"}
        mock_get.return_value = mock_response

        public_key = oauth2._get_public_key()

        assert public_key == "-----BEGIN PUBLIC KEY-----\ntest_public_key\n-----END PUBLIC KEY-----"

    def test_call_with_valid_token(self, oauth2, oauth2_token):
        request = Mock(spec=HttpRequest)
        request.headers.get.return_value = f"Bearer {oauth2_token}"

        result = oauth2(request)

        assert result["name"] == "Max Mustermann"
        assert result["preferred_username"] == "max"
        assert result["email"] == "max@mustermann.de"
        assert result["resource_access"] == {"test": {"roles": ["full-access"]}}

    def test_call_with_missing_authorization_header(self, oauth2):
        request = Mock(spec=HttpRequest)
        request.headers.get.return_value = None

        with pytest.raises(HttpError) as exc_info:
            oauth2(request)

        assert exc_info.value.status_code == 403

    def test_call_with_wrong_authorization_header(self, oauth2):
        request = Mock(spec=HttpRequest)
        request.headers.get.return_value = "just a token"

        with pytest.raises(HttpError) as exc_info:
            oauth2(request)

        assert exc_info.value.status_code == 403

    def test_call_with_another_wrong_authorization_header(self, oauth2):
        request = Mock(spec=HttpRequest)
        request.headers.get.return_value = "bearer"

        with pytest.raises(HttpError) as exc_info:
            oauth2(request)

        assert exc_info.value.status_code == 403

    def test_call_with_invalid_token(self, oauth2):
        request = Mock(spec=HttpRequest)
        request.headers.get.return_value = "Bearer invalid_token"

        with pytest.raises(HttpError) as exc_info:
            oauth2(request)

        assert exc_info.value.status_code == 401

    def test_call_with_missing_authorization_header_no_auto_error(self, oauth2_no_auto_error):
        request = Mock(spec=HttpRequest)
        request.headers.get.return_value = None

        assert oauth2_no_auto_error(request) is None

    def test_call_with_wrong_authorization_header_no_auto_error(self, oauth2_no_auto_error):
        request = Mock(spec=HttpRequest)
        request.headers.get.return_value = "just a token"

        assert oauth2_no_auto_error(request) is None

    def test_call_with_invalid_token_no_auto_error(self, oauth2_no_auto_error):
        request = Mock(spec=HttpRequest)
        request.headers.get.return_value = "Bearer invalid_token"

        assert oauth2_no_auto_error(request) is None
