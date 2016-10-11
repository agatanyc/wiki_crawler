import requests
import bs4
from bs4 import BeautifulSoup
from urlparse import urljoin
from urlparse import urlparse
from collections import Counter

def find_philosophy(url, visited_url=None, path_length=0, cache=None):
    """(str) -> int

    Return path length or -1 if the `url` does not lead to 
    philosophy page."""
    if visited_url == None:
        visited_url = []
    if cache == None:
        cache = {}
    r = requests.get(url)
    html_content = r.text
    philosophy_url = 'https://en.wikipedia.org/wiki/Philosophy'
    if r.url == philosophy_url:
        # Number of requests it took to get to philosophy page. 
        cache[r.url] = 0
        path = path_length
        for v in visited_url:
            cache[v] = path
            path -= 1
        return path_length
    elif cache.has_key(r.url): 
        if cache[r.url] == -1:
            return cache[r.url]
        else:
            return cache[r.url] + path_length
    # Check it have we not seen the url yet. Repeted url would indicate
    # we will never get to philosophy page.
    elif r.url in visited_url:
        cache_update(visited_url, cache)
        return -1
    else:
        link = find_link(html_content)
        # Check if the page contains link that meets the requirements.
        if link and link.attrs.has_key('href'):
            new_url = urljoin(r.url, link.attrs['href'])
            if not differrent_path(r.url, new_url):
                cache_update(visited_url, cache)
                return -1
            else:
                path_length += 1
                visited_url.append(r.url)
                # Recurse
                return find_philosophy(new_url, visited_url, path_length, cache)
        else:
            cache_update(visited_url, cache)
            return -1

def cache_update(visited_url, cache):
    for v in visited_url:
        cache[v] = -1

def find_link(html_content):
    """(str) -> bs4.element.Tag or None

    Return the first link on the main body of the article that is
    not within parenthesis or italicized.
    Since Wikipedia uses a template we assume the not
    italicized link will be in one of the `p` tag paragraphs."""
    soup = BeautifulSoup(html_content, "html.parser")
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        string = ''
        for element in p:
            if type(element) == bs4.element.NavigableString:
                string += element
            elif type(element) == bs4.element.Tag and element.name == 'a':
                if balanced_parenths(string):
                    return element
            else:
                string += element.get_text()
    return None

def find_percentage(urls):
    """(list) -> int

    Return the percentage of pages that lead to philosophy.
    """
    # n is the number of pages that lead to philosophy
    n = 0
    cache = {}
    for url in urls:
        if find_philosophy(url, cache=cache) != -1:
            n += 1
    percentage = n * 100 / len(urls)
    return percentage

def random_percentage(m):
    pages = []
    for i in range(m):
        p = 'https://en.wikipedia.org/wiki/Special:Random'
        pages.append(p)
    return find_percentage(pages)


def distribution(urls):
    """(list) -> list

    Distrbution of path lengths to reach `philosophy` page.
    Elements of `urls` are the starting url.
    """
    distr = []
    cache = {}
    for url in urls:
        r = find_philosophy(url, cache=cache)
        if r != -1:
            distr.append(r)
    return distr

def random_distribution(m):
    """(int) -> list

    Distribution of path lengths mapped to occurrence for `m` pages."""
    urls = []
    for i in range(m):
        p = 'https://en.wikipedia.org/wiki/Special:Random'
        urls.append(p)
    return Counter(distribution(urls))

def balanced_parenths(string):
    """(str) -> bool

    Return True if `string` contains the same number of opening and closing parenths, 
    otherwise False."""
    balanced = 0
    for c in string:
        if c == '(':
            balanced += 1
        elif c == ')':
            balanced -= 1
    return balanced == 0

def differrent_path(old_url, new_url):
    """(str, str) -> bool

    Make sure we are not staying on the same page."""
    parsed_old = urlparse(old_url)
    parsed_new = urlparse(new_url)
    return parsed_old.path != parsed_new.path

if __name__ == '__main__':
    m = 5
    print random_percentage(m)
    print random_distribution(m)
