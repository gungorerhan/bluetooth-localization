import paho.mqtt.client as mqtt

HOST = "hairdresser.cloudmqtt.com"
PORT = 18407
USERNAME = "smrntlue"
PASSWORD = "T8Oenavy62jp"

TOPIC = "IPS/+/pd"

my_devs = [2292, 3131]
package_count = 0

cards = {2292: [], 3131: []}
positions = {2292: None, 3131: None}

def on_connect(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))

def make_prediction():
    for key in cards.keys():
        cards[key].sort(key = lambda x: x[1], reverse=True)
        dev, rssi = cards[key][0]
        positions[key] = dev

    print("=======Positions=======")
    for key in positions:
        print(f'Key: {key}, Position: {positions[key]}')

def parse_package(message):

    splitted_message = str(message.payload.decode("utf-8")).split(',')
    splitted_message_topic = message.topic.split('/')
    device = splitted_message_topic[1]

    for each_message in splitted_message:
        key, rssi = each_message.split(':')
        key, rssi = int(key), float(rssi)
        cards[key].append((device, rssi))
    

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode("utf-8")))

    parse_package(msg)

    global package_count
    package_count += 1
    print(f'{package_count} packages arrived!')
    if (package_count == 2):
        package_count = 0
        make_prediction()

        # clear global variables
        global cards
        cards = {2292: [], 3131: []}
        global positions
        positions = {2292: 0, 3131: 0}

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(USERNAME, PASSWORD)
client.connect(HOST, PORT, 60)

client.subscribe(topic=TOPIC)

client.loop_forever()



