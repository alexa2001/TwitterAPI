import requests

user_input = input("Text: ")

url = 'http://text-processing.com/api/sentiment/'
myobj = {
  "text": user_input
}

response = requests.post(url, data = myobj)

print(response.json())