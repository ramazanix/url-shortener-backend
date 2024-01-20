import secrets


def shortify_url(url: str) -> str:
    short_name = secrets.token_urlsafe(6)
    return short_name
