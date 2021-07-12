import requests 

BASE = "http://127.0.0.1:5000/"

data = [{"likes": 78, "name": "Joe", "views": 1000000}, 
        {"likes": 1000, "name": "How to create a mastadon api", "views": 8000}, 
        {"likes": 34, "name": "timatishka", "views": 2000}
]

for i in range(len(data)):
    response = requests.put(BASE + "video/"+str(i), data[i])
    print(response.json())

input()
response=requests.delete(BASE+"video/0")
print(response)

input()
response = requests.get(BASE + "video/1")
print(response.json())
