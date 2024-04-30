import kivy
import threading, time, random, os


#Loads the config file
from kivy.config import Config
Config.read("screen_config.cfg")

#GUI specific Imports
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


#Analysis specific imports
from pydub import AudioSegment
from pydub.playback import play
#import ADS1256
#import RPi.GPIO as GPIO
#import errorHandler
import pandas as pd
#from time import time, sleep, perf_counter

class RESULTSSTORAGE():    
    Data = ["Default data"] * 8
    Pass = ["Not Selected"] * 8   
     
class ANALYSIS():    
    #Select input of GMA to be tested
    GMAinputData = pd.DataFrame()
    #Load baseline Min and Max values, correlating to the GMA input
    GMAoutputs_Thresholds = dict()
    adc_channels = dict()
    GMAOutMax = dict() 
    GMAOutMin = dict()
    
    Results = RESULTSSTORAGE()
    
    def digitGrab(self, string):
        numList = list()
        for i in string:
            if i.isdigit():
                numList.append(i)
        return "".join(numList)
    
    def GMAInputSelection(self, gmaInputSelected):        
        
            
        baselineData = pd.read_csv(f'baselineCapture/baselineCSV/{gmaInputSelected}.csv')
        return baselineData
        #print(baselineData.to_string(index=False))

    def GMAOutputSelection(self, baselineData, gmaOuts):
        gmaOutSelected = list()
        for i in gmaOuts:
            gmaOutSelected = self.digitGrab(i)
        gmaOutputDict = dict()
        for output in gmaOutSelected:
            gmaOutputDict[output] = (float(baselineData.at[output-1,"Min"]),float(baselineData.at[output-1,"Max"]))
        return gmaOutputDict

    def ADC_Channels(self, gmaOutputDict):
        ADC_channels = dict()
        for output in gmaOutputDict.keys():
            ADC_channels[int(input('GMA Output {} plugged into which FTM Channel? '.format(output)))] = output
        return ADC_channels
    
    
    #define linear sweep function
    def LinearSweep(self):
        with errorHandler.noalsaerr():
            linSweepMp3 = AudioSegment.from_mp3("sinesweep/16Hz-20kHz-Lin-CA-10sec.mp3")
            print('Starting Linear Sine Sweep Audio on Outputs 1 & 2')
            play(linSweepMp3)
            sleep(1)
            print('Linear Sweep Complete')

    #define exponential sweep function    
    def ExponentialSweep(self):
        expSweepMp3 = AudioSegment.from_mp3("sinesweep/16Hz-20kHz-Exp-CA-10sec.mp3")
        print('Starting Exponential Sine Sweep Audio on Outputs 1 & 2')
        play(expSweepMp3)
        time.sleep(1)
        print('Exponential Sweep Complete')
        
    #define ADC Min/Max Capture Function
    def ADCRead(self, duration):
        print('starting ADC reads')
        t_end = time() + duration
        i = 0
        try:
            ADC = ADS1256.ADS1256()
            ADC.ADS1256_init()
            time.sleep(0.1) 

            while time() < t_end:
                ADC_Value = ADC.ADS1256_GetAll()
                for i in self.adc_channels.keys():
                    if (ADC_Value[i]*5.0/0x7fffff) > self.GMAOutMax[i]:
                        self.GMAOutMax[i] = (ADC_Value[i]*5.0/0x7fffff)
                    if (ADC_Value[i]*5.0/0x7fffff) < self.GMAOutMin[i]:
                        self.GMAOutMin[i] = (ADC_Value[i]*5.0/0x7fffff)
                    i+=1
                
        except :
            GPIO.cleanup()
            print ("\r\nProgram end     ")
            #exit()
        print('Done with ADC Reads')

    
    def runAnalysis(self, gmaInput, testType, gmaOutputs):
        #Select input of GMA to be tested
        self.GMAinputData = self.GMAInputSelection(gmaInput)
        #Load baseline Min and Max values, correlating to the GMA input
        self.GMAoutputs_Thresholds = self.GMAOutputSelection(self.GMAinputData, gmaOutputs)
        self.adc_channels = self.ADC_Channels(self.GMAoutputs_Thresholds)        

    
        
        for ch in self.adc_channels.keys():
            self.GMAOutMax[ch] = 0
            self.GMAOutMin[ch] = 5
            
        # create two new threads
        if testType == 'L':
            linSweepMp3 = AudioSegment.from_mp3("sinesweep/16Hz-20kHz-Lin-CA-10sec.mp3")
            duration = int(linSweepMp3.duration_seconds)
            t1 = threading.Thread(target=self.LinearSweep)
        if testType == 'E':
            expSweepMp3 = AudioSegment.from_mp3("sinesweep/16Hz-20kHz-Exp-CA-10sec.mp3")
            duration = int(expSweepMp3.duration_seconds)
            t1 = threading.Thread(target=self.ExponentialSweep)
        t2 = threading.Thread(target=self.ADCRead, args=(duration))

        # start the threads
        t1.start()
        t2.start()

        # wait for the threads to complete
        t1.join()
        t2.join()
        x = 0
        
        for i in self.adc_channels.keys():
            measured_min = self.GMAOutMin[i]
            measured_max = self.GMAOutMax[i]
            GMA_acceptable_range = self.GMAoutputs_Thresholds[self.adc_channels[i]]
            if measured_min < GMA_acceptable_range[0]:
                print('GMA Output {} Failed: Measured {} below {} threshold'.format(self.adc_channels[i],measured_min,GMA_acceptable_range))
                self.Results.Data[x] = "-" + measured_min
                self.Results.Pass[x] = "Fail"
            elif measured_max > GMA_acceptable_range[1]:
                print('GMA Output {} Failed: Measured {} above {} threshold'.format(self.adc_channels[i],measured_max,GMA_acceptable_range))
                self.Results.Data[x] = "-" + measured_max
                self.Results.Pass[x] = "Fail"
            else:
                print('GMA Output {} Passed!'.format(self.adc_channels[i]))
                self.Results.Data[x] = "Within Threshold"
                self.Results.Pass[x] = "Pass" 
            x += 1
        return
    #print(f'ADC Read Complete')




