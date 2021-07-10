import requests
from requests_oauthlib import OAuth1Session
import os
import json
import twitter

#API key: ife3mz9hr0XJxHNicgJO7OCzk
#API secret key: di4xpD1vMpzz1NyrgSAfU3akrbAKiT0K1UJjnZzq3jVSASyE59
#Bearer token: AAAAAAAAAAAAAAAAAAAAAJ0PRgEAAAAAhgKZSlYk2ukLTwMAQvvCV1SbshA%3DQpNXtJT0pAUG4KkltRgJByywn0oa9D0ytJiEBFDGQ8BS4TSWn0

KEY = 'ife3mz9hr0XJxHNicgJO7OCzk'
SECRET_KEY = 'di4xpD1vMpzz1NyrgSAfU3akrbAKiT0K1UJjnZzq3jVSASyE59'

id = "1413640311331598338"

# auth_url = "https://api.twitter.com/oauth/request_token"

# response = requests.post(auth_url, {
#   "grant_type" : "client_credentials",
#   "key": KEY,
#   "secret_key": SECRET_KEY
# })

# You can replace Tweet ID given with the Tweet ID you wish to like.
# You can find a Tweet ID by using the Tweet lookup endpoint
payload = {"tweet_id": "1405578416095731712"}

# Get request token
request_token_url = "https://api.twitter.com/oauth/request_token"
oauth = OAuth1Session(KEY, client_secret=SECRET_KEY)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print(
        "There may have been an issue with the consumer_key or consumer_secret you entered."
    )

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)

# Get authorization
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Please go here and authorize: %s" % authorization_url)
verifier = input("Paste the PIN here: ")

# Get the access token
access_token_url = "https://api.twitter.com/oauth/access_token"
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

# Making the request
response = oauth.post(
    "https://api.twitter.com/2/users/{}/likes".format(id), json=payload
)

if response.status_code != 200:
    raise Exception(
        "Request returned an error: {} {}".format(response.status_code, response.text)
    )

print(response.status_code)

fields = "created_at,description,pinned_tweet_id"
params = {"usernames": "TwitterDev", "user.fields": fields}

response = oauth.get("https://api.twitter.com/labs/2/users/by?", params=params)
print(response)
print("Response status: %s" % response.status_code)
print("Body: %s" % response.text)