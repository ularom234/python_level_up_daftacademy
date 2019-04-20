# app.py
from flask import Flask, jsonify, request
import json
 
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/show_data', methods=['POST'])
def show_data():
    return jsonify(request.json)


@app.route('/pretty_print_name', methods=['POST'])
def pretty_print_name():
    
    return 'Na imię mu {}, a nazwisko jego {}'.format(request.json.get('name'), request.json.get('surename'))



@app.route('/method', methods=['GET', 'POST','DELETE', 'PUT'])
def request_method():
    return str(request.method)

@app.route('/request')
def request_info():
    return 'request method: {} url: {} headers: {}'.format(request.method,request.url,request.headers)

if __name__ == '__main__':
    app.run(debug=True)
