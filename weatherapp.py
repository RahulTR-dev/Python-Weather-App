from dotenv import load_dotenv
import os
load_dotenv()
import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

class WeatherApp(QWidget):

    def __init__(self):
        super().__init__()

        # Widgets
        self.city_label = QLabel("Enter City name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)

        # Setup UI
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        

        # Vertical Layout
        vbox = QVBoxLayout()

        # Add widgets to layout
        self.setFixedSize(400, 600)  # Optimal size for weather app
        vbox.setContentsMargins(30, 30, 30, 30)  # Add padding around the edges
        vbox.setSpacing(15)  # Consistent spacing between widgets
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        

        # Add this to your initUI method after creating widgets
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(300)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_animation.start()

        self.setLayout(vbox)

        # Center-align all labels and input
        for widget in [self.city_label, self.city_input, self.temperature_label, self.emoji_label, self.description_label]:
            widget.setAlignment(Qt.AlignCenter)

        # Set object names for styling
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # Set stylesheet
        self.setStyleSheet("""
                QWidget {
                    background-color: #f5f7fa;
                }
                
                QLabel, QPushButton {
                    font-family: 'Segoe UI', Arial, sans-serif;
                }

                QLabel#city_label {
                    font-size: 24px;
                    color: #4a4a4a;
                    margin-bottom: 5px;
                }

                QLineEdit#city_input {
                    font-size: 20px;
                    padding: 10px;
                    border: 2px solid #d1d5db;
                    border-radius: 8px;
                    background-color: white;
                    color: #374151;
                    margin-bottom: 15px;
                }
                
                QLineEdit#city_input:focus {
                    border-color: #3b82f6;
                    outline: none;
                }

                QPushButton#get_weather_button {
                    font-size: 18px;
                    font-weight: 600;
                    color: white;
                    background-color: #3b82f6;
                    border: none;
                    border-radius: 8px;
                    padding: 12px;
                    margin: 10px 0;
                }
                
                QPushButton#get_weather_button:hover {
                    background-color: #2563eb;
                }
                
                QPushButton#get_weather_button:pressed {
                    background-color: #1d4ed8;
                }
                
                QPushButton#get_weather_button:disabled {
                    background-color: #9ca3af;
                }
                                
                QLabel#temperature_label {
                    font-size: 72px;
                    font-weight: 300;
                    color: #1f2937;
                    margin: 10px 0;
                }
                
                QLabel#emoji_label {
                    font-size: 100px;
                    font-family: 'Segoe UI Emoji', 'Apple Color Emoji';
                    margin: 5px 0;
                }
                
                QLabel#description_label {
                    font-size: 24px;
                    color: #4b5563;
                    text-transform: capitalize;
                    margin-top: 5px;
                }
                
                /* Error message styling */
                QLabel[accessibleName="error"] {
                    font-size: 18px;
                    color: #ef4444;
                    padding: 10px;
                    background-color: #fee2e2;
                    border-radius: 6px;
                }
            """)

        # Connect button click
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        self.get_weather_button.setEnabled(False)
        self.temperature_label.setStyleSheet("font-size: 30px; color: orange; font-weight: bold;")
        self.temperature_label.setText("Loading...")
        self.emoji_label.clear()
        self.description_label.clear()

        api_key = os.getenv('WEATHER_API_KEY')

        if api_key is None:
            raise ValueError("API key not found. Set the WEATHER_API_KEY environment variable.")
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError:
            match response.status_code:
                case 400:
                    self.display_error("Bad request\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized\nPlease check your authentication credentials.")
                case 403:
                    self.display_error("Forbidden\nYou do not have permission to access this resource.")
                case 404:
                    self.display_error("Not Found\nThe requested resource could not be found.")
                case 500:
                    self.display_error("Internal Server Error\nSomething went wrong on the server.")
                case 502:
                    self.display_error("Bad Gateway\nReceived an invalid response from the upstream server.")
                case 503:
                    self.display_error("Service Unavailable\nThe server is currently unable to handle the request.")
                case 504:
                    self.display_error("Gateway Timeout\nThe server took too long to respond.")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")
        finally:
            self.get_weather_button.setEnabled(True)

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px; color: red; font-weight: bold;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px; color: black;")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"].capitalize()

        self.temperature_label.setText(f"{temperature_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    def get_weather_emoji(self, weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "⛅"
        else:
            return "❓"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
