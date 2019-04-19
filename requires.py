from charms.reactive import when, when_not
from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint

from charmhelpers.core.hookenv import (
    log,
)

class SSEEndpointRequires(Endpoint):
    @when('endpoint.{endpoint_name}.joined')
    @when_not('{endpoint_name}.available')
    def joined(self):
        if self.base_url:
            set_flag(self.expand_name('{endpoint_name}.available'))


    @when_not('endpoint.{endpoint_name}.joined')
    @when('{endpoint_name}.available')
    def broken(self):
        log("Relation is not joined anymore; removing available state.")
        clear_flag(self.expand_name('{endpoint_name}.available'))


    @when('endpoint.{endpoint_name}.changed.base-url')
    def base_url_changed(self):
        if self.base_url:
            set_flag(self.expand_name('{endpoint_name}.changed'))
        else:
            log("base_url is unset; removing available state.")
            clear_flag(self.expand_name('{endpoint_name}.available'))

    @property
    def base_url(self):
        """
        The chain of trust for the root CA.
        """
        # only the leader of the provider should set the base-url, or all units
        # had better agree
        return self.all_joined_units.received['base-url']
