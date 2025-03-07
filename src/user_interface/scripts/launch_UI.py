#!/usr/bin/env python3
# coding=utf-8
 
from flask import Flask, render_template, request, jsonify
from gen_json import gen_json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', data=gen_json())

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json() # retrieve the data sent from JavaScript
    print(data)
    result = data['value'] * 2
    return jsonify(result=result) # return the result to JavaScript

if __name__ == '__main__':    
    app.run(debug=True)
