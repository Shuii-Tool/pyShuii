# proxy, request, retrieve
import ssl


class ProxyClient:
    def __init__(self, proxies):
        self.proxies = proxies.strip().split('\n')
