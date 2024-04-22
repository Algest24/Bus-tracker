from kivymd.app import MDApp
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty
from kivy.garden.mapview import MapView
from kivymd.theming import ThemeManager
import sqlite3
from kivymd.uix.list import MDList, OneLineListItem
class FirstWindow(Screen):
    pass


class SecondWindow(Screen):
	def login_button_pressed(self):
		db = sqlite3.connect('bus.db')
		c = db.cursor()
		c.execute('''
		CREATE TABLE IF NOT EXISTS Drivers (
		id INTEGER PRIMARY KEY,
		login TEXT,
		password TEXT
		)
		''')
		# c.execute("INSERT INTO Drivers VALUES (1, 'Login', 'Pass')")
		# c.execute("INSERT INTO Drivers VALUES (2, 'Admin', 'Admin')")

		c.execute("SELECT rowid, * FROM Drivers")
		items = c.fetchall()
					
		login = self.ids.username_field.text
		password = self.ids.password_field.text

		status = False

		for item in items:

			print(item[3])
			if login == item[2] and item[3] == password:
				status = True

		if status:
			print("Успешный вход!")
			app = App.get_running_app()
			app.set_dark_theme()  # Устанавливаем темную тему
			self.manager.current = "map"
			# Применить анимацию перехода
			self.manager.transition.direction = "left"                        
		else:
			print("Неверный логин или пароль")
			self.manager.current = "first"
    
			# Применить анимацию перехода
			self.manager.transition.direction = "right"                           

		db.commit()
		db.close()

class MapWindow(Screen):
    menu = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MapWindow, self).__init__(**kwargs)

        # Create menu items
        menu_items = [
			{
				"text": "О приложении",
				"on_release": lambda: self.show_about(),
			},
			{
				"text": "Выход",
				"on_release": lambda: self.switch_to_first_window(),
			}
        ]

        # Create the dropdown menu
        self.menu = MDDropdownMenu(items=menu_items, width_mult=4)

    def menu_callback(self, text_item):
        self.menu.dismiss()
        Snackbar(text=text_item).open()
    def show_about(self):
        self.manager.current = 'AboutAPP'

    def switch_to_first_window(self):
        self.manager.current = 'first'

    # Метод для открытия меню из KV файла
    def open_menu(self, button):
        self.menu.caller = button
        self.menu.open()

class CallboardWindow(Screen):
	pass

class WindowManager(ScreenManager):
    pass

class Stops(Screen):
	pass
	#def build(self):
	#	screen = Screen()

#		list_view = MDList()
#		item1 = OneLineListItem(text='Тест 1')
#		item2 = OneLineListItem(text='Тест 2')

#		list_view.add_widget(item1)
#		list_view.add_widget(item2)
		
#		screen.add_widget(list_view)
#		return screen
class AboutAPP(Screen):
	pass

class AwesomeApp(MDApp):
	theme_cls = ThemeManager()      
    
	def build(self):
		kv = Builder.load_file('new_window.kv')
		self.theme_cls.primary_palette = 'Green'
		return kv
      
	def set_dark_theme(self):
		self.theme_cls.theme_style = "Dark"

	def set_light_theme(self):
		self.theme_cls.theme_style = "Light"

if __name__ == '__main__':
    AwesomeApp().run()