
import requests
import pandas as pd
import os

import numpy as np

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {'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'}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Change the directory to Documentation Scraper
path = os.path.realpath(__file__)
dir = os.path.dirname(path)
dir = dir.replace('Hugging Face','Documentation_Scraper')
os.chdir(dir)
df = pd.read_csv('numpy_scrapped_items.csv')
df = df.fillna('')

func = np.array(df["title"])
des = np.array(df["description"])

des_example = []

for i in range (len(des)):
    des_example.append(des[i])
    
while (1):
    user_input = input ("Enter Description: ")
    data = query(
        {
            "inputs": {
                "source_sentence": user_input,
                "sentences": des_example
            }
        })
    print (len(data))
    
    print (func[np.argmax(data)])
    print (des[np.argmax(data)])
    
    sorted_data = np.argsort(data)

