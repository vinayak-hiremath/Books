import pymongo

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client['library_db']

# Collections
books_col = db['books']
users_col = db['users']
history_col = db['borrow_history']