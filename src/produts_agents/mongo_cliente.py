import os 
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.environ["MONGODB_URI"]
cliente = MongoClient(uri)
db = cliente["produts_agents"]
