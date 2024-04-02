from pathlib import Path

from django.http import HttpRequest, HttpResponse
from ninja.openapi.docs import render_template

ABS_TPL_PATH = Path(__file__).parent.parent / "templates/ninja_oauth2/"


def oauth2_redirect_view(request: HttpRequest) -> HttpResponse:
    template = "ninja_oauth2/oauth2-redirect.html"
    template_cdn = str(ABS_TPL_PATH / "oauth2-redirect.html")

    return render_template(request, template, template_cdn, {})
