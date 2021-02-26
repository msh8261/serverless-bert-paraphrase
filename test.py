
import requests
import json


event = {
        "sequence_0": "The company HuggingFace is based in New York City",
        "sequence_1": "Apples are especially bad for your health"
        }

url = "https://snhbnzw2dc.execute-api.us-east-2.amazonaws.com/dev/qa"

r = requests.post(url, json=event)
print("result without securely key: ", r.json())



# key = {'x-api-key': 'tI95Zb3Ikr5l8jK1o3DDN4BOzFDLi13y3GYZ5uDW'}


# r = requests.post(url, json.dumps(event), headers=key)
# res = json.loads(r.content)
# print("result with securely key: ", res)
