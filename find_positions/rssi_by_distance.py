import psycopg2
from bluepy.btle import Scanner, DefaultDelegate
import numpy as np


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


def calculate_distance(rssi):
	n = 2
	d0 = 2
	rssi_d0 = -50
	d = float("{0:.3f}".format(d0*(10**( (rssi_d0 - float(rssi)) / (10*n)))))
	return d


def record_distance_to_db(rssi, real_distance, estimated_distance):
	# connect to db
	hostname = 'localhost'
	port = 5432
	username = 'postgres'
	password = ''
	database = 'ble_rssi'

	conn = psycopg2.connect( host=hostname, port=port, user=username, password=password, dbname=database )

	# execute query
	with conn.cursor() as cur:
		values = f'({rssi}, {real_distance}, {estimated_distance})'
		print("values = ", values)

		cur.execute("INSERT INTO rssi_distance(rssi, distance, estimated_distance) VALUES " + values + ";")

	# close db connection
	conn.commit()
	conn.close()

# scan ble devices 
mac_id = {
	"00:00:02:00:08:f4": 2292,
	"00:00:02:00:0c:3b": 3131
}
my_devs = {}
i = 0
while i<10:
	my_devs = {}

	# collect rssi values
	scanner = Scanner().withDelegate(ScanDelegate())
	devices = scanner.scan(20.0, passive=True)

	# publish rssi values
	real_distance = 4
	for key in my_devs.keys():
		if key != 3131:
			continue
		key_rssi = "{0:.2f}".format(np.mean(my_devs[key]))
		estimated_distance = calculate_distance(key_rssi)
		record_distance_to_db(key_rssi, real_distance, estimated_distance)

	i += 1

