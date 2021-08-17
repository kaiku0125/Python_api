import requests
import logging

BASE = "http://127.0.0.1:5000/"

data = {"user_id" : "kaiku0125", "password" : "ggg"}
data2 = {"user_id" : "amy666", "password" : "GGGG"}



response = requests.delete(BASE + "mygame/2")
print(response.json())
logging.error('error')
logging.info('info')
input()

response = requests.get(BASE + "mygame/2")
print(response.json())

