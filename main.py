import random
import os

from kivy import Config
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

# Config.set('graphics', 'width', 400)
# Config.set('graphics', 'height', 500)
# Config.set('graphics', 'resizable', False)
Config.set('graphics', 'window_state', 'maximized')
# Config.set('graphics', 'fullscreen', 'fake')
# Config.set('graphics', 'position', 'custom')

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input_list = ObjectProperty(None)
    text_input_word = ObjectProperty(None)
    text_input_translate = ObjectProperty(None)
    button_show_list: ObjectProperty(None)
    button_show_translate: ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Открыть файл", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def generate(self):
        if self.step < len(self.lines):
            self.text_input_word.text = ""
            self.text_input_translate.text = ""
            self.text_input_word.text = self.lines[self.step].split("=")[0]
            try:
                self.text_input_translate.text = self.lines[self.step].split("=")[1]
            except IndexError:
                self.text_input_translate.text = ""
            self.step += 1
        else:
            self.text_input_word.text = "Достигнут конец списка. Он будет перемешан и запущен снова"
            self.shuffle_list()

    def shuffle_list(self):
        self.text_input_list.text = ""
        self.text_input_translate.text = ""
        random.shuffle(self.lines)
        for line in self.lines:
            self.text_input_list.text += line + "\n"
        self.step = 0


    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.lines = stream.read().split('\n')
        self.shuffle_list()
        self.dismiss_popup()

    def show_list(self):
        if self.button_show_list.state == 'normal':
            self.text_input_list.size_hint = [1, .0001]
        else:
            self.text_input_list.size_hint = [1, 1]

    def show_translate(self):
        if self.button_show_translate.state == 'normal':
            self.text_input_translate.size_hint = [1, .001]
        else:
            self.text_input_translate.size_hint = [1, 1]

class Editor(App):
    pass


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)


if __name__ == '__main__':
    Editor().run()