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
        self.no_resource = "resource does not exist"

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

    def delete(self, service_name, node):
        node = str(node)
        if service_name not in self.services:
            return self.no_resource

        if node not in self.services[service_name]:
            return self.no_resource

        idx = self.services[service_name].index(node)
        self.services[service_name].pop(idx)
        return self._ok
