import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json

from handler import handler

def test_add():
	a=2
	assert 2 == a


event1 = {"body":[
         "The company HuggingFace is based in New York City",
         "Apples are especially bad for your health"]
        }

event2 = {"body":[
         "The company HuggingFace is based in New York City",
         "HuggingFace's headquarters are situated in Manhattan"]
        }

def test_handler1():
    res = handler(event1, "")
    assert json.loads(res['body']) == {"answer": ["not paraphrase", "0.94"]}


def test_handler2():
    res = handler(event2, "")
    assert json.loads(res['body']) == {"answer": ["is paraphrase", "0.90"]}




