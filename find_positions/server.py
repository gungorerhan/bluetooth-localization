import paho.mqtt.client as mqtt
from device import Receiver as receiver
from prediction import Prediction as prediction
import requests


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


def upload_positions_to_cloud(card_positions, url):
	# format card positions in order to work with API
	for card_id in card_positions.keys():
		temp = card_positions[card_id]
		card_positions[card_id] = {'x':temp[0], 'y':temp[1]}

	# make post request
	response = requests.post(url, json=card_positions)
	if response.status_code != 200:
		print("HTTP request error: ", response)
	else:
		print("Positions succesfully updated to cloud!\n")

		# TODO delete later!!
		global uploaded_data_count
		uploaded_data_count += 1
		print("Upload count:", uploaded_data_count)
		if uploaded_data_count >= 1000:
			exit(0)
		


def on_message(client, userdata, message):
	global package_count
	package_count += 1
	print(f'\n{package_count} packages arrived!')

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

		# find card positions
		card_positions = pred.make_prediction()
		#print("Card positions:", card_positions)
		upload_positions_to_cloud(card_positions, add_positions_url)
	    

# main func
# global variables
add_positions_url = "https://t7ftvwr8bi.execute-api.eu-central-1.amazonaws.com/cors/position"
receivers = []
package_count = 0    # make prediction when 4 packages arrived

uploaded_data_count = 0 # TODO delete later

# mqtt related variables
HOST = "hairdresser.cloudmqtt.com"
PORT = 18407
USERNAME = "smrntlue"
PASSWORD = "T8Oenavy62jp"
TOPIC = "IPS/+/pd"

# add receiver objects
receivers.append(receiver(id="raspberry-10", x=0, y=0))   # top left
receivers.append(receiver(id="msi-gt70", x=5.25, y=0))   # top right
receivers.append(receiver(id="erhan-e570", x=2.62, y=3.45))   # bottom mid

# stores prediction dictionary, handles dictionary operations
pred = prediction(receivers, reference_distance=1, reference_rssi=-54, n=2)

# set fingerprinting
#model_filename = 'svm_final_model.sav'
#model_features = ["msi-gt70", "raspberry-10", "erhan-e570"]
#model_classes = {0: [1,1], 1: [4.25, 2.45]}
#pred.set_fingerprinting(model_filename, model_features, model_classes)


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