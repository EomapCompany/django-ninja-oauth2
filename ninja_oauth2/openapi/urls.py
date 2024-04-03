from functools import partial
from typing import TYPE_CHECKING, Any, List

from django.urls import path
from ninja.openapi.views import openapi_json, openapi_view

from ninja_oauth2.openapi.utils import get_oauth2_redirect_url
from ninja_oauth2.openapi.views import oauth2_redirect_view

if TYPE_CHECKING:
    from ninja import NinjaAPI  # pragma: no cover


def get_openapi_urls(api: "NinjaAPI") -> List[Any]:
    result = []

    if api.openapi_url:
        view = partial(openapi_json, api=api)
        if api.docs_decorator:
            view = api.docs_decorator(view)  # type: ignore
        result.append(
            path(api.openapi_url.lstrip("/"), view, name="openapi-json"),
        )

        assert (
                api.openapi_url != api.docs_url
        ), "Please use different urls for openapi_url and docs_url"

        if api.docs_url:
            view = partial(openapi_view, api=api)
            if api.docs_decorator:
                view = api.docs_decorator(view)  # type: ignore
            result.append(
                path(api.docs_url.lstrip("/"), view, name="openapi-view"),
            )

            redirect_view = partial(oauth2_redirect_view, api=api)
            redirect_url = get_oauth2_redirect_url(api.docs_url)
            result.append(
                path(redirect_url, redirect_view, name="openapi-redirect-view"),
            )

    return result
