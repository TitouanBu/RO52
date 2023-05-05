from pybricks.messaging import BluetoothMailboxClient, TextMailbox

# au démarrage
client = BluetoothMailboxClient()
channel = TextMailbox("speed", client)

client.connect("ev3dev")

# while loop
speed = float(channel.read())