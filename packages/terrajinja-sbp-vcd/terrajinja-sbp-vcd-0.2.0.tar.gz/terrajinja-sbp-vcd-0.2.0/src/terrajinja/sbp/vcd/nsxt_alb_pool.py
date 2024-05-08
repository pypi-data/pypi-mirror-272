from dataclasses import dataclass
from constructs import Construct
from terrajinja.imports.vcd.nsxt_alb_pool import NsxtAlbPool
from .decorators import run_once
from .nsxt_ip_set import SbpVcdNsxtIpSet
from ipaddress import IPv4Network, AddressValueError


@dataclass
class SbpLoadbalancerPool:
    scope: Construct
    destination_address_name: str
    destination_port: int
    edge_gateway_id: str
    destination_address: list
    algorithm: str
    default_port: int
    persistence: str

    def __post_init__(self):
        object.__setattr__(self, "algorithm", self.algorithm.upper().replace(' ', '_'))

    @property
    def name(self):
        return f"{self.destination_address_name}-{self.destination_port}-pool".upper()

    @property
    def member_group_id(self):
        return [SbpVcdNsxtIpSet(
            scope=self.scope,
            edge_gateway_id=self.edge_gateway_id,
            name=self.destination_address_name,
            ip_addresses=self.destination_address
        ).id][0]

    @property
    def persistence_profile(self):
        return {
            'type': self.persistence.upper().replace(' ', '_')
        }


@run_once(parameter_match=["destination_address_name", "destination_port"])
class SbpVcdNsxtAlbPool(NsxtAlbPool):
    """Extends the original class to ensure that it only gets called once"""

    def __init__(self, scope: Construct, destination_address_name: str, destination_port: int,
                 algorithm: str, persistence: str, vip_port: int, destination_address: list,
                 edge_gateway_id: str, id_=None, **kwargs):

        pool = SbpLoadbalancerPool(
            scope=scope,
            destination_address_name=destination_address_name,
            destination_port=destination_port,
            algorithm=algorithm,
            persistence=persistence,
            default_port=vip_port,
            destination_address=destination_address,
            edge_gateway_id=edge_gateway_id
        )

        # destination can be a set of ip, or a link to a resource (e.g. security group/ precreated ip set)
        if isinstance(destination_address, str):
            destination_address = [destination_address]

        # test if destination is an ip or resource
        try:
            IPv4Network(destination_address[0])
            member_group_id = pool.member_group_id
            default_port = pool.default_port
            algorithm = pool.algorithm
            persistence = pool.persistence_profile
        except AddressValueError:
            member_group_id = destination_address[0]
            default_port = destination_port
            algorithm = algorithm.upper().replace(' ', '_')
            persistence = {
                'type': persistence.upper().replace(' ', '_')
            }

        super().__init__(
            scope=scope,
            id_=pool.name,
            name=pool.name,
            algorithm=algorithm,
            persistence_profile=persistence,
            default_port=default_port,
            member_group_id=member_group_id,
            edge_gateway_id=edge_gateway_id,
            lifecycle={'create_before_destroy': True},
            **kwargs
        )
