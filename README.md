# 🌐 IoT Environmental Station using AWS IoT Core & MQTT

This repository contains the code and documentation for **Assignment 3** of the **CIS600 - Internet of Things** course (Spring 2025). The goal is to build a cloud-based IoT system using MQTT that collects environmental sensor data from virtual sensors and communicates with AWS IoT Core.

---

## 📌 Brief Explanation of the Steps

I developed a Python-based IoT system that simulates an environmental station using virtual sensors for temperature, humidity, and CO2. The system connects securely to AWS IoT Core using MQTT and publishes sensor data every 2 seconds. It also subscribes to the same topic to receive and display the latest data. All received messages are stored in a local JSON file, and users can view sensor readings from the last 5 hours by filtering data based on timestamp and sensor type.

---

## 📊 Sensor Data Range

| Sensor       | Range            |
|--------------|------------------|
| Temperature  | -50 to 50 °C     |
| Humidity     | 0 to 100 %       |
| CO2          | 300 to 2000 ppm  |

---
## Install Dependencies
pip install paho-mqtt python-dateutil

## 🧰 Technologies Used

- Python 3
- AWS IoT Core
- Paho MQTT Client
- TLS Certificates (CA, Device Cert, Private Key)
- JSON for data storage and messaging
- `python-dateutil` for timestamp parsing

---

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/iot-environmental-station.git
cd iot-environmental-station
run main.py
