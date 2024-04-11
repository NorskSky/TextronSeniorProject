import kivy

from kivy.app import App
from kivy.uix.widget import Widget
class MAINWINDOW(Widget):
    pass

class TESTERGUI(App):
    def build(self):
        return MAINWINDOW()
    
if __name__ == '__main__':
    TESTERGUI().run()