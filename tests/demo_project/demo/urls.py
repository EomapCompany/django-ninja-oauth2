from django.contrib import admin
from django.urls import path

from ninja_oauth2 import NinjaAPIOAuth2, SwaggerOAuth2
from ninja_oauth2.security.oauth2 import OAuth2AuthorizationCodeBearer

oauth2 = OAuth2AuthorizationCodeBearer(
    authorization_url="https://auth.eomap.com/auth/realms/eomap/protocol/openid-connect/auth",
    token_url="https://auth.eomap.com/auth/realms/eomap/protocol/openid-connect/token",
    public_key_url="https://auth.eomap.com/auth/realms/eomap"
)

api = NinjaAPIOAuth2(
    docs=SwaggerOAuth2(
        auth={"clientId": "test"}
    ),
    auth=oauth2)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
