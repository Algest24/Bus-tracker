from kivymd.app import MDApp
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty
from kivy.garden.mapview import MapView, MapMarkerPopup
from kivymd.theming import ThemeManager
import sqlite3
import requests

from kivymd.uix.list import MDList, OneLineListItem

class FirstWindow(Screen):
	def onmap(self):
		app = App.get_running_app()
		app.set_dark_theme()



class SecondWindow(Screen):
	# def login_button_pressed(self):
	# 	db = sqlite3.connect('bus.db')
	# 	c = db.cursor()
	# 	c.execute('''
	# 	CREATE TABLE IF NOT EXISTS Drivers (
	# 	id INTEGER PRIMARY KEY,
	# 	login TEXT,
	# 	password TEXT
	# 	)
	# 	''')
	# 	# c.execute("INSERT INTO Drivers VALUES (1, 'Login', 'Pass')")
	# 	# c.execute("INSERT INTO Drivers VALUES (2, 'Admin', 'Admin')")

	# 	c.execute("SELECT rowid, * FROM Drivers")
	# 	items = c.fetchall()
					
	# 	login = self.ids.username_field.text
	# 	password = self.ids.password_field.text

	# 	status = False

	# 	for item in items:

	# 		print(item[3])
	# 		if login == item[2] and item[3] == password:
	# 			status = True

	# 	if status:
	# 		print("Успешный вход!")
	# 		app = App.get_running_app()
	# 		app.set_dark_theme()  # Устанавливаем темную тему
	# 		self.manager.current = "map"
	# 		# Применить анимацию перехода
	# 		self.manager.transition.direction = "left"                        
	# 	else:
	# 		print("Неверный логин или пароль")
	# 		self.manager.current = "first"
    
	# 		# Применить анимацию перехода
	# 		self.manager.transition.direction = "right"                           

	# 	db.commit()
	# 	db.close()
	
	def login_button_pressed(self):
		url = 'http://127.0.0.1:5000/login'
		login = self.ids.username_field.text
		password = self.ids.password_field.text
		data = {'login': login, 'password': password}
		response = requests.post(url, json=data)

		if response.status_code == 200:
			app = App.get_running_app()
			app.set_dark_theme()  # Устанавливаем темную тему
			self.manager.current = "map"
			# Применить анимацию перехода
			self.manager.transition.direction = "left"
			# print("UID:", response.json()['uid'])
		else:
			# print("Ошибка:", response.json()['error'])
			self.manager.current = "first"
			self.manager.transition.direction = "right"

class MapWindow(Screen):
	
	menu = ObjectProperty(None)

	def __init__(self, **kwargs):
		global stops_data
		
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




	# def menu_callback(self, text_item):  НЕ РАБОТАЕТ НУЖНО ПРИВЯЗАТЬ КАК-ТО КАЛЛБЕК
	# 	self.menu.dismiss()
	# 	Snackbar(text=text_item).open()
	def show_about(self):
			app = App.get_running_app()
			app.set_light_theme()
			self.manager.current = 'AboutAPP'
			self.menu.dismiss()

	def switch_to_first_window(self):
		app = App.get_running_app()
		app.set_light_theme()
		self.manager.current = 'first'
		self.menu.dismiss()

	# Метод для открытия меню из KV файла
	def open_menu(self, button):
		self.menu.caller = button
		self.menu.open()
		
	def white(self):
		app = App.get_running_app()
		app.set_light_theme()
		
	def add_marker(self):
		global stops_data

		for stop in stops_data:
			name = stop["name"]
				
			coordinates = stop["coordinates"]
			print(name, coordinates)
			lat, lon = coordinates[0], coordinates[1]
			# Добавляем метку на карту
			marker = MapMarkerPopup(lat=lat, lon=lon, source="marker32.png")
			self.ids.map_view.add_marker(marker)





class CallboardWindow(Screen):
	pass

class WindowManager(ScreenManager):
    pass

class Stops(Screen):
	def onmap(self):
		app = App.get_running_app()
		app.set_dark_theme()
		
	#def build(self):
	#	screen = Screen()

#		list_view = MDList()
#		item1 = OneLineListItem(text='Тест 1')
#		item2 = OneLineListItem(text='Тест 2')

#		list_view.add_widget(item1)
#		list_view.add_widget(item2)
		
#		screen.add_widget(list_view)
#		return screen

	def create_stop_list(self):
			stop_list = self.ids.stop_list

			for item in stops_data:
				name = item["name"]
				coordinates = item["coordinates"]
				item_widget = OneLineListItem(text=name)
				item_widget.bind(on_release=lambda widget, name=name, coordinates=coordinates : self.on_stop_selected(widget, name, coordinates))
				stop_list.add_widget(item_widget)

	def on_stop_selected(self, widget, name, coordinates):
			print(name)
			print(coordinates)
			app = App.get_running_app()
			app.set_dark_theme()

			# Получаем доступ к экземпляру MapView
			map_view = self.manager.get_screen("map").ids.map_view

			
			# Перемещаем карту к указанным координатам
			map_view.center_on(*coordinates)
			# self.manager.get_screen("map").ids.map_view.zoom = 30 крашит и не видно меток
			self.manager.transition.direction = "down"
			self.manager.current = "map"
			# Применить анимацию перехода
			
			
		
class AboutAPP(Screen):
	def onmap(self):
		app = App.get_running_app()
		app.set_dark_theme()
		

class AwesomeApp(MDApp):
	theme_cls = ThemeManager()      
    
	
    
   

	def build(self):
		global stops_data
		response = requests.get("http://127.0.0.1:5000/stops")
		 
		if response.status_code == 200:
			stops_data = response.json()["stops"]
			
		else:
			print("Ошибка при получении данных о метках")

		kv = Builder.load_file('new_window.kv')
		self.theme_cls.primary_palette = 'Green'
		return kv
      
	def set_dark_theme(self):
		self.theme_cls.theme_style = "Dark"

	def set_light_theme(self):
		self.theme_cls.theme_style = "Light"
		

if __name__ == '__main__':
    AwesomeApp().run()