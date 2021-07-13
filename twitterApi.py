import requests
from requests_oauthlib import OAuth1Session
import os
import json
import twitter

# API key: ife3mz9hr0XJxHNicgJO7OCzk
# API secret key: di4xpD1vMpzz1NyrgSAfU3akrbAKiT0K1UJjnZzq3jVSASyE59
# Bearer token: AAAAAAAAAAAAAAAAAAAAAJ0PRgEAAAAAhgKZSlYk2ukLTwMAQvvCV1SbshA%3DQpNXtJT0pAUG4KkltRgJByywn0oa9D0ytJiEBFDGQ8BS4TSWn0 # noqa

KEY = 'ife3mz9hr0XJxHNicgJO7OCzk'
SECRET_KEY = 'di4xpD1vMpzz1NyrgSAfU3akrbAKiT0K1UJjnZzq3jVSASyE59'

id = "1413640311331598338"


# Get request token
#url input = "https://api.twitter.com/oauth/request_token"
#Test 1: check that user input is correct
def requestToken(url):
  request_token_url = url
  oauth = OAuth1Session(KEY, client_secret=SECRET_KEY)

  try:
      fetch_response = oauth.fetch_request_token(request_token_url)
  except ValueError:
      print(
          "There may have been an issue with the consumer_key or consumer_secret you entered."  # noqa
      )

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)

# Get authorization
# url input = "https://api.twitter.com/oauth/authorize"
# Test 2: check that PIN is correct
def getAuthorization(url): 
  base_authorization_url = url
  authorization_url = oauth.authorization_url(base_authorization_url)
  print("Please go here and authorize: %s" % authorization_url)
  verifier = input("Paste the PIN here: ")
  return verifier

# Get the access token
# url input "https://api.twitter.com/oauth/access_token"
# Test 3: check that url is valid
def getAccessToken(url):
  access_token_url = url
  oauth = OAuth1Session(
      KEY,
      client_secret=SECRET_KEY,
      resource_owner_key=resource_owner_key,
      resource_owner_secret=resource_owner_secret,
      verifier=verifier,
  )
  oauth_tokens = oauth.fetch_access_token(access_token_url)

  access_token = oauth_tokens["oauth_token"]
  access_token_secret = oauth_tokens["oauth_token_secret"]

# Make the request
oauth = OAuth1Session(
    KEY,
    client_secret=SECRET_KEY,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

# POST request
# Test 4: confirm that the selected tweet was liked
# payload = {"tweet_id": "1414570335794573313"}
def postRequest(payload):
  response = oauth.post(
      "https://api.twitter.com/2/users/{}/likes".format(id), json=payload
  )

  if response.status_code != 200:
      raise Exception(
          "Request returned an error: {} {}".format(response.status_code, response.text)  # noqa
      )

  print(response.status_code)
  
# GET request
# username input "TwitterDev"
# Test 5: check that username exists
def getRequest(username):
  fields = "created_at,description,pinned_tweet_id"
  params = {"usernames": username, "user.fields": fields}


  response = oauth.get("https://api.twitter.com/labs/2/users/by?", params=params)
  print(response)
  print("Response status: %s" % response.status_code)
  print("Body: %s" % response.text)
