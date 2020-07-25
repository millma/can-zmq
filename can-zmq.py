

import time
import can
import zmq
import sys

class ZmqListener(can.Listener):
    def __init__(self, socket):
        self.sock = socket
    def on_message_received(self, msg):
        if msg is not None and msg.is_extended_id:
            msgStr = 'can0-%02X-%04X-%01d-' % (msg.arbitration_id & 0xFF, (msg.arbitration_id >> 8) & 0xFFFF, len(msg.data))
            msgStr = msgStr + '-'.join('{:02X}'.format(x) for x in msg.data)
            #print(msgStr)
            self.sock.send_string(msgStr)


if __name__ == "__main__":


    bus = can.interface.Bus(channel="can0", bustype="socketcan")
    print("Started CAN Interface")

    port = 7373
    if len(sys.argv) > 1:
        port = sys.argv[1]

    context = zmq.Context()
    sock = context.socket(zmq.PUB)
    sock.bind('tcp://*:%s' % port)

    listener = ZmqListener(sock)

    notifier = can.Notifier(bus, [listener])

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Cleaning up!")

    bus.shutdown()
    

