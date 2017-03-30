# -*- coding: utf-8 -*-
import time


class DNSBuffer(dict):
    def __init__(self, timeout=3600):
        self.timeouts = {}
        self.timeout = timeout

    def __setitem__(self, key, value):
        self.timeouts[key] = time.time() + self.timeout
        super(DNSBuffer, self).__setitem__(key, value)

    def __getitem__(self, key):
        if key in self:
            if self.timeouts[key] <= time.time():
                del self[key]
                del self.timeouts[key]
                return None
        return super(DNSBuffer, self).__getitem__(key)

    def __iter__(self):
        for key in self:
            if self.timeouts[key] > time.time():
                yield key


if __name__ == "__main__":
    buffer = DNSBuffer(timeout=1)
    buffer["key"] = "value"
    print(buffer["key"], buffer)
    time.sleep(2)
    print(buffer["key"], buffer)
