from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    # Here you would typically process the data, e.g., send it to a backend API
    response = requests.post('http://localhost:5001/submit', json=data)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)