from pybricks.messaging import BluetoothMailboxClient, TextMailbox

# au démarrage
client = BluetoothMailboxClient()
channel = TextMailbox("speed", client)

try:
    client.connect("maestro")
except:
    # Tout ou rien
    pass
# while loop
speed = float(channel.read())