from requests_oauthlib import OAuth1Session
import os, json, twitter, sqlalchemy, requests
from sqlalchemy import create_engine
import pandas as pd

# API key: ife3mz9hr0XJxHNicgJO7OCzk
# API secret key: di4xpD1vMpzz1NyrgSAfU3akrbAKiT0K1UJjnZzq3jVSASyE59
# Bearer token: AAAAAAAAAAAAAAAAAAAAAJ0PRgEAAAAAhgKZSlYk2ukLTwMAQvvCV1SbshA%3DQpNXtJT0pAUG4KkltRgJByywn0oa9D0ytJiEBFDGQ8BS4TSWn0 # noqa

engine = create_engine('mysql://root:codio@localhost/twitter_data')

KEY = 'ife3mz9hr0XJxHNicgJO7OCzk'
SECRET_KEY = 'di4xpD1vMpzz1NyrgSAfU3akrbAKiT0K1UJjnZzq3jVSASyE59'

id = "1413640311331598338"


# Get request token
request_token_url = "https://api.twitter.com/oauth/request_token"
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
# test that user input is valid
def get_authorization():
  base_authorization_url = "https://api.twitter.com/oauth/authorize"
  authorization_url = oauth.authorization_url(base_authorization_url)
  
  print("Please go here and authorize: %s" % authorization_url)
  verifier = input("Paste the PIN here: ")
  
  return verifier

# Get the access token
def get_access_token(pVerifier):
  access_token_url = "https://api.twitter.com/oauth/access_token"
  oauth = OAuth1Session(
      KEY,
      client_secret=SECRET_KEY,
      resource_owner_key=resource_owner_key,
      resource_owner_secret=resource_owner_secret,
      verifier=pVerifier,
  )

  oauth_tokens = oauth.fetch_access_token(access_token_url)

  access_token = oauth_tokens["oauth_token"]
  access_token_secret = oauth_tokens["oauth_token_secret"]
  
  return (access_token, access_token_secret)

# Make the request
def make_request(tokens):
  oauth = OAuth1Session(
      KEY,
      client_secret=SECRET_KEY,
      resource_owner_key=tokens[0], 
      resource_owner_secret=tokens[1],
  )
  
  return oauth

# POST request
def postRequest(myOauth):
  response = myOauth.post(
      "https://api.twitter.com/2/users/{}/likes".format(id), json=payload
  )

  if response.status_code != 200:
      raise Exception(
          "Request returned an error: {} {}".format(response.status_code, response.text)  # noqa
      )

  print(response.status_code)
  
# GET request
# This inserts twitter user information into my twitter_sample database
def getRequest(myOauth, username):
  fields = "created_at,description,pinned_tweet_id"
  params = {"usernames": username, "user.fields": fields}
  response = myOauth.get("https://api.twitter.com/labs/2/users/by?", params=params)
  
  print(response)
  print("Response status: %s" % response.status_code)
  print("Body: %s" % response.text)

  r = response.json()
  data = r['data'][0]

  col_names = ['id', 'created_at', 'name', 'username', 'description']
  df = pd.DataFrame(columns = col_names)
  df.loc[len(df.index)] = [data['id'], data['created_at'], data['name'], data['username'], data['description']]

  df.to_sql('twitter_sample', con=engine, if_exists='append', index=False)


def main():
#   postRequest({"tweet_id" : "1403291168583073795"})
  verifier = get_authorization()
  tokens = get_access_token(verifier)
  myOauth = make_request (tokens)
  getRequest(myOauth, "Malala")
#   getRequest(myOauth, "TwitterDev")
  
if __name__ == "__main__":
    main()
    
""" 
QUESTIONS

1. mysql doesnt like it when I try to make a getRequest 
   with a twitter account that contains a single quotation.
   You can see this error if you replace "JoeBiden" with 
   "Malala". How can I fix this?
""" 

