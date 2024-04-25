import kivy
import os

#Loads the config file
from kivy.config import Config
Config.read("screen_config.cfg")

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen


#Builder.load_file("tester.kv")

#Loads the kv files, that dictate look, feel, and behavior of the GUI 
Builder.load_file("menu.kv")
Builder.load_file("settings.kv")

class MENUSCREEN(Screen):
    pass


class SETTINGSSCREEN(Screen):      
    pass

class RESULTSSCREEN(Screen):
    pass

class TESTERGUI(App):    
    sm = ScreenManager()
    
    
    #Data used in the .kv files for color and other uses
    INPUTS = ('GMA Output 1', 'GMA Output 2', 'GMA Output 3', 'GMA Output 4', 'GMA Output 5', 'GMA Output 6', 'GMA Output 7', 'GMA Output 8')
    STEELBLUE = (0.2471, 0.5333, 0.7726, 1)
    PINEGREEN = (0.0745, 0.4353, 0.3882, 1)
    ENGORANGE = (0.8157, 0.0000, 0.0000, 1)
    SELYELLOW = (1.0000, 0.7294, 0.0314, 1)
    PRUSSBLUE = (0.0118, 0.1686, 0.2627, 1)
    Thresholds = list()
    
    #Defines the Behavior when the Start Test button is pressed
    #This button is located with in the 'menu' screen
    def startTest(self, text):
        print(text) 
    
    #Defines the Behavior when the Export button is pressed
    #This button is located with in the 'menu' screen
    def export(self, text):
        print(text)
    
    def save(self):           
        self.Thresholds.append(self.sm.current_screen.ids.thresholdInput_1.text)    
        self.Thresholds.append(self.sm.current_screen.ids.thresholdInput_2.text)
        self.Thresholds.append(self.sm.current_screen.ids.thresholdInput_3.text)
        self.Thresholds.append(self.sm.current_screen.ids.thresholdInput_4.text)
        self.Thresholds.append(self.sm.current_screen.ids.thresholdInput_5.text)
        self.Thresholds.append(self.sm.current_screen.ids.thresholdInput_6.text)
        self.Thresholds.append(self.sm.current_screen.ids.thresholdInput_7.text)
        self.Thresholds.append(self.sm.current_screen.ids.thresholdInput_8.text)      
        for i in self.Thresholds:
            print(i)       
        self.sm.current = 'menu'
        
    def build(self):        
        self.sm.add_widget(MENUSCREEN(name = 'menu'))   
        self.sm.add_widget(SETTINGSSCREEN(name = 'settings'))                 
        return self.sm
    
if __name__ == '__main__':
    TESTERGUI().run()