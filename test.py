
import requests
import json


event1 = {"body":[
		 "The company HuggingFace is based in New York City",
		 "Apples are especially bad for your health"]
		}

event2 = {"body":[
		 "The company HuggingFace is based in New York City",
		 "HuggingFace's headquarters are situated in Manhattan"]
		}

event3 = {"body": ["The sky is blue and beautiful.",
                  "The quick brown fox jumps over the lazy dog."
            ]
        }


url = "https://.execute-api.region.amazonaws.com/dev/qa"

r = requests.post(url, json=event3)
print("result without securely key: ", r.json())




# r = requests.post(url, json.dumps(event), headers=key)
# res = json.loads(r.content)
# print("result with securely key: ", res)
