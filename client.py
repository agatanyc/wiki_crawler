import urllib2
from bs4 import BeautifulSoup
from stack import Stack

prettify = BeautifulSoup.prettify

def find_link(url):
    """(str) -> str
    Return the first link on the main body of the article that is
    not within parenthesis or italicized.
    Since Wikipedia uses a template we assume the not
    italicized link will be in one of the `p` tag paragraphs."""
    html_content = urllib2.urlopen(url)
    soup = BeautifulSoup(html_content)
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        string = ''
        for element in p:
            if type(element) == bs4.element.NavigableString:
                string += element
            elif type(element) == bs4.element.Tag and s.name == 'a':
                if matched_parenths(string):
                    return element
            else:
                string += element.get_text()
    return None

def matched_parenths(string):
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

def find_philosophy(url, visited_url=[], path_length=0):
    """(str) -> int

    Return path length or -1 if the `url` does not lead to 
    philosophy page."""
    # track previous url to check for loops
    # if no link on the page -1
    # if see some page again in one search -1
    philosophy_url = 'https://en.wikipedia.org/wiki/Philosophy'
    path_length = 0
    if url == philosophy_url:
        return path_length
    else:
        link = find_link(url)
        # Check if the page contains link that meets the requirements.
        # Check it have we not seen the link yet. Repeted link would indicate
        # we will never get to philosophy page
        if link and link url not in visited_url:
            path_length += 1
            visited_url.append(url)
            # Recurse
            find_philosophy(link, visited_url, path_length)
        else:
            return -1

def find_path_length(url):
    """(str) -> int
    Check how many requests to took to get to
    philosophy page."""
    if find_philosophy(url):
        pass


def find_percentage(n, m):
    """(int) -> int
    Return the percentage of pages often lead to philosophy.
    """
    # n is the number of pages that lead to philosophy
    # m is the number of pages we are considering in the search
    percentage = n // m * 100

def distribution(list):
    distribution = {}
    for url in list:
        dist[url] = find_path_length(url)
    return distribution

# helper functions

def get_soup(url):
    html_content = urllib2.urlopen(url)
    return BeautifulSoup(html_content)

if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/Uniform_Resource_Locator'
    s1 = '((()))'
    s2 = '()()'
    s3 = '(()'

    #find_link(url)
    print matched_parenths(s1)
    print matched_parenths(s2)
    print matched_parenths(s3)



