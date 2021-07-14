import unittest
from twitterApi import get_authorization


class Tests(unittest.TestCase):
    def test_getAuthorization(self):
      self.assertNotEqual(get_authorization(), "")
      
    

if __name__ == '__main__':
    unittest.main()