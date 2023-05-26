from pybricks.messaging import BluetoothMailboxServer, TextMailbox

# au démarrage :
server = BluetoothMailboxServer()
channel = TextMailbox("speed",server)
try:
    server.wait_for_connection()
except:
    pass

# à integrer dans le cycle loop :
try:
    channel.send("speed")
except:
    pass

