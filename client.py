# -*- coding: utf-8 -*-
from dns import query


class DNSClient(object):
    def __init__(self, host, port=53, type="tcp"):
        self.host = host
        self.port = port
        self.type = type

    def query(self, message):
        try:
            if self.type == "tcp":
                return query.tcp(message, self.host, port=self.port)
        except:
            return None
