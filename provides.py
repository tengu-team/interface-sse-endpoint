from charms.reactive import Endpoint
from charms.reactive import when, when_not
from charms.reactive import set_flag, clear_flag

class SSEEndpointProvides(Endpoint):
    @when('endpoint.{endpoint_name}.joined')
    @when_not('{endpoint_name}.consumer.available')
    def joined(self):
        set_flag(self.expand_name('{endpoint_name}.consumer.available'))


    @when_not('endpoint.{endpoint_name}.joined')
    @when('{endpoint_name}.consumer.available')
    def broken(self):
        clear_flag(self.expand_name('{endpoint_name}.consumer.available'))


    def set_base_url(self, base_url):
        """
        Publish the CA to all related applications.
        """
        for relation in self.relations:
            # All the clients get the same CA, so send it to them.
            relation.to_publish['base-url'] = base_url
