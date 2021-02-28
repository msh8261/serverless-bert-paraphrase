
#from __future__ import print_function
import os
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig
import torch
import io



tokenizer = AutoTokenizer.from_pretrained("./model")
model = AutoModelForSequenceClassification.from_pretrained("./model")





def handler(event, context):

	body = event["body"]
	sequence_0 = body[0]
	sequence_1 = body[1]
	not_paraphrase = tokenizer(sequence_0, sequence_1, return_tensors="pt")

	not_paraphrase_classification_logits = model(**not_paraphrase)

	result = torch.softmax(not_paraphrase_classification_logits[0], dim=1).tolist()[0]
	classes = ["not paraphrase", "is paraphrase"]
	ind = result.index(max(result))
	answer = (classes[ind], ("{:.2f}".format(max(result))))
	return {
			"statusCode": 200,
			"headers": {
				"Content-Type": "application/json",
				"Access-Control-Allow-Origin": "*",
				"Access-Control-Allow-Credentials": True
				},
				"body": json.dumps({"answer": answer})
			}






# event1 = {"body":[
# 		 "The company HuggingFace is based in New York City",
# 		 "Apples are especially bad for your health"]
# 		}

# event2 = {"body":[
# 		 "The company HuggingFace is based in New York City",
# 		 "HuggingFace's headquarters are situated in Manhattan"]
# 		}


# result1 = handler(event1, "")
# print(result1['body'])

# result2 = handler(event2, "")
# print(result2['body'])