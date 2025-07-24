from flask import Flask, jsonify, request, redirect, render_template
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv
import pymongo
import redis
# import dnspython
load_dotenv()
# MongoDB connection
mongo_uri = os.getenv('MONGO_URI')

client = pymongo.MongoClient(mongo_uri)
db = client.test
collection = db['to_do_list']

app = Flask(__name__)
CORS(app)

url = os.getenv('REDIS_URL')

r = redis.Redis(
    host=os.getenv('REDIS_URL', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    password=os.getenv('REDIS_PASSWORD'),
    username=os.getenv('REDIS_USERNAME'),
    decode_responses=True,
)

success = r.set('foo', 'bar')
result = r.get('foo')
print(f"Redis connection successful: {success}, Result: {result}")

@app.route('/redis', methods=['POST'])
def redis():
    if not url:
        return jsonify({"error": "REDIS_URL not set"}), 500
    
    try:
        r.set('foo', 'bar')
        value = r.get('foo')
        return jsonify({"message": "Redis connection successful", "value": value}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    todo_item = request.json.get('todoItem')
    todo_description = request.json.get('todoDescription')
    print(f"Todo item received: {todo_item}")
    print(f"Todo description received: {todo_description}")
    
    if todo_item or todo_description:
        db.collection.insert_one({
            "todo_item": todo_item,
            "todo_description": todo_description
        })
    elif not todo_item or not todo_description:
        return jsonify({"error": "Todo item and description are required"}), 400
    
    else:
        return jsonify({"Data saved successfully!"}), 200
    
    return redirect('http://localhost:5000')

@app.route('/api', methods=['GET'])
def api():
    data = db.collection.find()
    data = list(data)  # Convert cursor to list
    with open('data.json', 'w') as file:
        file.write(str(data))
    
    return jsonify([{"name": item["name"], "email": item["email"]} for item in data])

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    db.collection.insert_one({"name": name, "email": email})
    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400
    elif name and email:
        db.collection.insert_one({"name": name, "email": email})
        print(f"Data submitted: Name: {name}, Email: {email}")
    else:
        return jsonify({"error": "Invalid data"}), 400  
    return redirect('/success')

@app.route('/success')
def success():
    return jsonify({"message": "Data submitted successfully!"}) # Or over here I can use another html file to show success message

if __name__ == '__main__':
    app.run(debug=True, port=5001)