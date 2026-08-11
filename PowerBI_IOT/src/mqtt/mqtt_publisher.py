import json
import logging
import paho.mqtt.client as mqtt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MqttPublisher:
    def __init__(self, host="localhost", port=1883, enabled=False):
        self.host = host
        self.port = port
        self.enabled = enabled
        self.client = None
        self.connected = False
        
        if self.enabled:
            try:
                self.client = mqtt.Client()
                self.client.connect(self.host, self.port, 60)
                self.client.loop_start()
                self.connected = True
                logger.info(f"Connected to MQTT broker at {self.host}:{self.port}")
            except Exception as e:
                logger.warning(f"Failed to connect to MQTT broker: {e}. Running in offline CSV-only mode.")
                self.enabled = False
                self.connected = False

    def publish_reading(self, location, machine_id, data_dict):
        """
        Publishes sensor reading to MQTT if enabled.
        Topic format: factory/{location}/{machine_id}/sensors
        """
        if not self.enabled or not self.connected:
            return

        try:
            # Clean up topic string
            safe_location = location.lower().replace(" ", "_")
            topic = f"factory/{safe_location}/{machine_id}/sensors"
            
            payload = json.dumps(data_dict)
            self.client.publish(topic, payload)
        except Exception as e:
            logger.error(f"Failed to publish to MQTT: {e}")

    def disconnect(self):
        if self.client and self.connected:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False
