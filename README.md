# 🌤️ Python Weather App (PyQt5 + OpenWeatherMap)

A simple desktop application built with **Python** and **PyQt5** that fetches and displays real-time weather data using the **OpenWeatherMap API**.

---

## 🧰 Technologies Used

- **Python 3**
- **PyQt5** – for the GUI interface
- **requests** – to make HTTP requests to the weather API
- **python-dotenv** – to manage API keys securely via `.env` file
- **OpenWeatherMap API** – to fetch current weather data

---

## ✨ Features

- ✅ Enter any city name to get real-time weather updates
- 🌡️ Displays temperature, weather condition, humidity
- ⚠️ Error handling for invalid city input or API issues
- 🔐 API key hidden using `.env` file

---

## 📸 Screenshot

<img width="264" alt="{C6EFA3B6-568F-4227-9E12-9BCDF5ABEE59}" src="https://github.com/user-attachments/assets/fe89bcf0-6f80-44a6-8edb-20da6633095a" />

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone  https://github.com/RahulTR-dev/Python-Weather-App.git
cd Python_Weather_App
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Set Your OpenWeatherMap API Key
```
Create a .env file in the project root:
in the file add
WEATHER_API_KEY=your_api_key_here
```
### 4. Run the App
```bash
python weather.py
```

