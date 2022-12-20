## ask-hn-urls
Find URLs posted as a part of comments over on [Ask HN](https://news.ycombinator.com/ask) section.

### Idea
Posts like where people do post urls links as part of comments, like
[Ask HN: How Can I Learn Programming From The Ground Up?](https://link-url-here.org)
, gathering all urls for posts like this would be useful.

### Setup
* Install 3.11 or newer.
* Install pipenv
* Run ```pipenv install``` and ```pipenv shell```

### Usage
```
python askhn.py --url https://news.ycombinator.com/item\?id\=1475575
```
