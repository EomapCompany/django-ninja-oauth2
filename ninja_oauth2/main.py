from typing import List, Union

from django.urls import URLPattern, URLResolver
from ninja import NinjaAPI
from ninja.openapi.urls import get_root_url

from ninja_oauth2.openapi.urls import get_openapi_urls


class NinjaAPIOAuth2(NinjaAPI):
    def _get_urls(self) -> List[Union[URLResolver, URLPattern]]:
        result = get_openapi_urls(self)

        for prefix, router in self._routers:
            result.extend(router.urls_paths(prefix))

        result.append(get_root_url(self))
        return result
