import network # network kütüphanesi dahil edilir.
import time # network kütüphanesi dahil edilir.
from dht import DHT11 # dht kütüphanesinden DHT11 kütüphanesi dahil edilir.
from umqtt.simple import MQTTClient # umqtt.simple kütüphanesinden MQTTClient kütüphanesi dahil edilir.
from machine import Pin # machine kütüphanesinden dahil Pin kütüphanesi edilir.

# Wi-Fi'ya bağlanılır.
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("********", "********") # Sırasıyla kullandığınız Wi-Fi'ın adını ve şifresini girin.

dht11_pin = DHT11(Pin(16, Pin.OUT, Pin.PULL_DOWN)) # Dht11 sensörü GP16'ya bağlanır.

# Broker ile ilgili bilgiler.
mqtt_server = 'broker.hivemq.com'
client_id = 'bigles'
topic_pub_temp = b'Dht11_Project/Temp'
topic_pub_humid = b'Dht11_Project/Humidity'

# MQTT servera bağlanmak için fonksiyon
def mqtt_connect():
   client = MQTTClient(client_id, mqtt_server, keepalive=3600)
   client.connect()
   print('Connected to %s MQTT Broker'%(mqtt_server))
   return client

# MQTT Broker'a bağlantı olmazsa tekrardan bağlanmak için fonksiyon
def reconnect():
   print('Failed to connect to the MQTT Broker. Reconnecting...')
   time.sleep(5)
   machine.reset()
   
try:
   client = mqtt_connect() # MQTT'ye bağlanılır.
except OSError as e:
   reconnect()
   
while True:
    
    dht11_pin.measure() 
    temp = dht11_pin.temperature() # Dht11 sensörünün okuduğu sıcaklık değeri.
    hum = dht11_pin.humidity() # Dht11 sensörünün okuduğu nem değeri.
    
    # Okunan değererler broker'a publish edilir.
    client.publish(topic_pub_temp, str(temp))
    client.publish(topic_pub_humid, str(hum))
    time.sleep(2) # 2 saniye gecikme.


