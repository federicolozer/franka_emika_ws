#!/usr/bin/env python3
# coding=utf-8
 
from flask import Flask, render_template, request, jsonify
from gen_json import gen_json
import os

app = Flask(__name__)



def callDatasetCreator(data):
    msg = "rosrun neural_network dataset_creator"
    for elem in data:
        msg += (" " + elem)
    
    os.system(msg)



def callTrainNN():
    msg = "rosrun neural_network NN_trainer.py"
    os.system(msg)



@app.route('/')
def home():
    return render_template('home.html')



@app.route('/getJson', methods=['GET'])
def sendData():
    return gen_json()



@app.route('/sendDatasetCreatorRequest', methods=['SEND'])
def getData():
    data = request.get_json()
    callDatasetCreator(data)
    return jsonify(result="Dataset created correctly")



@app.route('/sendTrainingNNRequest', methods=['SEND'])
def startTraining():
    data = request.get_json()
    callTrainNN()
    return jsonify(result="Neural network training has ended correctly")




if __name__ == '__main__':    
    app.run(debug=True)
