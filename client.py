# -*- coding: utf-8 -*-
from dns import query
from dns import resolver
import subprocess


class DNSClient(object):
    def set_address(self, host, port=53, type="tcp"):
        self.host = host
        self.port = port
        self.type = type

    def query(self, message, verify=True):
        try:
            if self.type == "tcp":
                response = query.tcp(message, self.host, port=self.port)
            elif self.type == "udp":
                response = query.udp(message, self.host, port=self.port)
            if self.verify(message):
                return response
        except:
            return None

    def verify(self, message):
        for a in message.answer:
            for rdata in a:
                address = rdata.to_text()
                if subprocess.call(["ping", "-c 1", address]) != 0:
                    return False
        return True
