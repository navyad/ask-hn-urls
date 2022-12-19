import argparse
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, element


SCHEMES = ["https", "http"]
BASE_URL = "news.ycombinator.com"
PATH = "/item"
CONTENT_TYPE = 'text/html; charset=utf-8'


def is_ask_hn_url(url: str) -> bool:
    parse_result = urlparse(url)
    is_scheme = parse_result.scheme in SCHEMES
    is_netloc = parse_result.netloc == BASE_URL
    is_path = parse_result.path == PATH
    try:
        _ref, _post_id = parse_result.query.split("id=")
    except ValueError:
        is_post_id = False
    else:
        is_post_id = str.isdigit(_post_id)
    return all([is_scheme, is_netloc, is_path, is_post_id])


def fetch_post(url: str) -> str:
    response = requests.get(url=url)
    if not response.status_code == 200:
        print(f"request to {url} failed")
        return
    assert response.headers['Content-Type'] == CONTENT_TYPE
    return response.text


def comment_tags(page_source: str) -> element.ResultSet:
    soup = BeautifulSoup(page_source, 'html.parser')
    return soup.find_all(name='span', attrs={"class": "commtext c00"})


def href_tags(tag: element.Tag) -> element.ResultSet:
    return tag.find_all("a", href=True)


def scrap_post(page_source: str):
    for tag in comment_tags(page_source):
        for url_tag in href_tags(tag):
            print(url_tag.text)


def main() -> int:
    parser = argparse.ArgumentParser(prog='Ask:HN post urls')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', type=str, help='url of post')
    args = parser.parse_args()
    url = args.url

    if not is_ask_hn_url(url=url):
        print(f"{url}: Not a Ask:HN url")
    else:
        print(f"fetching {url} ...")
        page_source = fetch_post(url)
        print("scraping post ...")
        scrap_post(page_source)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
