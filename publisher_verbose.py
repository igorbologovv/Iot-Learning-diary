import time, random
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"   # публичный брокер HiveMQ
PORT   = 1883                  # без TLS: видно в Wireshark
TOPIC  = "oamkiotcourse/igogo/test"  # сделай уникальным: меняй "igogo"

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"[on_connect] rc={reason_code}")

def on_publish(client, userdata, mid, properties=None):
    print(f"[on_publish] mid={mid}")

def on_disconnect(client, userdata, reason_code, properties=None):
    print(f"[on_disconnect] rc={reason_code}")

# Клиент с уникальным ID
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                     client_id=f"ldiary-{int(time.time())}")

client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect

print(f"Connecting to {BROKER}:{PORT} ...")
client.connect(BROKER, PORT, keepalive=60)

client.loop_start()
for i in range(5):
    payload = f"ldiary-sample-{i}-{random.randint(1000,9999)}"
    print(f"Publishing to {TOPIC}: {payload}")
    info = client.publish(TOPIC, payload=payload, qos=0, retain=False)
    info.wait_for_publish()
    time.sleep(0.5)
client.loop_stop()

print("Disconnecting ...")
client.disconnect()
print("Done.")
