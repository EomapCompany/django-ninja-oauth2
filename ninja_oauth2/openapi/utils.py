def get_oauth2_redirect_url(docs_url: str) -> str:
    return f"{docs_url.rstrip("/")}/oauth2-redirect.html".lstrip("/")
