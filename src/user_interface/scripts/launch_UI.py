#!/usr/bin/env python3
# coding=utf-8
 
import sys
sys.path.append('/home/lozer/franka_emika_ws/src/path_planning/scripts')

from flask import Flask, render_template, request, jsonify
from gen_json import gen_json
import webbrowser
import os
from main import main

app = Flask(__name__)




def callDatasetCreator(data):
    msg = "rosrun neural_network dataset_creator"
    if len(data) > 0:
        for elem in data:
            msg += f" {elem}"
    
        res = os.system(msg)
    else:
        res = 1

    return res



def callTestCreator(data):
    msg = "rosrun neural_network test_creator"
    res = 0
    if len(data) > 0:
        for elem in data:
            msg_tmp = (f"{msg} {elem}")

            path = f"/home/lozer/franka_emika_ws/src/path_planning/data/trajectory/{elem[5:-4]}"

            if not os.path.exists(path):
                os.makedirs(path)
            
            res += os.system(msg_tmp)
    else:
        res = 1
    
    return res



def callTrainNN():
    msg = "rosrun neural_network NN_trainer.py"
    res = os.system(msg)

    return res
        


@app.route('/')
def home():
    return render_template('home.html')



@app.route('/page1')
def page1():
    return render_template('page1.html')



@app.route('/page2')
def page2():
    return render_template('page2.html')



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
    print(res)
    return jsonify(result=res)



@app.route('/sendTrainingNNRequest', methods=['SEND'])
def startTraining():
    res = callTrainNN()
    return jsonify(result=res)



@app.route('/sendExecuteTrajectoryRequest', methods=['SEND'])
def exec():
    data = request.get_json()
    data = data[5:-4]
    res = main(data)
    return jsonify(result=res)




if __name__ == '__main__':   
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:5000/')

    app.run(debug=True)
