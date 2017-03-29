# -*- coding: utf-8 -*-
import re
from dns.message import from_wire, make_response

from server import DNSServer
from client import DNSClient
from buffer import DNSBuffer
import config


class DNSProxy(DNSServer):
    def __init__(self, address, config):
        super(DNSProxy, self).__init__(address)
        self.servers = config.servers
        self.indexes = dict((key, 0) for key in self.servers)
        self.buffer = DNSBuffer()

    def get_server(self, question):
        name = question[0].name.to_text(omit_final_dot=True)
        for pattern in reversed(self.servers):
            if re.search(pattern, name):
                index = self.indexes[pattern]
                self.indexes[pattern] = (index + 1) % len(self.servers[pattern])
                return self.servers[pattern][index]

    def handle(self, data, address):
        query_msg = from_wire(data)
        print(query_msg.question)
        assert len(query_msg.question) == 1
        if str(query_msg.question[0].name) in self.buffer:
            print("hit buffer")
            response_msg = make_response(query_msg)
            response_msg.answer = self.buffer[str(query_msg.question[0].name)]
            self.socket.sendto(response_msg.to_wire(), address)
            return
        while 1:
            server = self.get_server(query_msg.question)
            print(server)
            client = DNSClient(server)
            response_msg = client.query(query_msg)
            if response_msg:
                self.buffer[str(query_msg.question[0].name)] = response_msg.answer
                self.socket.sendto(response_msg.to_wire(), address)
                return


if __name__ == "__main__":
    from gevent import monkey; monkey.patch_all()
    DNSProxy(("127.0.0.1", 53), config).serve_forever()
