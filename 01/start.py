import sys
import kivy

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

import main
from main import LnJ


class Sandbox(App):


	def build(self, **kwargs):

		super(Sandbox,self).__init__(**kwargs)

		self.keyboard = Window.request_keyboard(self.keyboard_cleanup, self.root)
		self.keyboard.bind(on_key_down=self.keyboard_trigger)

		self.LNJ = LnJ()

		self.reload_container = BoxLayout()
		self.reload_container.add_widget(self.LNJ)

		return self.reload_container


	def keyboard_cleanup(self):
		self.keyboard.unbind(on_key_down=self.keyboard_trigger)
		self.keyboard = None


	def keyboard_trigger(self, keyboard, keycode, text, modifiers):
		print self, keyboard, keycode, text, modifiers

		if keycode[1] == 'r':

			try:
				self.reload_container.remove_widget(self.LNJ)

				reload(main)
				from main import LnJ

				self.LNJ = LnJ()
				self.reload_container.add_widget(self.LNJ)

			except:
				print "Failed to reload. Bummer. "
				print sys.exc_info()


		#if keycode[1] == '':




if __name__ == "__main__":
	app = Sandbox().run()
