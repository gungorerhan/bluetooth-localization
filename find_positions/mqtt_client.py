import paho.mqtt.client as mqtt
from bluepy.btle import Scanner, DefaultDelegate
import numpy as np


host = "hairdresser.cloudmqtt.com"
port = 18407
username = "smrntlue"
password = "T8Oenavy62jp"

topic = "IPS/erhan-e570/pd"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("topic: " + msg.topic+", msg: "+str(msg.payload.decode('utf-8')))


class ScanDelegate(DefaultDelegate):
	def __init__(self):
		DefaultDelegate.__init__(self)

	def handleDiscovery(self, dev, isNewDev, isNewData):
		if dev.addrType == "public" and dev.addr in mac_id.keys():
			if mac_id[dev.addr] not in my_devs.keys():
				my_devs[mac_id[dev.addr]] = [dev.rssi]
			else:
				my_devs[mac_id[dev.addr]].append(dev.rssi)

			if isNewDev:
				print ("Discovered device (%s) with RSSI (%d)" % (dev.addr, dev.rssi))
			elif isNewData:
				print ("Received new data from (%s) with RSSI (%d)" % (dev.addr, dev.rssi))


# main func 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username, password)
client.connect(host, port, 60)

# scan ble devices 
mac_id = {
	"00:00:02:00:08:f4": 2292,
	"00:00:02:00:0c:3b": 3131
}

my_devs = {}


while True:
	my_devs = {}

	# collect rssi values
	scanner = Scanner().withDelegate(ScanDelegate())
	devices = scanner.scan(20.0, passive=True)

	# publish rssi values
	payload = ""
	for key in my_devs.keys():
		key_rssi = "{0:.2f}".format(np.mean(my_devs[key]))
		payload += str(key) + ":" + str(key_rssi) + ","

	payload = payload[:-1]
	print(f'Payload = {payload}')
	client.publish(topic=topic, payload=payload)