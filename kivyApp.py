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
    
    #Initializations
    location = [0,0]
    xTicks = 0
    yTicks = 0
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    #Generates Map
    def genMap(self):
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
            #fig = plt.figure()
            #ax = self.fig.add_subplot(1,1,1)
            plt.scatter(xStart, yStart)
            self.xTicks = np.arange(0, xRange, 1)
            self.yTicks = np.arange(0, yRange, 1)
            self.ax.set_xticks(self.xTicks)
            self.ax.set_yticks(self.yTicks)
            self.ax.grid(which='both')
            self.ids.gridPlot.add_widget(FigureCanvasKivyAgg(plt.gcf()))
            return
            
        if self.gName.text != '' and path.exists(self.gName.text + '.db') == False:
            try:
                xRange = int(self.sizeX.text)
                yRange = int(self.sizeY.text)
                xStart = int(self.startX.text)
                yStart = int(self.startY.text)
                dbName = self.gName.text
                author = self.gAuthor.text
            except:
                return
            con = sqlite3.connect(dbName + '.db')
            cursor = con.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS setup(id integer PRIMARY KEY AUTOINCREMENT, title text, author text, sizeX integer, sizeY integer, startX integer, startY integer)")
            con.commit()
            cursor.execute("CREATE TABLE IF NOT EXISTS spots(id integer PRIMARY KEY AUTOINCREMENT, xLoc integer, yLoc integer, name text)")
            con.commit()
            cursor.execute("INSERT INTO setup (title, author, sizeX, sizeY, startX, startY) VALUES (?,?,?,?,?,?)", (dbName, author, xRange, yRange, xStart, yStart))
            con.commit()
            cursor.execute("INSERT INTO spots (xLoc, yLoc) VALUES (?,?)", (xStart, yStart))
            con.commit()
            self.location[0] = xStart
            self.location[1] = yStart
            self.ids.gridPlot.clear_widgets()
            #fig = plt.figure()
            #ax = self.fig.add_subplot(1,1,1)
            plt.scatter(xStart, yStart)
            self.xTicks = np.arange(0, xRange, 1)
            self.yTicks = np.arange(0, yRange, 1)
            self.ax.set_xticks(self.xTicks)
            self.ax.set_yticks(self.yTicks)
            self.ax.grid(which='both')
            self.ids.gridPlot.add_widget(FigureCanvasKivyAgg(plt.gcf()))
            return
    
    def moveLeft(self):
        self.ids.gridPlot.clear_widgets()
        self.location[0] = self.location[0] - 1
        plt.scatter(self.location[0], self.location[1])
        self.ax.set_xticks(self.xTicks)
        self.ax.set_yticks(self.yTicks)
        self.ids.gridPlot.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
    def moveRight(self):
        self.ids.gridPlot.clear_widgets()
        self.location[0] = self.location[0] + 1
        plt.scatter(self.location[0], self.location[1])
        self.ax.set_xticks(self.xTicks)
        self.ax.set_yticks(self.yTicks)
        self.ids.gridPlot.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
    def moveUp(self):
        self.ids.gridPlot.clear_widgets()
        self.location[1] = self.location[1] + 1
        plt.scatter(self.location[0], self.location[1])
        self.ax.set_xticks(self.xTicks)
        self.ax.set_yticks(self.yTicks)
        self.ids.gridPlot.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
    def moveDown(self):
        self.ids.gridPlot.clear_widgets()
        self.location[1] = self.location[1] - 1
        plt.scatter(self.location[0], self.location[1])
        self.ax.set_xticks(self.xTicks)
        self.ax.set_yticks(self.yTicks)
        self.ids.gridPlot.add_widget(FigureCanvasKivyAgg(plt.gcf()))    
        
#APP Class
class MyApp(App):
    def build(self):
        self.title = "CS"
        return MainClass()

#Runs Loop
if __name__ == '__main__':
    MyApp().run()
