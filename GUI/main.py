import kivy
import threading, time, random, os
#from pathlib import Path, PurePath

#Loads the config file
from kivy.config import Config
Config.read("screen_config.cfg")

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.properties import NumericProperty
from kivy.uix.accordion import Widget
from kivy.uix.accordion import Animation
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.properties import ObjectProperty

#Builder.load_file("tester.kv")

#Loads the kv files, that dictate look, feel, and behavior of the GUI 
Builder.load_file("kv_files/menu.kv")
Builder.load_file("kv_files/settings.kv")
Builder.load_file("kv_files/loading.kv")
Builder.load_file("kv_files/results.kv")

class MENUSCREEN(Screen):
    
    def shutdown(self):
        if self.ids.pwrBt.collide_point(self.ids.pwrBt.x, self.ids.pwrBt.y):       
            os.system("shutdown -h now")              
    pass


class SETTINGSSCREEN(Screen):     
   pass
    

class RESULTSSCREEN(Screen):
    Outputs = [ObjectProperty]*8 
    Results = [ObjectProperty]*8     
        
    
    def on_pre_enter(self):
        self.Outputs[0] = self.ids.Output1
        self.Outputs[1] = self.ids.Output2
        self.Outputs[2] = self.ids.Output3
        self.Outputs[3] = self.ids.Output4
        self.Outputs[4] = self.ids.Output5
        self.Outputs[5] = self.ids.Output6
        self.Outputs[6] = self.ids.Output7
        self.Outputs[7] = self.ids.Output8
        
        self.Results[0] = self.ids.Result1
        self.Results[1] = self.ids.Result2
        self.Results[2] = self.ids.Result3
        self.Results[3] = self.ids.Result4
        self.Results[4] = self.ids.Result5
        self.Results[5] = self.ids.Result6
        self.Results[6] = self.ids.Result7
        self.Results[7] = self.ids.Result8
        
        for i in range(0,8):            
            if self.Outputs[i].text != "Not Selected |":
                self.Outputs[i].color = (0,0,0,1)
            
                    
                
                
            
        print("on pre enter for results has been entered")
    
    def updateOutputs(self, outputs):
        for i in range(0, 8):                 
            if outputs[i] != "Not Selected":                
                self.Outputs[i].text = outputs[i] + ' @ FTM Input ' + str(i+1) + ' |' 
    
    def updateResults(self, results):
        for i in range(0, 8):                 
            if results[i] != "Not Selected":                
                self.Results[i].text = results[i]                 
                if self.Results[i].text == "Pass":                    
                    self.Results[i].color = (0.0000, 0.5019, 0.0000, 1)
                else:
                    self.Results[i].color = (0.8157, 0.0000, 0.0000, 1)
                
            
    

class LOADING(Popup):    
    pass

#Both the SPINRECTANGLE classes are use to create the loading screen animation
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

class SPINRECTANGLE2(Widget):
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

class RESULTSSTORAGE():    
    Data = ["Default data"] * 8
    Pass = ["Not Selected"] * 8    
    
    
            

class COLORS():
    STEELBLUE = (0.2471, 0.5333, 0.7726, 1)
    PINEGREEN = (0.0745, 0.4353, 0.3882, 1)
    ENGORANGE = (0.8157, 0.0000, 0.0000, 1)
    SELYELLOW = (1.0000, 0.7294, 0.0314, 1)
    PRUSSBLUE = (0.0118, 0.1686, 0.2627, 1)
    WHITE = (1.0000, 1.0000, 1.000, 1)
    BLACK = (0.0000, 0.0000, 0.000, 1)
    

