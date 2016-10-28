# wiki_philosophy
Take any random article on Wikipedia (example: http://en.wikipedia.org/wiki/Art)
 and click on the first link on the main body of the article that is not within
 parenthesis or italicized;
If you repeat this process for each subsequent article you will often end up on
the Philosophy page.
• What percentage of pages often lead to philosophy?
• Using the random article link (found on any wikipedia article in the left sidebar),
what is the distribution of
path lengths for 500 pages, discarding those paths that never reach the Philosophy page?
• How can you reduce the number of http requests necessary for 500 random starting pages?

## Dependencies

python2

BeautifulSoup `from bs4 import BeautifulSoup`

## Description

Module client_1.py contains solution to first and second part of the assignment.

To run:  `python client_1.py`

Module client.py contains solution to the third part of the assignment.
We can reduce number of the HTTP requests by using caching.
Consider this:
Create a cache dictionary where the URLs are mapped to path length or -1. 
Every URL we see, we compare with the keys in cache dictionary. 
Once URL matches one of the keys we can calculate the path length w/o
 sending any more requests. When a URL does not lead to the `philosophy`
 page we return -1.
We are working with the assumption that Wikipedia pages' content does not change.

To run: `python client.py`

## To run tests go :

`python test_1.py` to test solution to  problem 1 and 2.

`pyton test.py` to test solution to  problem 3.



