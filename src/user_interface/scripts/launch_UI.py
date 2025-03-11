#!/usr/bin/env python3
# coding=utf-8
 
from flask import Flask, render_template, request, jsonify
from gen_json import gen_json
import os

app = Flask(__name__)



def callDatasetCreator(data):
    msg = ""
    for elem in data:
        msg += (" " + elem)
    print(msg)
    os.system(f"rosrun neural_network dataset_creator{msg}")



@app.route('/')
def home():
    return render_template('home.html')



@app.route('/get', methods=['GET'])
def sendData():
    return gen_json()



@app.route('/send', methods=['SEND'])
def getData():
    data = request.get_json()
    callDatasetCreator(data)
    return jsonify(result=1)




if __name__ == '__main__':    
    app.run(debug=True)
