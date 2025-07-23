from flask import Flask, jsonify, request, redirect
import os
import requests
from dotenv import load_dotenv
import pymongo
# import dnspython
load_dotenv()
# MongoDB connection
mongo_uri = os.getenv('MONGO_URI')

client = pymongo.MongoClient(mongo_uri)
db = client.test
collection = db['test_collection']

app = Flask(__name__)

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