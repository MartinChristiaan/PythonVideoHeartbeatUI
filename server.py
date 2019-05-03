from flask import Flask,Response
from flask import render_template
import os
from os import path
from flask import request
import json
from flask_cors import CORS
import math



def create_server(uiInstructions,createCamera):
    """Receives list of uiElements that handle interaction with their specified classes"""
    app = Flask(__name__)
    CORS(app)
    uiElements = []
    figures = []
    def getUIInstructions():
        communicationString = ""       
        for element in uiInstructions:
            elementIndex = len(uiElements)
            uiElements.append(element)
            instructions = element.getInstructions()
            print(instructions)
            noitems = len(instructions)+1 # for index

            instructions = [str(value) for value in instructions]            
            if instructions[0] == "figure":
                figures.append(element)
                                            # no items , elementype(example = slider) , index to retrieve element, the rest of the instructions 
            communicationString+= ",".join([str(noitems),str(elementIndex)]+instructions)+","

        print(communicationString)
        return communicationString[:-1]

    instructionstring = getUIInstructions()

    @app.route("/")
    @app.route('/getInstructions')
    def getInstructions():
        return instructionstring

    @app.route('/UIUpdate',methods=['PUT'])
    def updateField():
        value = request.form['value']
        uiindex = int(request.form['index'])
        uiElement = uiElements[uiindex]
        uiElement.updateValue(value)
        uiElement.performUpdate()
        #serialization.saveJson(uiElement.myclass)
        return "OK"

    def gen(camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


    @app.route('/video_feed')
    def video_feed():
        return Response(gen(createCamera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    @app.route('/figureUpdate')
    def figureUpdates():
        communicationstring= ""
        for figure in figures:
            instructions = [str(instr) for instr in figure.getUpdateInstructions()]
            communicationstring+= ",".join(instructions)+","
        
        return communicationstring[:-1]        
    
    return app




