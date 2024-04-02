"""Django Ninja - Fast Django REST framework"""

__version__ = "1.1.0"

from ninja_oauth2.main import NinjaAPIOAuth2
from ninja_oauth2.openapi.docs import SwaggerOAuth2

__all__ = [
    "NinjaAPIOAuth2",
    "SwaggerOAuth2"
]
