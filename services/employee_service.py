from pymongo import MongoClient
from bson.objectid import ObjectId
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.get_default_database()
collection = db["employees"]

# Pagination-based employee fetch
def get_employees(filter_query, page, per_page):
    employees = list(collection.find(filter_query).skip((page - 1) * per_page).limit(per_page))
    total = collection.count_documents(filter_query)
    return employees, total

# Insert a new employee
def insert_employee(data):
    return collection.insert_one(data)

# Update an employee
def update_employee(emp_id, data):
    return collection.update_one({'_id': ObjectId(emp_id)}, {'$set': data})

# Fetch a single employee
def get_employee(emp_id):
    return collection.find_one({'_id': ObjectId(emp_id)})

# ✅ Add this function to fix your error
def get_all_employees():
    return list(collection.find())
