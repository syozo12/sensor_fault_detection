from pymongo.mongo_client import MongoClient
import pandas as pd  
import json

url="mongodb+srv://radhasvohra05:genai12@cluster0.lotvxsp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#create nwe clien and connect to dserver
client=MongoClient(url)
DATABASE_NAME="p2"
MONGO_COLLECTION_NAME = "waferfault"
df=pd.read_csv("./notebook/wafer.csv")
json_read=list(json.loads(df.T.to_json()).values())
#upload data
client[DATABASE_NAME][MONGO_COLLECTION_NAME].insert_many(json_read)