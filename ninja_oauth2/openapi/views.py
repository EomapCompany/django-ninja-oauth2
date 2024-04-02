from pathlib import Path
from typing import TYPE_CHECKING, Any

from django.http import HttpRequest, HttpResponse
from ninja.openapi.docs import _render_cdn_template

if TYPE_CHECKING:
    from ninja import NinjaAPI  # pragma: no cover

ABS_TPL_PATH = Path(__file__).parent.parent / "templates/ninja_oauth2/"


def oauth2_redirect_view(request: HttpRequest, api: "NinjaAPI", **kwargs: Any) -> HttpResponse:
    template_cdn = str(ABS_TPL_PATH / "oauth2-redirect.html")

    return _render_cdn_template(request, template_cdn)
