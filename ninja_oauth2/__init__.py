"""Django Ninja OAuth2 library"""

__version__ = "0.1.6"

from ninja_oauth2.main import NinjaAPIOAuth2
from ninja_oauth2.openapi.docs import SwaggerOAuth2

__all__ = ["NinjaAPIOAuth2", "SwaggerOAuth2"]