#======================================================================================================================
#=====================================GUI CODE=========================================================================
#Loads the kv files, that dictate look, feel, and behavior of the GUI 
Builder.load_file("kv_files/menu.kv")
Builder.load_file("kv_files/settings.kv")
Builder.load_file("kv_files/loading.kv")
Builder.load_file("kv_files/results.kv")
class MENUSCREEN(Screen):
    
    def shutdown(self):            
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
    #results = RESULTSSTORAGE()
    analysis = ANALYSIS()
      
    
    
    GMAInputs = ('GMA Input 1', 'GMA Input 2', 'GMA Input 3', 'GMA Input 4', 'GMA Input 5', 'GMA Input 6', 
                'GMA Input 7', 'GMA Input 8', 'GMA Input 9', 'GMA Input 10', 'GMA Input 11', 'GMA Input 12', 
                'GMA Input 13', 'GMA Input 14', 'GMA Input 15', 'GMA Input 16', 'GMA Input 17', 'GMA Input 18', 
                'GMA Input 19', 'GMA Input 20', 'GMA Input 21', 'GMA Input 22', 'GMA Input 23', 'GMA Input 24', 
                'GMA Input 25', 'GMA Input 26', 'GMA Input 27', 'GMA Input 28', 'GMA Input 29', 'GMA Input 30', 
                'GMA Input 31', 'GMA Input 32', 'GMA Input 33', 'GMA Input 34', 'GMA Input 35', 'GMA Input 36', 
                'GMA Input 37', 'GMA Input 38', 'GMA Input 39', 'GMA Input 40', 'GMA Input 41', 'GMA Input 42', 
                'GMA Input 43', 'GMA Input 44', 'GMA Input 45', 'GMA Input 46', 'GMA Input 47', 'GMA Input 48',
                'GMA Input 49', 'GMA Input 50', 'GMA Input 51', 'GMA Input 52' ,'GMA Input 53', 'GMA Input 54',
                'GMA Input 54', 'GMA Input 56', 'GMA Input 57', 'GMA Input 58' ,'GMA Input 59', 'GMA Input 60',  
                'GMA Input 61', 'GMA Input 62', 'GMA Input 63', 'GMA Input 64')
 
    GMAOutputs = ('GMA Output 1', 'GMA Output 2', 'GMA Output 3', 'GMA Output 4', 'GMA Output 5', 'GMA Output 6', 
                  'GMA Output 7', 'GMA Output 8', 'GMA Output 9', 'GMA Output 10', 'GMA Output 11', 'GMA Output 12',
                  'GMA Output 13', 'GMA Output 14', 'GMA Output 15', 'GMA Output 16', 'GMA Output 17', 'GMA Output 18',
                  'GMA Output 19', 'GMA Output 20', 'GMA Output 21', 'GMA Output 22', 'GMA Output 23', 'GMA Output 24',
                  'GMA Output 25', 'GMA Output 26', 'GMA Output 27', 'GMA Output 28', 'GMA Output 29', 'GMA Output 30',
                  'GMA Output 31')
    
    Thresholds = [""] * 8
    OutputsSelected = ["Not Selected"] * 8
    GMAInputSelected = ""
   
    def digitGrab(self, string):
        numList = list()
        for i in string:
            if i.isdigit():
                numList.append(i)
        return "".join(numList)
   
    def loadResults(self):
        
        thistime = time.time()         
        while thistime + 5 > time.time(): # 5 seconds
            time.sleep(1)       
        self.sm.get_screen('results').updateResults(self.analysis.Results.Pass)
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
        self.showLoading()       
        
        mythread = threading.Thread(target=self.analysis.runAnalysis, args=(self.GMAInputSelected, "L", self.OutputsSelected))
        mythread2 = threading.Thread(target=self.loadResults)
        mythread.start()  
        mythread2.start()
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
        
        #grabs the GMA input
        self.GMAInputSelected = self.digitGrab(self.sm.current_screen.ids.dropdown_9.text)
        print(self.GMAInputSelected)
        #Updates the result screen with the correct data 
        self.sm.current = 'results'
            
        self.sm.get_screen('results').updateOutputs(self.OutputsSelected)
        self.sm.current = 'menu'
   
           
    def build(self):          
        self.sm.add_widget(MENUSCREEN(name = 'menu'))   
        self.sm.add_widget(SETTINGSSCREEN(name = 'settings'))     
        self.sm.add_widget(RESULTSSCREEN(name = 'results'))    
        return self.sm
#running code   
if __name__ == '__main__':
    TESTERGUI().run()