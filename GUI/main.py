import kivy

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.land.builder import Builder
class MAINWINDOW(Widget):
    pass

Builder.load_file("tester.kv")

class TESTERGUI(App):
    def build(self):
        return MAINWINDOW()
    
if __name__ == '__main__':
    TESTERGUI().run()