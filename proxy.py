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
        self.stats = {"total": 0, "success": 0}

    def get_server(self, question):
        name = question[0].name.to_text(
            omit_final_dot=True) if question else ""
        for pattern in reversed(self.servers):
            if re.search(pattern, name):
                index = self.indexes[pattern]
                self.indexes[pattern] = (
                    index + 1) % len(self.servers[pattern])
                return self.servers[pattern][index]

    def handle(self, data, address):
        print("成功解析{}次, 共解析{}次".format(self.stats["success"], self.stats[
            "total"]))
        self.stats["total"] += 1
        query_msg = from_wire(data)
        assert len(query_msg.question) == 1
        buffer = self.buffer.get(str(query_msg.question[0].name))
        if buffer:
            response_msg = make_response(query_msg)
            response_msg.answer = buffer
            self.socket.sendto(response_msg.to_wire(), address)
            self.stats["success"] += 1
            return
        client = DNSClient()
        for _ in range(2):
            server = self.get_server(query_msg.question)
            client.set_address(server)
            response_msg = client.query(query_msg)
            if response_msg and response_msg.answer:
                self.buffer[str(query_msg.question[0]
                                .name)] = response_msg.answer
                self.socket.sendto(response_msg.to_wire(), address)
                self.stats["success"] += 1
                return
        server = self.get_server("")
        client.set_address(server)
        response_msg = client.query(query_msg)
        if response_msg and response_msg.answer:
            self.buffer[str(query_msg.question[0].name)] = response_msg.answer
            self.socket.sendto(response_msg.to_wire(), address)
            self.stats["success"] += 1


if __name__ == "__main__":
    from gevent import monkey
    monkey.patch_all()
    DNSProxy(("0.0.0.0", 53), config).serve_forever()
