
try:
	import unzip_requirements
except ImportError:
	pass


#from __future__ import print_function
import os
import boto3

# os.environ['AWS_PROFILE'] = "MyProfile"
# os.environ['AWS_DEFAULT_REGION'] = "us-east-2"
import tarfile
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig
import torch
import io




s3 = boto3.client('s3', region_name='us-east-2')
print("[INFO:] Connecting to cloud")

model_path = './model-bert-clsssify'
s3_bucket =  'bert-classify-para'
file_prefix = 'bert-finetuned.tar.gz'



def load_model_from_s3(model_path: str, s3_bucket: str, file_prefix: str):
	print("--->>> model_path: ", model_path)
	if model_path and s3_bucket and file_prefix:
		obj = s3.get_object(Bucket=s3_bucket, Key=file_prefix)
		bytestream = io.BytesIO(obj['Body'].read())
		tar = tarfile.open(fileobj=bytestream, mode="r:gz")
		config = AutoConfig.from_pretrained(f'{model_path}/config.json')
		# tokenizer = AutoTokenizer.from_pretrained(model_path)
		# model = AutoModelForSequenceClassification.from_pretrained(pretrained_model_name_or_path=None, state_dict=state, config=config)

		for member in tar.getmembers():
		    print(member)
		    if member.name.endswith(".bin"):
		        f = tar.extractfile(member)
		        state = torch.load(io.BytesIO(f.read()))
		        tokenizer = AutoTokenizer.from_pretrained(model_path)
		        model = AutoModelForSequenceClassification.from_pretrained(pretrained_model_name_or_path=None, state_dict=state, config=config)

		return model, tokenizer
	else:
		raise KeyError('No S3 Bucket and Key Prefix provided')



model, tokenizer = load_model_from_s3(model_path, s3_bucket, file_prefix)





# tokenizer = AutoTokenizer.from_pretrained("./model-bert-clsssify")
# model = AutoModelForSequenceClassification.from_pretrained("./model-bert-clsssify")



def predict_answer(event, context):
	sequence_0 = event['sequence_0']
	sequence_1 = event['sequence_1']
	not_paraphrase = tokenizer(sequence_0, sequence_1, return_tensors="pt")

	not_paraphrase_classification_logits = model(**not_paraphrase)

	result = torch.softmax(not_paraphrase_classification_logits[0], dim=1).tolist()[0]
	classes = ["not paraphrase", "is paraphrase"]
	ind = result.index(max(result))
	answer = (classes[ind], ("{:.2f}".format(max(result))))
	return {
			"statusCode": 200,
			"headers": {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*',
				"Access-Control-Allow-Credentials": True
				},
				"body": json.dumps({'answer': answer})
			}






# event1 = {
# 		"sequence_0": "The company HuggingFace is based in New York City",
# 		"sequence_1": "Apples are especially bad for your health"
# 		}

# event2 = {
# 		"sequence_0": "The company HuggingFace is based in New York City",
# 		"sequence_1": "HuggingFace's headquarters are situated in Manhattan"
# 		}


# result1 = predict_answer(event1, "")
# print(result1['body'])

# result2 = predict_answer(event2, "")
# print(result2['body'])