import requests
import json
data= {'name':'Python', 
        'surname':'Programming'
      }
url = 'https://pritty.herokuapp.com/show_data'
#url = 'http://127.0.0.1:5000/show_data'
response = requests.post(url, json=data)
print (response)
print(response.url) 
print (response.json())
values=response.json()
 

print (response.json()) 
print (values['name'])
print (values['surname'])



