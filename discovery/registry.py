"""
    registry services format:
    {
        service1: {
                    id1: {
                            host:host
                            uri_list:uri_list
                         },
                    id2: {
                            host:host
                            uri_list:uri_list
                         }
                    }
    }
"""


class Registry:
    def __init__(self):
        self.host = "host"
        self.uri_list = "uri_list"
        self._id = 0
        self.services = {}
        self._ok = "success"

    def register(self, service, host, endpoint):
        if service not in self.services.keys():
            self.services[service] = {}

        if not self.services[service]:
            self.services[service][self._id] = {self.host: host,
                                                self.uri_list: [endpoint]}
            self._id += 1
            return self._ok

        for cur_id in self.services[service].keys():
            if host in self.services[service][cur_id][self.host]:
                if endpoint not in self.services[service][cur_id][self.uri_list]:
                    self.services[service][cur_id][self.uri_list].append(endpoint)
                return self._ok

        self.services[service][self._id] = {self.host: host,
                                            self.uri_list: [endpoint]}
        self._id += 1
        return self._ok

    def get(self, service_name):
        return self.services[service_name]
