import paho.mqtt.client as mqtt
from device import Receiver as receiver
from prediction import Prediction as prediction
import psycopg2
import numpy as np

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


def record_rssi_log(receivers, distance_dict, pred_dict):
	# card position dict
	card_positions_temp = {3131:[1.20, 1.70], 2292:[4.05, 1.70]}
	card_distance_temp = {
							3131:{},
							2292:{}
						 }

	# calculate real distances between temporary card positions and receivers
	for card_id, val in card_positions_temp.items():
	    for rec in receivers:
	        distance_to_rec = np.sqrt((val[0]-rec.x)**2 + (val[1]-rec.y)**2)
	        card_distance_temp[card_id][rec.id] = distance_to_rec

	# print card_distance_temp dictionary
	for key in card_distance_temp.keys():
		print("\nReal distances between receiver and temporary card positions")
		print(f'key = {key}')
		for k,v in card_distance_temp[key].items():	
			print(f'{k}: {v}')

	# connect to db
	hostname = 'localhost'
	port = 5432
	username = 'postgres'
	password = ''
	database = 'ble_rssi'

	conn = psycopg2.connect( host=hostname, port=port, user=username, password=password, dbname=database )

	with conn.cursor() as cur:
		values = ""
		for card_id, distance_values in distance_dict.items():
			for distance_val in distance_values:
				rssi = 0
				for pred_val in pred_dict[card_id]:
					print(pred_val[0])
					print(distance_val)
					print(distance_val[0])
					if pred_val[0] == distance_val[0]:
						rssi = pred_val[1]
						print(rssi)
						break;

				card_x, card_y = card_positions_temp[card_id]
				real_distance = card_distance_temp[card_id][distance_val[0]]

				values += f"({card_id}, '{distance_val[0]}', {rssi}, {distance_val[2]}, {distance_val[3]}, {card_x}, {card_y}, {real_distance}, {distance_val[1]}),"

		values = values[:-1]
		print("values = ", values)

		cur.execute("INSERT INTO rssi_log (card_id, receiver_id, receiver_x, receiver_y, rssi, card_x, card_y, real_distance, estimated_distance) VALUES " + values + ";")

	# close db connection
	conn.commit()
	conn.close()


def on_message(client, userdata, message):
	try:
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

			pred.print_predictionDict()
			pred.calculate_distances()
			pred.print_distanceDict()

			# record rssi log to db
			global receivers
			record_rssi_log(receivers, pred.distance_dict, pred.pred_dict)

			pred.pred_dict.clear()
			pred.distance_dict.clear()

	except Exception as e:
		print(e)
		exit()


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