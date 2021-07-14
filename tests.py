import unittest
from twitterApi import get_authorization, get_access_token


class Tests(unittest.TestCase):
    def test_get_authorization(self):
      self.assertNotEqual(get_authorization(), "")
      
    def test_get_request(self):
        verifier = get_authorization()
        tokens = get_access_token(verifier)
        myOauth = make_request (tokens)
      
  
if __name__ == '__main__':
    unittest.main()