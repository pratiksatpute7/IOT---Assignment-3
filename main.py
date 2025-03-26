import paho.mqtt.client as mqtt
import time
import json
import random
import os
from datetime import datetime, timedelta
from dateutil import parser 

mqtt_host = "a3jgfbx3hg8d89-ats.iot.us-east-2.amazonaws.com" 
port = 8883
thing_name = "station_001"

ca_path = "AmazonRootCA1.pem"
cert_path = "certificate.pem.crt"
key_path = "private.pem.key"

topic = f"iot/{thing_name}/data"

def generate_sensor_data():
    return {
        "station_id": thing_name,
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": round(random.uniform(-50, 50), 2),
        "humidity": round(random.uniform(0, 100), 2),
        "co2": random.randint(300, 2000)
    }

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected to AWS IoT Core with result code " + str(rc))
    client.subscribe(topic)

def on_publish(client, userdata, mid):
    print("Data published successfully.")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload)
        print("\nLatest Sensor Data Received:")
        print(json.dumps(payload, indent=4))

    
        if os.path.exists("sensor_data.json"):
            with open("sensor_data.json", "r") as f:
                data = json.load(f)
        else:
            data = []

    
        data.append(payload)
        with open("sensor_data.json", "w") as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        print("Error processing message:", e)

def display_last_5_hours_from_file(sensor_type):
    try:
        with open("sensor_data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No sensor_data.json file found.")
        return

    now = datetime.utcnow()
    cutoff = now - timedelta(hours=5)

    print(f"\nSensor readings for '{sensor_type}' in the last 5 hours:")
    found = False
    for entry in data:
        try:
            timestamp = parser.parse(entry['timestamp'])
            if timestamp >= cutoff and sensor_type in entry:
                print(f"{entry['timestamp']} | {sensor_type}: {entry[sensor_type]}")
                found = True
        except Exception as e:
            continue

    if not found:
        print("No data found for this sensor in the last 5 hours.")

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.tls_set(ca_path, certfile=cert_path, keyfile=key_path)
client.on_publish = on_publish
client.on_message = on_message
client.on_connect = on_connect
client.connect(mqtt_host, port)
client.loop_start()

publish_count = 0 

try:
    while True:
        sensor_data = generate_sensor_data()
        payload = json.dumps(sensor_data)
        client.publish(topic, payload)

        publish_count += 1
        if publish_count % 10 == 0: 
            user_input = input("Enter sensor name (temperature or humidity or co2) to view last 5 hours data, or press Enter to skip: ").strip().lower()
            if user_input in ["temperature", "humidity", "co2"]:
                display_last_5_hours_from_file(user_input)

        time.sleep(2)

except KeyboardInterrupt:
    print("Stopping script.")
    client.loop_stop()
    client.disconnect()
