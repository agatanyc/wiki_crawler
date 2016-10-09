import requests
import bs4
from bs4 import BeautifulSoup
from urlparse import urljoin
from urlparse import urlparse

def find_philosophy(url, visited_url=[], path_length=0):
    """(str) -> int

    Return path length or -1 if the `url` does not lead to 
    philosophy page."""
    print 'URL: ', url
    r = requests.get(url)
    html_content = r.text
    philosophy_url = 'https://en.wikipedia.org/wiki/Philosophy'
    # Number of requests it took to get to philosophy page.
    path_length = 0
    if url == philosophy_url:
        return path_length
    elif url in visited_url:
        return -1
    else:
        link = find_link(html_content)
        # Check if the page contains link that meets the requirements.
        # Check it have we not seen the link yet. Repeted link would indicate
        # we will never get to philosophy page.
        if link and link.attrs.has_key('href'):
            new_url = urljoin(url, link['href'])
            if not differrent_path(url, new_url):
                return -1
            else:
                path_length += 1
                visited_url.append(url)
                # Recurse
                find_philosophy(new_url, visited_url, path_length)
        else:
            return -1

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

def find_percentage(m):
    """(int, int) -> int

    Return the percentage of pages that lead to philosophy from 
    `m` number of pages total.
    """
    # n is the number of pages that lead to philosophy
    # m is the number of pages we are considering in the search
    n = 0
    for i in range(m):
        # find random page
        url = 'https://en.wikipedia.org/wiki/Special:Random'
        found = []
        if find_philosophy(url) != -1:
            n += 1
            found.append(url)
    percentage = n // m * 100
    return percentage, found

def distribution(m):
    """() -> dict

    Distrbution of path lengths for m pages.
    """
    distr = {}
    found = find_percentage(m)[1]
    for url in found:
        distr[url] = find_philosophy(url)
    return distr

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
    """Make sure we are not staing on the same page."""
    parsed_old = urlparse(old_url)
    parsed_new = urlparse(new_url)
    return parsed_old.path != parsed_new.path

if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/New_York_City'
    print find_philosophy(url)
