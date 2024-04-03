import json
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urljoin

from ninja import NinjaAPI
from ninja.openapi.docs import HttpRequest, HttpResponse, Swagger, _csrf_needed, _render_cdn_template
from ninja.types import DictStrAny

from ninja_oauth2.openapi.utils import get_oauth2_redirect_url

ABS_TPL_PATH = Path(__file__).parent.parent / "templates/ninja_oauth2/"


class SwaggerOAuth2(Swagger):
    template_cdn = str(ABS_TPL_PATH / "swagger_cdn.html")
    default_settings = {
        "layout": "BaseLayout",
        "deepLinking": True,
    }

    def __init__(self, settings: Optional[DictStrAny] = None, auth: Optional[DictStrAny] = None):
        self.auth = auth
        super().__init__(settings)

    def render_page(self, request: HttpRequest, api: "NinjaAPI", **kwargs: Any) -> HttpResponse:
        self.settings["url"] = self.get_openapi_url(api, kwargs)

        if self.auth:
            self.settings["oauth2RedirectUrl"] = get_oauth2_redirect_url(api.docs_url)

        context = {
            "swagger_settings": json.dumps(self.settings, indent=1),
            "api": api,
            "add_csrf": _csrf_needed(api),
            "add_auth": bool(self.auth),
            "swagger_auth": json.dumps(self.auth, indent=1),
        }
        return _render_cdn_template(request, self.template_cdn, context)
