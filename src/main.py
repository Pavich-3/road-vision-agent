from paho.mqtt import client as mqtt_client
import time
from schema.parking_schema import ParkingSchema
from schema.aggregated_data_schema import AggregatedDataSchema
from file_datasource import FileDatasource
import config


def connect_mqtt(broker, port):
    """Create MQTT client"""
    print(f"Connecting to {broker}:{port}...")

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker ({broker}:{port})")
        else:
            print(f"Failed to connect {broker}:{port}, return code {rc}")
            exit(rc)  # Stop execution

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()

    return client


def publish(client, topic, datasource, delay):
    datasource.startReading()
    print(f"Publishing to topic `{topic}` every {delay} seconds")

    while True:
        time.sleep(delay)

        data = datasource.read()
        msg = AggregatedDataSchema().dumps(data)
        client.publish(topic, msg)
        print(f"Sent to `{topic}`: {msg}")

        parking_data = datasource.read_parking()
        parking_msg = ParkingSchema().dumps(parking_data)
        client.publish("parking_data_topic", parking_msg)
        print(f"Sent to `parking_data_topic`: {parking_msg}")


def run():
    client = connect_mqtt(config.MQTT_BROKER_HOST, config.MQTT_BROKER_PORT)
    datasource = FileDatasource("data/accelerometer.csv", "data/gps.csv", "data/parking.csv")
    try:
        publish(client, config.MQTT_TOPIC, datasource, config.DELAY)
    except KeyboardInterrupt:
        print("Interrupted by user, stopping...")
    finally:
        datasource.stopReading()
        client.loop_stop()
        client.disconnect()
        print("Stopped.")


if __name__ == '__main__':
    run()
