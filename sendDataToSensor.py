
import threading
import time
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
from commonData import broker, username

def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32

def average(values):
    return sum(values) / len(values)


def mqtt_publish_loop():
    client = TBDeviceMqttClient(broker, username=username)
    
    try:
        client.connect()
        
        for i in range(1000):
            telemetry = {
                "CO2": 400 + (i % 10),
                "PM2.5": 35 + (i % 5),
                "PM10": 50 + (i % 7),
                "temperature": celsius_to_fahrenheit(22.0 + (i % 2))
            }

            avg_air_quality = average([telemetry["CO2"], telemetry["PM2.5"], telemetry["PM10"]])
            print(f"Average air quality value: {avg_air_quality:.2f}")

            
            # Send telemetry and check delivery status
            result = client.send_telemetry(telemetry)
            success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
            print(f"Published telemetry (success={success}): {telemetry}")
            
            time.sleep(5)
            
    except Exception as e:
        print(f"MQTT Error: {str(e)}")
    finally:
        client.disconnect()
        print("MQTT disconnected")


# Threaded MQTT Runner
def start_mqtt_thread():
    mqtt_thread = threading.Thread(target=mqtt_publish_loop)
    mqtt_thread.daemon = True
    mqtt_thread.start()
    print("MQTT Thread started")