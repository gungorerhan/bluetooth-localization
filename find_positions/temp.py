from device import Receiver as receiver
from prediction import Prediction as prediction
import requests

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

receivers = []
url = "https://t7ftvwr8bi.execute-api.eu-central-1.amazonaws.com/cors/position"

# add receiver objects
receivers.append(receiver(id="raspberry-10", x=0, y=0))   # top left
receivers.append(receiver(id="msi-gt70", x=5.25, y=0))   # top right
receivers.append(receiver(id="erhan-E570", x=2.62, y=3.45))   # bottom mid

# stores prediction dictionary, handles dictionary operations
pred = prediction(receivers, reference_distance=1, reference_rssi=-54, n=2)
pred.add_new_value(2292, "raspberry-10", -60)
pred.add_new_value(2292, "erhan-E570", -65)
pred.add_new_value(2292, "msi-gt70", -54)

pred.add_new_value(3131, "raspberry-10", -50)
pred.add_new_value(3131, "erhan-E570", -62)
pred.add_new_value(3131, "msi-gt70", -70)
#pred.print_predictionDict()
card_positions = pred.make_prediction()
upload_positions_to_cloud(card_positions, url)
