class Registry:
    def __init__(self):
        self.services = {}
        self._endpoint_exists = "endpoint already exists"
        self._ok = "success"

    def register(self, service, host, endpoint):
        if service not in self.services.keys():
            self.services[service] = {}

        if host not in self.services[service].keys():
            self.services[service][host] = []

        if endpoint not in self.services[service][host]:
            self.services[service][host].append(endpoint)
        else:
            return self._endpoint_exists

        return self._ok

    def get(self, service_name):
        return self.services[service_name]
