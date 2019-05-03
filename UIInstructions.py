from flask import Flask
from flask import render_template
import os
from os import path
import json
import csv

# This file defines the UI elements that can be made. 

inputDataPath = "input.json"
flatten = lambda l: [item for sublist in l for item in sublist]



class UIElement:
    def __init__(self,fieldname,classname,uiname,onupdate,myclass):   
        self.fieldname = fieldname
        self.uiname = uiname
        self.onupdate = onupdate
        self.classname = classname
        self.value = myclass.__dict__[fieldname]
        self.myclass = myclass

    def performUpdate(self):
        if self.onupdate!=None:
           getattr(self.myclass, self.onupdate)()

class Switch(UIElement):
    def __init__(self,fieldname,classname,uiname,myclass,onupdate):
        UIElement.__init__(self,fieldname,classname,uiname,onupdate,myclass)

    def getInstructions(self):
        return ["switch",self.classname,self.uiname,self.value]

    def updateValue(self,_):
        self.myclass.__dict__[self.fieldname] = not self.myclass.__dict__[self.fieldname] 

class Slider(UIElement):
    def __init__(self,fieldname,classname,uiname,min,max,myclass,onupdate):
        UIElement.__init__(self,fieldname,classname,uiname,onupdate,myclass)
        self.min = min
        self.max = max
    def getInstructions(self):
        return ["slider",self.classname,self.uiname, self.min,self.max,self.value]
    
    def updateValue(self,value):
        self.myclass.__dict__[self.fieldname] = float(value)
        
class Button():
    def __init__(self,classname,uiname,myclass,onclick):
        self.uiname = uiname
        self.onclick = onclick
        self.classname = classname
        self.myclass = myclass
        
    def performUpdate(self):
        if self.onclick!=None:
           getattr(self.myclass, self.onclick)()
    def getInstructions(self):
        return ["button",self.classname,self.uiname]
    
    def updateValue(self,value):
        pass
    
class Dropdown(UIElement):
    def __init__(self,fieldname,classname,uiname,myclass,options,optionlabels,onupdate):
        UIElement.__init__(self,fieldname,classname,uiname,onupdate,myclass)
        if isinstance(self.value, (list,)):
            self.value = tuple(self.value)
        try:
            self.value = optionlabels[options.index((self.value))]
        except:
            for i,option in enumerate(options):
                if type(option) == type(self.value):
                    self.value = optionlabels[i]
        self.options = options
        self.optionlabels = optionlabels
        # Maybe also execute some callback in myclass
  
    def getInstructions(self):
        return ["dropdown",self.classname,self.uiname,self.value] + self.optionlabels 

    def updateValue(self,label):
        self.myclass.__dict__[self.fieldname] = self.options[self.optionlabels.index(label)]
   

class AddingFigure():
    def updateValues(self):
        self.t += 0.01
        self.y = [self.myclass.__dict__[yFieldName] for yFieldName in self.yfieldnames]

    def __init__(self,myclass,xfieldName,yFieldNames,xname,ynames):
        self.xfieldname = xfieldName
        self.yfieldnames = yFieldNames
        self.myclass = myclass      
        self.ynames= ynames
        self.updatePol = "Add"
        self.t = 0
        self.y = [self.myclass.__dict__[yFieldName] for yFieldName in self.yfieldnames]
        
    def getInstructions(self):
        return ["figure",0,len(self.y),self.updatePol,"Time"] + self.ynames + [self.t] + self.y

    def getUpdateInstructions(self):
        self.updateValues()
        return [1,len(self.y), self.t] + self.y


class ReplacingFigure():
    def updateValues(self):
        self.x = self.myclass.__dict__[self.xfieldname]
        self.y = [self.myclass.__dict__[yFieldName] for yFieldName in self.yfieldnames]

    def __init__(self,myclass,xfieldName,yFieldNames,xname,ynames):
        self.xfieldname = xfieldName
        self.yfieldnames = yFieldNames
        self.xname = xname
        self.myclass = myclass      
        self.ynames= ynames
        self.updatePol = "Replace"
        self.updateValues()
        
    def getInstructions(self):
        yflat =flatten(self.y)
        print(yflat)
        return ["figure",len(self.x),len(self.y),self.updatePol,self.xname] + self.ynames + list(self.x) + yflat

    def getUpdateInstructions(self):
        self.updateValues()
        # A way to also update x may need to be added in the future.
        return [len(self.x),len(self.y)] + list(self.x) + flatten(self.y)


