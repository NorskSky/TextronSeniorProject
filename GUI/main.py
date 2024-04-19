import kivy
import os

#Loads the config file
from kivy.config import Config
Config.read("screen_config.cfg")

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen


Builder.load_file("tester.kv")

class MENUSCREEN(Screen):
    pass


class SETTINGSSCREEN(Screen):
    pass

class TESTERGUI(App):    
    sm = ScreenManager()
    #Defines the Behavior when the Start Test button is pressed
    #This button is located with in the 'menu' screen
    def startTest(self, text):
        print(text) 
    
    #Defines the Behavior when the Export button is pressed
    #This button is located with in the 'menu' screen
    def export(self, text):
        print(text)
    
        
    def build(self):        
        self.sm.add_widget(MENUSCREEN(name = 'menu'))   
        self.sm.add_widget(SETTINGSSCREEN(name = 'settings'))             
        return self.sm
    
if __name__ == '__main__':
    TESTERGUI().run()