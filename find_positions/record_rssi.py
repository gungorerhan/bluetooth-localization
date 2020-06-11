import paho.mqtt.client as mqtt
from device import Receiver as receiver
from prediction import Prediction as prediction


def on_connect(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))


def parse_package(message):
    splitted_message = str(message.payload.decode("utf-8")).split(',')
    splitted_message_topic = message.topic.split('/')
    receiver_id = splitted_message_topic[1]

    for each_message in splitted_message:
        card_id, rssi = each_message.split(':')
        card_id, rssi = int(card_id), float(rssi)
        pred.add_new_value(card_id, receiver_id, rssi)


def on_message(client, userdata, message):
	global package_count
	package_count += 1
	print(f'{package_count} packages arrived!')

	print(message.topic+"\n"+str(message.payload.decode("utf-8")))
	parse_package(message)

	if (package_count == 3):
		package_count = 0

		# check if each receiver sent rssi of each card
		error = 0
		for card_id in pred.pred_dict.keys():
			if(len(pred.pred_dict[card_id]) < len(pred.receivers)):
				error = 1

		if error==1:
			pred.pred_dict.clear()
			pred.distance_dict.clear()
			return

		pred.print_predictionDict()
		pred.calculate_distances()
		pred.print_distanceDict()
		pred.pred_dict.clear()
		pred.distance_dict.clear()

		#record_rssi_log


# main func
# global variables
receivers = []
package_count = 0    # make prediction when 4 packages arrived

uploaded_data_count = 0 # TODO delete later

# mqtt related variables
HOST = "hairdresser.cloudmqtt.com"
PORT = 18407
USERNAME = "smrntlue"
PASSWORD = "T8Oenavy62jp"
TOPIC = "IPS/+/rssi"

# add receiver objects
receivers.append(receiver(id="raspberry-10", x=0, y=0))   # top left
receivers.append(receiver(id="msi-gt70", x=5.25, y=0))   # top right
receivers.append(receiver(id="erhan-e570", x=2.62, y=3.45))   # bottom mid

# stores prediction dictionary, handles dictionary operations
pred = prediction(receivers, reference_distance=1, reference_rssi=-54, n=2)

# create client
client = mqtt.Client()

# set callback functions
client.on_connect = on_connect
client.on_message = on_message

# set username and password
client.username_pw_set(USERNAME, PASSWORD)

# connect to broker
client.connect(HOST, PORT, 60)

# subscribe to periodic data topics
client.subscribe(topic=TOPIC)

client.loop_forever()