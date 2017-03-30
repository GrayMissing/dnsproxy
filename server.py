# -*- coding: utf-8 -*-
from gevent.server import DatagramServer
from dns.message import from_wire, make_response

from client import DNSClient


class DNSServer(DatagramServer):
    def handle(self, data, address):
        query_msg = from_wire(data)
        assert len(query_msg.question) == 1
        client = DNSClient('192.168.6.2')
        response_msg = client.query(query_msg)
        self.socket.sendto(response_msg.to_wire(), address)
