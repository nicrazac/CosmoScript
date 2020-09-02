import sqlite3
from sqlite3 import Error
import matplotlib.pyplot as plt
import numpy as np
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
    generateMap = ObjectProperty(None)
    plot = ObjectProperty(None)
    
    #Generates Map
    def genMap(self):
        try:
            xRange = int(self.sizeX.text) + 1
            yRange = int(self.sizeY.text) + 1
        except:
            return
        if int(self.sizeX.text) and int(self.sizeY.text):
            fig = plt.figure()
            ax = fig.add_subplot(1,1,1)
            xTicks = np.arange(0, xRange, 1)
            yTicks = np.arange(0, yRange, 1)
            ax.set_xticks(xTicks)
            ax.set_yticks(yTicks)
            ax.grid(which='both')
            self.ids.gridPlot.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
#APP Class
class MyApp(App):
    def build(self):
        self.title = "My DB Practice"
        return MainClass()

#Runs Loop
if __name__ == '__main__':
    MyApp().run()
