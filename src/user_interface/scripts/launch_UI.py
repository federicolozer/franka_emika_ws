#!/usr/bin/env python3
# coding=utf-8
 
from flask import Flask, render_template, request, jsonify
from gen_json import gen_json
import webbrowser
import os

app = Flask(__name__)



def callDatasetCreator(data):
    msg = "rosrun neural_network dataset_creator"
    for elem in data:
        msg += (" " + elem)
    
    res = os.system(msg)

    return(res)



def callTestCreator(data):
    msg = "rosrun neural_network test_creator"
    for elem in data:
        msg += (" " + elem)
    
    res = os.system(msg)
    
    return(res)



def callTrainNN():
    msg = "rosrun neural_network NN_trainer.py"
    res = os.system(msg)

    return(res)



@app.route('/')
def home():
    return render_template('home.html')



@app.route('/getJson', methods=['GET'])
def sendData():
    return gen_json()



@app.route('/sendDatasetCreatorRequest', methods=['SEND'])
def getData():
    data = request.get_json()
    res = callDatasetCreator(data)
    return jsonify(result=res)



@app.route('/sendTestCreatorRequest', methods=['SEND'])
def getTest():
    data = request.get_json()
    res = callTestCreator(data)
    return jsonify(result=res)



@app.route('/sendTrainingNNRequest', methods=['SEND'])
def startTraining():
    request.get_json()
    res = callTrainNN()
    return jsonify(result=res)




if __name__ == '__main__':   
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(debug=True)
