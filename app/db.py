from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "chat_bot"
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
users_collection = db["users"]
chats_collection = db["chat_state"]
threads_collection = db["threads"]
print(users_collection)
print(chats_collection)