class TESTERGUI(App):    
    sm = ScreenManager()
    #Data used in the .kv files for color and other uses
    colors = COLORS()
    results = RESULTSSTORAGE()  
    
      
    INPUTS = ('GMA Output 1', 'GMA Output 2', 'GMA Output 3', 'GMA Output 4', 'GMA Output 5', 'GMA Output 6', 'GMA Output 7', 'GMA Output 8')
    Thresholds = [""] * 8
    OutputsSelected = ["Not Selected"] * 8
    
   
   
    def wasteTime(self):
        
        thistime = time.time()         
        while thistime + 5 > time.time(): # 5 seconds
            time.sleep(1)
        for i in range(0,8):
            if self.OutputsSelected[i] != "Not Selected": 
                if random.randint(-2,2) > 0:
                    self.results.Pass[i] = "Pass"
                else:
                    self.results.Pass[i] = "Fail"   
        self.sm.get_screen('results').updateResults(self.results.Pass)
        print("time wasting done")              
        self.pop_up.dismiss()           
    
 
    #Pops up the loading screen while the analysis happens
    def showLoading(self):       
        self.pop_up = Factory.LOADING()        
        self.pop_up.open()
        
    #Defines the Behavior when the Start Test button is pressed
    #This button is located with in the 'menu' screen
    def startTest(self, text):
        print(text)
        if self.sm.get_screen('menu').ids.testStBt.collide_point(self.get_screen('menu').ids.testStBt.x, self.get_screen('menu').ids.testStBt.y):          
            self.showLoading()       
        
            mythread = threading.Thread(target=self.wasteTime)
            mythread.start()  
            self.sm.current = 'results' 
        
        
    
    #Defines the Behavior when the Export button is pressed
    #This button is located with in the 'menu' screen
    def export(self, text):
        print(text)
    
    #Defined the Behavior of the Save button located in the Settings Screen
    #Save test parameters to a set of data structures
    def save(self):
                   
        #saving Threshold Values        
        self.Thresholds[0] = (self.sm.current_screen.ids.thresholdInput_1.text)    
        self.Thresholds[1] = (self.sm.current_screen.ids.thresholdInput_2.text)
        self.Thresholds[2] = (self.sm.current_screen.ids.thresholdInput_3.text)
        self.Thresholds[3] = (self.sm.current_screen.ids.thresholdInput_4.text)
        self.Thresholds[4] = (self.sm.current_screen.ids.thresholdInput_5.text)
        self.Thresholds[5] = (self.sm.current_screen.ids.thresholdInput_6.text)
        self.Thresholds[6] = (self.sm.current_screen.ids.thresholdInput_7.text)
        self.Thresholds[7] = (self.sm.current_screen.ids.thresholdInput_8.text)
       
        #Saving GMA Selected Outputs        
        self.OutputsSelected[0] = (self.sm.current_screen.ids.dropdown_1.text)    
        self.OutputsSelected[1] = (self.sm.current_screen.ids.dropdown_2.text)
        self.OutputsSelected[2] = (self.sm.current_screen.ids.dropdown_3.text)
        self.OutputsSelected[3] = (self.sm.current_screen.ids.dropdown_4.text)
        self.OutputsSelected[4] = (self.sm.current_screen.ids.dropdown_5.text)
        self.OutputsSelected[5] = (self.sm.current_screen.ids.dropdown_6.text)
        self.OutputsSelected[6] = (self.sm.current_screen.ids.dropdown_7.text)
        self.OutputsSelected[7] = (self.sm.current_screen.ids.dropdown_8.text)         
        
        #Updates the result screen with the correct data 
        self.sm.current = 'results'
            
        self.sm.get_screen('results').updateOutputs(self.OutputsSelected)
        self.sm.current = 'menu'
   
    def shutdown(self):
        os.system("shutdown -h now")          
    def build(self):          
        self.sm.add_widget(MENUSCREEN(name = 'menu'))   
        self.sm.add_widget(SETTINGSSCREEN(name = 'settings'))     
        self.sm.add_widget(RESULTSSCREEN(name = 'results'))    
        return self.sm
    
if __name__ == '__main__':
    TESTERGUI().run()