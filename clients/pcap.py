from threading import Thread
from typing import Callable

from scapy.sendrecv import sniff


class PCap(Thread):
    def __init__(self, pkt_callback: Callable):
        self.pkt_callback = pkt_callback
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        sniff(prn=self.pkt_callback,
              filter="udp portrange 22023-22923",
              store=0)
