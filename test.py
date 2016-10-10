import unittest
from client import find_philosophy, find_percentage, distribution 

# path length = 17 (expect 17)
SUCCESS_URL1 = 'https://en.wikipedia.org/wiki/Alcacocha_(Pasco)'
SUCESS_URL2 = 'https://en.wikipedia.org/wiki/1736_Floirac'
SUCCESS_URL3 = 'https://en.wikipedia.org/wiki/UFC_111'

# there is no valid link on the page (expect -1)
NO_LINK_URL = 'https://en.wikipedia.org/wiki/Arrondissements_of_the_Charente-Maritime_department'

# link that leads to itself (expect -1)
LOOP_URL = 'https://en.wikipedia.org/wiki/Maid_service'
LOOP_URL2 = 'https://en.wikipedia.org/wiki/United_States'
#philsosphy page
PHILOSOPHY_URL = 'https://en.wikipedia.org/wiki/Philosophy'

class PhilosophyTestCase(unittest.TestCase):

    def test_success(self):
        # ensure that the url leads to `philosophy page`
        r = find_philosophy(SUCCESS_URL1)
        self.assertTrue(r > 0)

    def test_no_link(self):
        # if there is no valid link on the page expect output -1
        r = find_philosophy(NO_LINK_URL)
        self.assertEqual(r, -1)

    def test_loop(self):
        # if we see the same page agin we are will never reach 
        # `philosophy` page
        r = find_philosophy(LOOP_URL)
        self.assertEqual(r, -1)

    def test_philosophy_itself(self):
        # no need to look we are there
        r = find_philosophy(PHILOSOPHY_URL)
        self.assertEqual(r, 0)


class PercentageTestCase(unittest.TestCase):
    
    def test_all_success(self):
        urls = (SUCCESS_URL1, SUCESS_URL2, SUCCESS_URL3)
        self.assertEqual(find_percentage(urls), 100)

    def test_no_success(self):
        urls = (LOOP_URL, LOOP_URL2, NO_LINK_URL)
        self.assertEqual(find_percentage(urls), 0)

    def test_mixed(self):
        urls = (SUCCESS_URL1, SUCESS_URL2, LOOP_URL)
        self.assertEqual(find_percentage(urls), 66)


class DistributionTestCase(unittest.TestCase):

    def test_all_philosophy(self):
        urls = (PHILOSOPHY_URL, PHILOSOPHY_URL, PHILOSOPHY_URL)
        self.assertEqual(distribution(urls), [0, 0, 0])

    def test_distr_all_sucess(self):
        urls = (SUCCESS_URL1, SUCESS_URL2, SUCCESS_URL3)
        self.assertEqual(distribution(urls), [17, 7, 16])

if __name__ == '__main__':
    unittest.main()