import requests
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from weather_utils import get_weather_data, get_weather_emoji

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.api_key = "025890427621353419ae99b0dde95498"
        self.setGeometry(600, 250, 350, 570)
        self.setup_widgets()
        self.initUI()

    def setup_widgets(self):
        self.city_label = QLabel("Enter city name:")
        self.city_input = QLineEdit()
        self.get_weather_button = QPushButton("Get Weather")
        self.city_info_label = QLabel()
        self.temp_label = QLabel()
        self.feels_like = QLabel()
        self.emoji_label = QLabel()
        self.description_label = QLabel()

        for widget, name in zip(
            [self.city_label, self.city_input, self.get_weather_button, self.city_info_label, self.temp_label, self.feels_like, self.emoji_label, self.description_label],
            ["city_label", "city_input", "get_weather_button", "city_info_label", "temp_label", "feels_like", "emoji_label", "description_label"]):
            widget.setObjectName(name)

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setWindowIcon(QIcon("icon.jpg"))

        vbox = QVBoxLayout()
        widgets = [
            self.city_label, self.city_input, self.get_weather_button,
            self.city_info_label, self.temp_label, self.feels_like,
            self.emoji_label, self.description_label
        ]

        for widget in widgets:
            vbox.addWidget(widget)
            if widget != self.get_weather_button:
                widget.setAlignment(Qt.AlignCenter)

        self.setLayout(vbox)
        self.apply_styles()
        self.get_weather_button.clicked.connect(self.get_weather)

    def apply_styles(self):
        self.setStyleSheet("""
            QLabel, QPushButton { font-family: calibri; }
            QLabel#city_label { font-size: 40px; font-style: italic; }
            QLineEdit#city_input { font-size: 30px; }
            QPushButton#get_weather_button { font-size: 30px; font-weight: bold; }
            QLabel#city_info_label { font-size: 15px; font-weight: bold; }
            QLabel#temp_label { font-size: 75px; }
            QLabel#feels_like { font-size: 30px; font-weight: bold; }
            QLabel#emoji_label { font-size: 100px; font-family: Segoe UI emoji; }
            QLabel#description_label { font-size: 50px; }
        """)

    def get_weather(self):
        city = self.city_input.text()
        
        try:
            geo_data, weather_data = get_weather_data(city, self.api_key)
            if weather_data.get("cod") == 200:
                self.display_weather(geo_data, weather_data)
            
        except requests.exceptions.HTTPError as http_error:
            # Handle HTTP errors
            if http_error.response.status_code == 400:
                self.display_error("Bad request\nPlease check your input.")
            elif http_error.response.status_code == 401:
                self.display_error("Unauthorized\nInvalid API key.")
            elif http_error.response.status_code == 403:
                self.display_error("Forbidden\nAccess denied.")
            elif http_error.response.status_code == 404:
                self.display_error("Not found\nCity not found.")
            elif http_error.response.status_code == 500:
                self.display_error("Internal server error\nPlease try again later.")
            elif http_error.response.status_code == 502:
                self.display_error("Bad Gateway\nInvalid response from the server.")
            elif http_error.response.status_code == 503:
                self.display_error("Service unavailable\nServer is down.")
            elif http_error.response.status_code == 504:
                self.display_error("Gateway timeout\nNo response from the server.")
            else:
                self.display_error(f"HTTP error occurred\n{http_error}")
        
        except requests.exceptions.ConnectionError:
            self.display_error("Connection error:\nCheck your internet connection.")
        
        except requests.exceptions.Timeout:
            self.display_error("Timeout error:\nThe request timed out.")
        
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects:\nCheck the URL.")
        
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error:\n{req_error}")

     
    
    def display_error(self, message):
        self.city_info_label.clear()
        self.temp_label.setStyleSheet("font-size: 30px;")
        self.temp_label.setText(message)
        self.feels_like.clear()
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, geo_data, weather_data):
        city_name = geo_data.get("name", "")
        state_name = geo_data.get("state", "N/A")
        country_name = geo_data.get("country", "")
        
        self.city_info_label.setText(f"{city_name}, {state_name}, {country_name}")
        temp_c = weather_data["main"]["temp"] - 273.15
        feels_like_c = weather_data["main"]["feels_like"] - 273.15
        weather_description = weather_data["weather"][0]["description"]
        weather_id = weather_data["weather"][0]["id"]

        self.temp_label.setStyleSheet("font-size: 75px;")
        self.temp_label.setText(f"{temp_c:.0f}°C")
        self.feels_like.setText(f"Feels like: {feels_like_c:.0f}°C")
        self.description_label.setText(weather_description.capitalize())
        self.emoji_label.setText(get_weather_emoji(weather_id))