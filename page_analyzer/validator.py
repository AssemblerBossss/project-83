from urllib.parse import urlparse


def is_valid_url(url_to_validate) -> bool:
    return 255 > len(url_to_validate) > 0

def normalize_url(url_to_normalize) -> str:
    parsed_url = urlparse(url_to_normalize)
    normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return normalized_url




