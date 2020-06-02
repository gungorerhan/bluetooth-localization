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

# receiver positions
receivers = {
            "erhan-e570":   [2.62, 0],
            "msi-gt70":     [5.25, 3.45],
            "raspberry-10": [0, 3.45]
            }

def on_connect(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))

def find_positions():
    for card_id in cards.keys():
        cards[card_id].sort(key = lambda x: x[1], reverse=True)
        dev, rssi = cards[card_id][0]
        positions[card_id] = dev

    print("=======Positions=======")
    for card_id in positions:
        print(f'Key: {card_id}, Position: {positions[card_id]}')

def parse_package(message):
    splitted_message = str(message.payload.decode("utf-8")).split(',')
    splitted_message_topic = message.topic.split('/')
    device = splitted_message_topic[1]

    for each_message in splitted_message:
        card_id, rssi = each_message.split(':')
        card_id, rssi = int(card_id), float(rssi)
        cards[card_id].append((device, rssi))
    

def on_message(client, userdata, msg):
    global package_count
    package_count += 1
    print(f'{package_count} packages arrived!')

    print(msg.topic+"\n"+str(msg.payload.decode("utf-8")))
    parse_package(msg)

    if (package_count == 3):
        package_count = 0
        find_positions()

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



