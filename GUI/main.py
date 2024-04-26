from kivy.uix.accordion import Widget
from kivy.uix.accordion import Animation
import kivy
import queue, threading, random,time,os

#Loads the config file
from kivy.config import Config
Config.read("screen_config.cfg")

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.properties import NumericProperty


#Builder.load_file("tester.kv")

#Loads the kv files, that dictate look, feel, and behavior of the GUI 
Builder.load_file("menu.kv")
Builder.load_file("settings.kv")
Builder.load_file("loading.kv")

class MENUSCREEN(Screen):
    pass


class SETTINGSSCREEN(Screen):      
    pass

class RESULTSSCREEN(Screen):
    pass

class LOADINGSCREEN(Screen):    
    pass

class SPINRECTANGLE(Widget):
    angle = NumericProperty(0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        anim = Animation(angle = -360, duration=2) 
        anim += Animation(angle = -360, duration=2)
        anim.repeat = True
        anim.start(self)
    def on_angle(self, item, angle):
        if angle == -360:
            item.angle = 0
   
    

class TESTERGUI(App):    
    sm = ScreenManager()
    sineWavePt = list()
    isDone = -1
    
    #Data used in the .kv files for color and other uses
    INPUTS = ('GMA Output 1', 'GMA Output 2', 'GMA Output 3', 'GMA Output 4', 'GMA Output 5', 'GMA Output 6', 'GMA Output 7', 'GMA Output 8')
    STEELBLUE = (0.2471, 0.5333, 0.7726, 1)
    PINEGREEN = (0.0745, 0.4353, 0.3882, 1)
    ENGORANGE = (0.8157, 0.0000, 0.0000, 1)
    SELYELLOW = (1.0000, 0.7294, 0.0314, 1)
    PRUSSBLUE = (0.0118, 0.1686, 0.2627, 1)
    Thresholds = list()
   
   
    def wasteTime(self):
        thistime = time.time() 
        while thistime + 5 > time.time(): # 5 seconds
            time.sleep(1)
        self.isDone = 1
        print("time wasting done")
        pass
            
         
    #Defines the Behavior when the Start Test button is pressed
    #This button is located with in the 'menu' screen
    def startTest(self, text):
        self.sm.current = 'loading'
        print(text)
        myThread = threading.Thread(target = self.wasteTime)
        myThread.start()    
        #still working on showing the loading screen synchoroly while doing something else   
        while self.isDone < 0:
           pass
        self.sm.current = 'menu'
    
    def switchLoading(self):
        self.sm.current = 'loading'
           
    
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
        self.sm.add_widget(LOADINGSCREEN(name = 'loading'))            
        return self.sm
    
if __name__ == '__main__':
    TESTERGUI().run()