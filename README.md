# wiki_philosophy


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

