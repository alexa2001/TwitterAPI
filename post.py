import requests

url = 'https://jsonplaceholder.typicode.com/posts'
data = {'title': 'Special Agent', 'body': 'Leroy Jethro Gibbs', 'userId': 1}

response = requests.post(url, data)

print(response.status_code)
print(response.json())