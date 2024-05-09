import unittest
from ipaddress import IPv4Address
from unittest.mock import Mock
from uuid import uuid4

from parameterized import parameterized  # type: ignore

from catalystwan.api.configuration_groups.parcel import Global, as_global, as_variable
from catalystwan.api.feature_profile_api import (
    ServiceFeatureProfileAPI,
    SystemFeatureProfileAPI,
    TransportFeatureProfileAPI,
)
from catalystwan.endpoints.configuration.feature_profile.sdwan.service import ServiceFeatureProfile
from catalystwan.endpoints.configuration.feature_profile.sdwan.system import SystemFeatureProfile
from catalystwan.endpoints.configuration.feature_profile.sdwan.transport import TransportFeatureProfile
from catalystwan.models.configuration.feature_profile.parcel import ParcelAssociationPayload, ParcelCreationResponse
from catalystwan.models.configuration.feature_profile.sdwan.service import (
    AppqoeParcel,
    InterfaceEthernetParcel,
    InterfaceGreParcel,
    InterfaceIpsecParcel,
    InterfaceSviParcel,
    LanVpnDhcpServerParcel,
    LanVpnParcel,
    OspfParcel,
    SwitchportParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.acl import Ipv4AclParcel, Ipv6AclParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.eigrp import EigrpParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.gre import BasicGre
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ipsec import IpsecAddress, IpsecTunnelMode
from catalystwan.models.configuration.feature_profile.sdwan.service.multicast import MulticastParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.ospfv3 import Ospfv3IPv4Parcel, Ospfv3IPv6Parcel
from catalystwan.models.configuration.feature_profile.sdwan.service.route_policy import RoutePolicyParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.wireless_lan import WirelessLanParcel
from catalystwan.models.configuration.feature_profile.sdwan.system import (
    AAAParcel,
    BannerParcel,
    BasicParcel,
    BFDParcel,
    GlobalParcel,
    LoggingParcel,
    MRFParcel,
    NTPParcel,
    OMPParcel,
    SecurityParcel,
    SNMPParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport import (
    ManagementVpnParcel,
    T1E1ControllerParcel,
    TransportVpnParcel,
)

system_endpoint_mapping = {
    AAAParcel: "aaa",
    BannerParcel: "banner",
    BasicParcel: "basic",
    BFDParcel: "bfd",
    GlobalParcel: "global",
    LoggingParcel: "logging",
    MRFParcel: "mrf",
    NTPParcel: "ntp",
    OMPParcel: "omp",
    SecurityParcel: "security",
    SNMPParcel: "snmp",
}


class TestSystemFeatureProfileAPI(unittest.TestCase):
    def setUp(self):
        self.profile_uuid = uuid4()
        self.parcel_uuid = uuid4()
        self.mock_session = Mock()
        self.mock_endpoint = Mock(spec=SystemFeatureProfile)
        self.api = SystemFeatureProfileAPI(self.mock_session)
        self.api.endpoint = self.mock_endpoint

    @parameterized.expand(system_endpoint_mapping.items())
    def test_delete_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.delete_parcel(self.profile_uuid, parcel, self.parcel_uuid)

        # Assert
        self.mock_endpoint.delete.assert_called_once_with(self.profile_uuid, expected_path, self.parcel_uuid)

    @parameterized.expand(system_endpoint_mapping.items())
    def test_get_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.get_parcel(self.profile_uuid, parcel, self.parcel_uuid)

        # Assert
        self.mock_endpoint.get_by_id.assert_called_once_with(self.profile_uuid, expected_path, self.parcel_uuid)

    @parameterized.expand(system_endpoint_mapping.items())
    def test_get_all_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.get_parcels(self.profile_uuid, parcel)

        # Assert
        self.mock_endpoint.get_all.assert_called_once_with(self.profile_uuid, expected_path)

    @parameterized.expand(system_endpoint_mapping.items())
    def test_create_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.create_parcel(self.profile_uuid, parcel)

        # Assert
        self.mock_endpoint.create.assert_called_once_with(self.profile_uuid, expected_path, parcel)

    @parameterized.expand(system_endpoint_mapping.items())
    def test_update_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.update_parcel(self.profile_uuid, parcel, self.parcel_uuid)

        # Assert
        self.mock_endpoint.update.assert_called_once_with(self.profile_uuid, expected_path, self.parcel_uuid, parcel)


service_endpoint_mapping = {
    LanVpnDhcpServerParcel: "dhcp-server",
    AppqoeParcel: "appqoe",
    LanVpnParcel: "lan/vpn",
    OspfParcel: "routing/ospf",
    Ospfv3IPv4Parcel: "routing/ospfv3/ipv4",
    Ospfv3IPv6Parcel: "routing/ospfv3/ipv6",
    RoutePolicyParcel: "route-policy",
    EigrpParcel: "routing/eigrp",
    Ipv6AclParcel: "ipv6-acl",
    Ipv4AclParcel: "ipv4-acl",
    SwitchportParcel: "switchport",
    MulticastParcel: "routing/multicast",
    WirelessLanParcel: "wirelesslan",
}

service_interface_parcels = [
    (
        "interface/gre",
        InterfaceGreParcel(
            parcel_name="TestGreParcel",
            parcel_description="Test Gre Parcel",
            basic=BasicGre(
                if_name=as_global("gre1"),
                tunnel_destination=as_global(IPv4Address("4.4.4.4")),
            ),
        ),
    ),
    (
        "interface/svi",
        InterfaceSviParcel(
            parcel_name="TestSviParcel",
            parcel_description="Test Svi Parcel",
            interface_name=as_global("Vlan1"),
            svi_description=as_global("Test Svi Description"),
        ),
    ),
    (
        "interface/ethernet",
        InterfaceEthernetParcel(
            parcel_name="TestEthernetParcel",
            parcel_description="Test Ethernet Parcel",
            interface_name=as_global("HundredGigE"),
            ethernet_description=as_global("Test Ethernet Description"),
        ),
    ),
    (
        "interface/ipsec",
        InterfaceIpsecParcel(
            parcel_name="TestIpsecParcel",
            parcel_description="Test Ipsec Parcel",
            interface_name=as_global("ipsec2"),
            ipsec_description=as_global("Test Ipsec Description"),
            pre_shared_secret=as_global("123"),
            ike_local_id=as_global("123"),
            ike_remote_id=as_global("123"),
            application=as_variable("{{ipsec_application}}"),
            tunnel_mode=Global[IpsecTunnelMode](value="ipv6"),
            tunnel_destination_v6=as_variable("{{ipsec_tunnelDestinationV6}}"),
            tunnel_source_v6=Global[str](value="::"),
            tunnel_source_interface=as_variable("{{ipsec_ipsecSourceInterface}}"),
            ipv6_address=as_variable("{{test}}"),
            address=IpsecAddress(address=as_global("10.0.0.1"), mask=as_global("255.255.255.0")),
            tunnel_destination=IpsecAddress(address=as_global("10.0.0.5"), mask=as_global("255.255.255.0")),
            mtu_v6=as_variable("{{test}}"),
        ),
    ),
]

service_vpn_sub_parcels = [
    (
        "routing/multicast",
        MulticastParcel(
            parcel_name="TestMulticastParcel",
            parcel_description="Test Multicast Parcel",
        ),
    )
]


class TestServiceFeatureProfileAPI(unittest.TestCase):
    def setUp(self):
        self.profile_uuid = uuid4()
        self.vpn_uuid = uuid4()
        self.parcel_uuid = uuid4()
        self.mock_session = Mock()
        self.mock_endpoint = Mock(spec=ServiceFeatureProfile)
        self.api = ServiceFeatureProfileAPI(self.mock_session)
        self.api.endpoint = self.mock_endpoint

    @parameterized.expand(service_endpoint_mapping.items())
    def test_post_method_parcel(self, parcel, parcel_type):
        # Act
        self.api.create_parcel(self.profile_uuid, parcel)

        # Assert
        self.mock_endpoint.create_service_parcel.assert_called_once_with(self.profile_uuid, parcel_type, parcel)

    @parameterized.expand(service_interface_parcels)
    def test_post_method_interface_parcel(self, parcel_type, parcel):
        # Act
        self.api.create_parcel(self.profile_uuid, parcel, self.vpn_uuid)

        # Assert
        self.mock_endpoint.create_lan_vpn_sub_parcel.assert_called_once_with(
            self.profile_uuid, self.vpn_uuid, parcel_type, parcel
        )

    @parameterized.expand(service_vpn_sub_parcels)
    def test_post_method_create_then_assigin_subparcel(self, parcel_type, parcel):
        # Arrange
        self.mock_endpoint.create_service_parcel.return_value = ParcelCreationResponse(id=self.parcel_uuid)

        # Act
        self.api.create_parcel(self.profile_uuid, parcel, self.vpn_uuid)

        # Assert
        self.mock_endpoint.create_service_parcel.assert_called_once_with(self.profile_uuid, parcel_type, parcel)
        self.mock_endpoint.associate_parcel_with_vpn.assert_called_once_with(
            self.profile_uuid,
            self.vpn_uuid,
            parcel_type,
            ParcelAssociationPayload(parcel_id=self.parcel_uuid),
        )


transport_enpoint_mapping = {
    T1E1ControllerParcel: "t1-e1-controller",
    ManagementVpnParcel: "management/vpn",
    TransportVpnParcel: "wan/vpn",
}


class TestTransportFeatureProfileAPI(unittest.TestCase):
    def setUp(self):
        self.profile_uuid = uuid4()
        self.vpn_uuid = uuid4()
        self.parcel_uuid = uuid4()
        self.mock_session = Mock()
        self.mock_endpoint = Mock(spec=TransportFeatureProfile)
        self.api = TransportFeatureProfileAPI(self.mock_session)
        self.api.endpoint = self.mock_endpoint

    @parameterized.expand(transport_enpoint_mapping.items())
    def test_post_method_parcel(self, parcel, parcel_type):
        # Act
        self.api.create_parcel(self.profile_uuid, parcel)

        # Assert
        self.mock_endpoint.create_transport_parcel.assert_called_once_with(self.profile_uuid, parcel_type, parcel)
