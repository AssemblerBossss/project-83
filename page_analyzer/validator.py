from urllib.parse import urlparse
from validators import url


def is_valid_url(url_to_validate) -> bool:
    return 255 > len(url_to_validate) > 0 and url(url_to_validate)


def normalize_url(url_to_normalize) -> str:
    parsed_url = urlparse(url_to_normalize)
    normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return normalized_url
