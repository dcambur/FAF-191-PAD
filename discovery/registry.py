"""
    registry services format:
    {
        service1: [host1, host2 ... hostN],
        ...
        serviceN: [host1, host2 ... hostN]
    }
"""


class Registry:
    def __init__(self):
        self.services = {}
        self._ok = "success"

    def register(self, service, host):
        if service not in self.services.keys():
            self.services[service] = []

        if not self.services[service]:
            self.services[service] = []

        if host in self.services[service]:
            return self._ok

        self.services[service].append(host)
        return self._ok

    def get(self, service_name):
        return self.services[service_name]
