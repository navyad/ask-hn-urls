import argparse
from urllib.parse import urlparse


def is_ask_hn_url(url: str) -> bool:
    parse_result = urlparse(url)
    is_scheme = parse_result.scheme in ["https", "http"]
    is_netloc = parse_result.netloc == "news.ycombinator.com"
    is_path = parse_result.path == "/item"
    try:
        _ref, _post_id = parse_result.query.split("id=")
    except ValueError:
        is_post_id = False
    else:
        is_post_id = str.isdigit(_post_id)
    return all([is_scheme, is_netloc, is_path, is_post_id])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Ask:HN post urls')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', type=str, help='url of post')
    args = parser.parse_args()

    if not is_ask_hn_url(url=args.url):
        print("It is not Ask:HN url")
    else:
        pass
