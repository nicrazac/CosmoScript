import sqlite3
from sqlite3 import Error
import matplotlib.pyplot as plt
import numpy as np
import os.path
from os import path
import kivy
kivy.require('1.11.1')
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image

kv = Builder.load_file("kivyApp.kv")

class MainClass(TabbedPanel):

    #Connects ids to kv file
    sizeX = ObjectProperty(None)
    sizeY = ObjectProperty(None)
    startX = ObjectProperty(None)
    startY = ObjectProperty(None)
    gName = ObjectProperty(None)
    gAuthor = ObjectProperty(None)
    generateMap = ObjectProperty(None)
    plot = ObjectProperty(None)
    left = ObjectProperty(None)
    right = ObjectProperty(None)
    up = ObjectProperty(None)
    down = ObjectProperty(None)
    locationCall = ObjectProperty(None)
    nameDesc = ObjectProperty(None)
    lookDesc = ObjectProperty(None)
    itemList = ObjectProperty(None)
    radioNorth = ObjectProperty(None)
    radioEast = ObjectProperty(None)
    radioSouth = ObjectProperty(None)
    radioWest = ObjectProperty(None)
    northTags = ObjectProperty(None)
    eastTags = ObjectProperty(None)
    southTags = ObjectProperty(None)
    westTags = ObjectProperty(None)
    fileChooser = ObjectProperty(None)
    mainImage = ObjectProperty(None)
    
    #Initializations
    location = [0,0]
    xTicks = 0
    yTicks = 0
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    tempLoc = ax.plot()
    permLoc = ax.plot()
    tempFile = ''
    global dbName
    
    #Generates Map
    def genMap(self):
        global dbName
        if self.gName.text != '' and path.exists(self.gName.text + '.db'):
            dbName = self.gName.text
            con = sqlite3.connect(dbName + '.db')
            cursor = con.cursor()
            cursor.execute("SELECT sizeX, sizeY, startX, startY FROM setup WHERE id = 1")
            setupData = cursor.fetchall()[0]
            xRange = setupData[0]
            yRange = setupData[1]
            xStart = setupData[2]
            yStart = setupData[3]
            self.location[0] = xStart
            self.location[1] = yStart
            self.ids.gridPlot.clear_widgets()
            cursor.execute("SELECT * FROM spots")
            spotRes = cursor.fetchall()
            for point in spotRes:
                self.permLoc, = self.ax.plot(point[1],point[2],'bo')
            self.tempLoc, = self.ax.plot(xStart, yStart, 'ro')
            self.xTicks = np.arange(0, xRange, 1)
            self.yTicks = np.arange(0, yRange, 1)
            self.ax.set_xticks(self.xTicks)
            self.ax.set_yticks(self.yTicks)
            self.ax.grid(which='both')
            self.ids.gridPlot.add_widget(FigureCanvasKivyAgg(plt.gcf()))
            self.locationCall.text = "Location: ("+str(self.location[0])+","+str(self.location[1])+")"
            self.loadSpot(self.location[0],self.location[1])
            return
            
        if self.gName.text != '' and path.exists(self.gName.text + '.db') == False:
            try:
                xRange = int(self.sizeX.text)
                yRange = int(self.sizeY.text)
                xStart = int(self.startX.text)
                yStart = int(self.startY.text)
            except:
                return
            dbName = self.gName.text
            author = self.gAuthor.text
            con = sqlite3.connect(dbName + '.db')
            cursor = con.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS setup(id integer PRIMARY KEY AUTOINCREMENT, title text, author text, sizeX integer, sizeY integer, startX integer, startY integer)")
            con.commit()
            cursor.execute("CREATE TABLE IF NOT EXISTS spots(id integer PRIMARY KEY AUTOINCREMENT, xLoc integer, yLoc integer, name text, description text, items text, north integer, east integer, south integer, west integer, northList text, eastList text, southList text, westList text, image blob)")
            con.commit()
            cursor.execute("INSERT INTO setup (title, author, sizeX, sizeY, startX, startY) VALUES (?,?,?,?,?,?)", (dbName, author, xRange, yRange, xStart, yStart))
            con.commit()
            cursor.execute("INSERT INTO spots (xLoc, yLoc) VALUES (?,?)", (xStart, yStart))
            con.commit()
            self.location[0] = xStart
            self.location[1] = yStart
            self.ids.gridPlot.clear_widgets()
            cursor.execute("SELECT * FROM spots")
            spotRes = cursor.fetchall()
            for point in spotRes:
                self.permLoc, = self.ax.plot(point[1],point[2],'bo')
            self.tempLoc, = self.ax.plot(xStart, yStart, 'ro')
            self.xTicks = np.arange(0, xRange, 1)
            self.yTicks = np.arange(0, yRange, 1)
            self.ax.set_xticks(self.xTicks)
            self.ax.set_yticks(self.yTicks)
            self.ax.grid(which='both')
            self.ids.gridPlot.add_widget(FigureCanvasKivyAgg(plt.gcf()))
            self.locationCall.text = "Current Location: ("+str(self.location[0])+","+str(self.location[1])+")"
            self.loadSpot(self.location[0],self.location[1])
            return
    
    def moveLeft(self):
        self.ids.gridPlot.clear_widgets()
        self.tempLoc.remove()
        self.location[0] = self.location[0] - 1
        self.tempLoc, = self.ax.plot(self.location[0], self.location[1], 'ro')
        self.ax.set_xticks(self.xTicks)
        self.ax.set_yticks(self.yTicks)
        self.ids.gridPlot.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        self.locationCall.text = "Current Location: ("+str(self.location[0])+","+str(self.location[1])+")"
        self.loadSpot(self.location[0],self.location[1])
        self.cleanUp(self.tempFile)
        
    def moveRight(self):
        self.ids.gridPlot.clear_widgets()
        self.tempLoc.remove()
        self.location[0] = self.location[0] + 1
        self.tempLoc, = self.ax.plot(self.location[0], self.location[1], 'ro')
        self.ax.set_xticks(self.xTicks)
        self.ax.set_yticks(self.yTicks)
        self.ids.gridPlot.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        self.locationCall.text = "Current Location: ("+str(self.location[0])+","+str(self.location[1])+")"
        self.loadSpot(self.location[0],self.location[1])
        self.cleanUp(self.tempFile)
        
    def moveUp(self):
        self.ids.gridPlot.clear_widgets()
        self.tempLoc.remove()
        self.location[1] = self.location[1] + 1
        self.tempLoc, = self.ax.plot(self.location[0], self.location[1], 'ro')
        self.ax.set_xticks(self.xTicks)
        self.ax.set_yticks(self.yTicks)
        self.ids.gridPlot.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        self.locationCall.text = "Current Location: ("+str(self.location[0])+","+str(self.location[1])+")"
        self.loadSpot(self.location[0],self.location[1])
        self.cleanUp(self.tempFile)
        
    def moveDown(self):
        self.ids.gridPlot.clear_widgets()
        self.tempLoc.remove()
        self.location[1] = self.location[1] - 1
        self.tempLoc, = self.ax.plot(self.location[0], self.location[1], 'ro')
        self.ax.set_xticks(self.xTicks)
        self.ax.set_yticks(self.yTicks)
        self.ids.gridPlot.add_widget(FigureCanvasKivyAgg(plt.gcf()))   
        self.locationCall.text = "Current Location: ("+str(self.location[0])+","+str(self.location[1])+")"
        self.loadSpot(self.location[0],self.location[1])
        self.cleanUp(self.tempFile)

    def loadSpot(self,xLoc,yLoc):
        global dbName
        con = sqlite3.connect(dbName + '.db')
        cursor = con.cursor()
        cursor.execute("SELECT id, name, description, items, north, east, south, west, northList, eastList, southList, westList, image FROM spots WHERE xLoc = ? AND yLoc = ?", (xLoc, yLoc))
        dataRes = cursor.fetchall()
        try:
            self.nameDesc.text = dataRes[0][1]
        except:
            self.nameDesc.text = ''
        try:
            self.lookDesc.text = dataRes[0][2]
        except:
            self.lookDesc.text = ''
        try:
            self.itemList.text = dataRes[0][3]
        except:
            self.itemList.text = ''
        try:
            self.radioNorth.active = dataRes[0][4]
            self.enableNorth()
        except:
            self.radioNorth.active = 0
            self.enableNorth()
        try:
            self.radioEast.active = dataRes[0][5]
            self.enableEast()
        except:
            self.radioEast.active = 0
            self.enableEast()
        try:
            self.radioSouth.active = dataRes[0][6]
            self.enableSouth()
        except:
            self.radioSouth.active = 0
            self.enableSouth()
        try:
            self.radioWest.active = dataRes[0][7]
            self.enableWest()
        except:
            self.radioWest.active = 0
            self.enableWest()
        try:
            self.northTags.text = dataRes[0][8]
        except:
            self.northTags.text = ''
        try:
            self.eastTags.text = dataRes[0][9]
        except:
            self.eastTags.text = ''
        try:
            self.southTags.text = dataRes[0][10]
        except:
            self.southTags.text = ''
        try:
            self.westTags.text = dataRes[0][11]
        except:
            self.westTags.text = ''
        try:
            self.tempFile = "image" + str(dataRes[0][0])+".jpg"
            filename = "image" + str(dataRes[0][0])+".jpg"
            image = open(filename, "wb")
            image.write(dataRes[0][12])
            image.close()
            self.ids.mainImage.source = "image" + str(dataRes[0][0])+ ".jpg"
        except:
            self.ids.mainImage.source = ""
            
    def cleanUp(self, filename):
        try:
            os.remove(filename)
        except:
            pass
            
    def updateName(self):
        global dbName
        con = sqlite3.connect(dbName + '.db')
        cursor = con.cursor()
        cursor.execute("UPDATE spots SET name = ? WHERE xLoc = ? AND yLoc = ?", (self.nameDesc.text, self.location[0], self.location[1]))
        con.commit()

    def updateLook(self):
        global dbName
        con = sqlite3.connect(dbName + '.db')
        cursor = con.cursor()
        cursor.execute("UPDATE spots SET description = ? WHERE xLoc = ? AND yLoc = ?", (self.lookDesc.text, self.location[0], self.location[1]))
        con.commit()
        
    def updateItems(self):
        global dbName
        con = sqlite3.connect(dbName + '.db')
        cursor = con.cursor()
        cursor.execute("UPDATE spots SET items = ? WHERE xLoc = ? AND yLoc = ?", (self.itemList.text, self.location[0], self.location[1]))
        con.commit()

    def commitSpot(self):
        global dbName
        con = sqlite3.connect(dbName + '.db')
        cursor = con.cursor()
        cursor.execute("INSERT INTO spots (xLoc, yLoc) VALUES (?, ?)", (self.location[0], self.location[1]))
        con.commit()
        self.ids.gridPlot.clear_widgets()
        self.permLoc, = self.ax.plot(self.location[0],self.location[1],'bo')
        self.tempLoc, = self.ax.plot(self.location[0], self.location[1], 'ro')
        self.ax.set_xticks(self.xTicks)
        self.ax.set_yticks(self.yTicks)
        self.ids.gridPlot.add_widget(FigureCanvasKivyAgg(plt.gcf()))
    
    def deleteSpot(self):
        global dbName
        con = sqlite3.connect(dbName + '.db')
        cursor = con.cursor()
        cursor.execute("DELETE FROM spots WHERE xLoc = ? AND yLoc = ?", (self.location[0], self.location[1]))
        con.commit()
        self.ids.gridPlot.clear_widgets()
        self.ax.clear()
        cursor.execute("SELECT sizeX, sizeY FROM setup WHERE id = 1")
        setupData = cursor.fetchall()[0]
        xRange = setupData[0]
        yRange = setupData[1]
        cursor.execute("SELECT * FROM spots")
        spotRes = cursor.fetchall()
        for point in spotRes:
            self.permLoc, = self.ax.plot(point[1],point[2],'bo')
        self.tempLoc, = self.ax.plot(self.location[0], self.location[1], 'ro')
        self.xTicks = np.arange(0, xRange, 1)
        self.yTicks = np.arange(0, yRange, 1)
        self.ax.set_xticks(self.xTicks)
        self.ax.set_yticks(self.yTicks)
        self.ax.grid(which='both')
        self.ids.gridPlot.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
    def enableNorth(self):
        if self.radioNorth.active == True:
            self.northTags.disabled = False
        else:
            self.northTags.disabled = True
            
    def enableEast(self):
        if self.radioEast.active == True:
            self.eastTags.disabled = False
        else:
            self.eastTags.disabled = True
            
    def enableSouth(self):
        if self.radioSouth.active == True:
            self.southTags.disabled = False
        else:
            self.southTags.disabled = True
            
    def enableWest(self):
        if self.radioWest.active == True:
            self.westTags.disabled = False
        else:
            self.westTags.disabled = True
            
    def updateDirections(self):
        global dbName
        con = sqlite3.connect(dbName + '.db')
        cursor = con.cursor()
        if self.radioNorth.active == True:
            cursor.execute("UPDATE spots SET north = 1, northList = ? WHERE xLoc = ? AND yLoc = ?", (self.northTags.text, self.location[0], self.location[1]))
            con.commit()
        else:
            cursor.execute("UPDATE spots SET north = 0")
            con.commit()
        if self.radioEast.active == True:
            cursor.execute("UPDATE spots SET east = 1, eastList = ? WHERE xLoc = ? AND yLoc = ?", (self.eastTags.text, self.location[0], self.location[1]))
            con.commit()
        else:
            cursor.execute("UPDATE spots SET east = 0")
            con.commit()
        if self.radioSouth.active == True:
            cursor.execute("UPDATE spots SET south = 1, southList = ? WHERE xLoc = ? AND yLoc = ?", (self.southTags.text, self.location[0], self.location[1]))
            con.commit()
        else:
            cursor.execute("UPDATE spots SET south = 0")
            con.commit()
        if self.radioWest.active == True:
            cursor.execute("UPDATE spots SET west = 1, westList = ? WHERE xLoc = ? AND yLoc = ?", (self.westTags.text, self.location[0], self.location[1]))
            con.commit()
        else:
            cursor.execute("UPDATE spots SET west = 0")
            con.commit()
        
    def uploadImage(self):
        global dbName
        con = sqlite3.connect(dbName + '.db')
        cursor = con.cursor()
        try:
            self.ids.mainImage.source = self.fileChooser.selection[0]
            with open(self.fileChooser.selection[0], 'rb') as file:
                blobData = file.read()
            cursor.execute("UPDATE spots SET image = ? WHERE xLoc = ? AND yLoc = ?", (blobData, self.location[0], self.location[1]))
            con.commit()
        except:
            pass
            
    def deleteImage(self):
        global dbName
        con = sqlite3.connect(dbName + '.db')
        cursor = con.cursor()
        cursor.execute("DELETE image FROM spots WHERE xLoc = ? AND yLoc = ?", (self.location[0], self.location[1]))
        con.commit()
        
#APP Class
class MyApp(App):
    def build(self):
        self.title = "CS"
        return MainClass()

#Runs Loop
if __name__ == '__main__':
    MyApp().run()
