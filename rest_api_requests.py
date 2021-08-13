import requests

URL = "http://127.0.0.1:8000/api/notes/"

input_text = "вставать в 6 утра начиная со 2 декабря - замечательно"
print(f"POST input text: {input_text}")
response = requests.post(URL, json={"input_text": input_text})
json = response.json()
print("Response:", json)

print(f"GET")
response = requests.get(URL)
json = response.json()
print("Response:", json)

print(f"DELETE pk 12")
response = requests.delete(URL+"12")
json = response.json()
print("Response:", json)

print(f"GET")
response = requests.get(URL)
json = response.json()
print("Response:", json)
