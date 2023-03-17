import argparse
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, element
from rich.console import Console
from rich.table import Table
from rich import box


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
    comments = soup.find_all(name='span', attrs={"class": "commtext c00"})
    return soup.title.text, comments


def href_tags(tag: element.Tag) -> element.ResultSet:
    return tag.find_all("a", href=True)


def scrap_post(page_source: str) -> set['str']:
    title, comments = comment_tags(page_source)
    return title, (
        url_tag.attrs['href'] for tag in comments for url_tag in href_tags(tag))


def display(title_color: str, title: str, box_items: set) -> None:
    table = Table(box=box.ROUNDED)
    table.add_column(title, style=title_color)
    for item in box_items:
        table.add_row(item)
    console = Console()
    console.print(table)


def main() -> int:
    parser = argparse.ArgumentParser(prog='python3 askhn')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', type=str, help='url of post')
    args = parser.parse_args()
    url = args.url

    if not is_ask_hn_url(url=url):
        display(title_color="red", title="ERROR", box_items=[f"Not a Ask HN url: {url}"])
        return 1
    page_source = fetch_post(url)
    title, comments = scrap_post(page_source)
    display(title_color="blue", title=title, box_items=comments)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
