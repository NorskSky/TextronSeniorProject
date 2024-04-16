import kivy

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout


Config.set('graphics', 'resizable', '0') 
# fix the width of the window 
Config.set('graphics', 'width', '800') 
# fix the height of the window 
Config.set('graphics', 'height', '480')

class MAINWINDOW(GridLayout):
    def __init__(self, **kwargs):
        super(MAINWINDOW, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 2    
        self.padding = [10, 10]   
        self.spacing = [10, 10]



Builder.load_file("tester.kv")

class TESTERGUI(App):
    def build(self):        
        return MAINWINDOW()
    
if __name__ == '__main__':
    TESTERGUI().run()