import requests
import bs4
from bs4 import BeautifulSoup
from urlparse import urljoin
from urlparse import urlparse
from time import sleep

def find_philosophy(url, visited_url=[], path_length=0):
    """(str) -> int

    Return path length or -1 if the `url` does not lead to 
    philosophy page."""
    r = requests.get(url)
    print 'URL: ', r.url, 'PATH LENGTH: ', path_length

    html_content = r.text
    philosophy_url = 'https://en.wikipedia.org/wiki/Philosophy'
    if r.url == philosophy_url:
        print 'Reached Philosophy'
        # Number of requests it took to get to philosophy page.
        return path_length
    # Check it have we not seen the link yet. Repeted link would indicate
    # we will never get to philosophy page.
    elif r.url in visited_url:
        print 'this is a loop'
        return -1
    else:
        link = find_link(html_content)
        # Check if the page contains link that meets the requirements.
        if link and link.attrs.has_key('href'):
            new_url = urljoin(r.url, link.attrs['href'])
            if not differrent_path(r.url, new_url):
                print 'This is a same page', new_url
                return -1
            else:
                path_length += 1
                visited_url.append(r.url)
                # Recurse
                return find_philosophy(new_url, visited_url, path_length)
        else:
            print 'This is not a link', link
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

def find_percentage(urls):
    """(list) -> int

    Return the percentage of pages that lead to philosophy.
    """
    # n is the number of pages that lead to philosophy
    n = 0
    for url in urls:
        if find_philosophy(url, [], 0) != -1:
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
    for url in urls:
        r = find_philosophy(url, [], 0)
        if r != -1:
            distr.append(r)
    return distr

def random_distribution(m):
    """(int) -> list

    Distribution of path lengths for `m` pages."""
    urls = []
    for i in range(m):
        p = 'https://en.wikipedia.org/wiki/Special:Random'
        urls.append(p)
    return distribution(urls)

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
    url = 'https://en.wikipedia.org/wiki/New_York_City'  # a loop
    url2 = 'http://en.wikipedia.org/wiki/Art'
    #print find_philosophy(url)
    #print ''
    #print find_philosophy(url2)
    #urls = ['https://en.wikipedia.org/wiki/David_Marr_(neuroscientist)',
    #        'https://en.wikipedia.org/wiki/Reinevatn',
    #        'https://en.wikipedia.org/wiki/Alpine_speedwell']
    #for url in urls:
    #    print "Testing url: ", url
    #    result = find_philosophy(url)
    #    print "*** Result: ", result
    #print ''
    print 'PERCENTAGE', find_percentage(3)
    print ''
    print 'DISTRIBUTIION', distribution(3)
