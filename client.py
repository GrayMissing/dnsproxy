# -*- coding: utf-8 -*-
from dns import query
from dns import resolver


class DNSClient(object):
    def set_address(self, host, port=53, type="tcp"):
        self.host = host
        self.port = port
        self.type = type

    def query(self, message):
        try:
            if self.type == "tcp":
                response = query.tcp(message, self.host, port=self.port)
                return response
            elif self.type == "udp":
                response = query.udp(message, self.host, port=self.port)
                return response
        except:
            return None
