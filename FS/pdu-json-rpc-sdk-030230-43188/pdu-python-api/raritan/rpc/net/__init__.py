# Do NOT edit this file!
# It was generated by IdlC class idl.json.python.ProxyAsnVisitor.

#
# Section generated from "/home/nb/builds/MEGA/px2-3.2.30-3.2.39-branch-20160511-none-release-none-pdu-raritan/fwcomponents/mkdist/tmp/px2_final/libisys/src/idl/Diagnostics.idl"
#

import raritan.rpc
from raritan.rpc import Interface, Structure, ValueObject, Enumeration, typecheck, DecodeException

# interface
class Diagnostics(Interface):
    idlType = "net.Diagnostics:1.0.0"

    NO_ERROR = 0

    ERR_INVALID_PARAM = 1

    ERR_EXEC_FAIL = 2

    ERR_TIMEOUT = 3

    ERR_RESOLVE_FAIL = 4

    class _ping(Interface.Method):
        name = 'ping'

        @staticmethod
        def encode(hostName, count):
            typecheck.is_string(hostName, AssertionError)
            typecheck.is_int(count, AssertionError)
            args = {}
            args['hostName'] = hostName
            args['count'] = count
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = rsp['_ret_']
            results = [x0 for x0 in rsp['results']]
            typecheck.is_int(_ret_, DecodeException)
            for x0 in results:
                typecheck.is_string(x0, DecodeException)
            return (_ret_, results)

    class _traceRoute(Interface.Method):
        name = 'traceRoute'

        @staticmethod
        def encode(hostName, timeout, useIcmp):
            typecheck.is_string(hostName, AssertionError)
            typecheck.is_int(timeout, AssertionError)
            typecheck.is_bool(useIcmp, AssertionError)
            args = {}
            args['hostName'] = hostName
            args['timeout'] = timeout
            args['useIcmp'] = useIcmp
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = rsp['_ret_']
            results = [x0 for x0 in rsp['results']]
            typecheck.is_int(_ret_, DecodeException)
            for x0 in results:
                typecheck.is_string(x0, DecodeException)
            return (_ret_, results)

    class _listTcpConnections(Interface.Method):
        name = 'listTcpConnections'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = rsp['_ret_']
            results = [x0 for x0 in rsp['results']]
            typecheck.is_int(_ret_, DecodeException)
            for x0 in results:
                typecheck.is_string(x0, DecodeException)
            return (_ret_, results)
    def __init__(self, target, agent):
        super(Diagnostics, self).__init__(target, agent)
        self.ping = Diagnostics._ping(self)
        self.traceRoute = Diagnostics._traceRoute(self)
        self.listTcpConnections = Diagnostics._listTcpConnections(self)
# Do NOT edit this file!
# It was generated by IdlC class idl.json.python.ProxyAsnVisitor.

#
# Section generated from "/home/nb/builds/MEGA/px2-3.2.30-3.2.39-branch-20160511-none-release-none-pdu-raritan/fwcomponents/mkdist/tmp/px2_final/libisys/src/idl/Net.idl"
#

import raritan.rpc
from raritan.rpc import Interface, Structure, ValueObject, Enumeration, typecheck, DecodeException
import raritan.rpc.net


# enumeration
class AutoConfigs(Enumeration):
    idlType = "net.AutoConfigs:1.0.0"
    values = ["STATIC", "DHCP", "AUTO"]

AutoConfigs.STATIC = AutoConfigs(0)
AutoConfigs.DHCP = AutoConfigs(1)
AutoConfigs.AUTO = AutoConfigs(2)

# structure
class NetworkConfigIP(Structure):
    idlType = "net.NetworkConfigIP:1.0.0"
    elements = ["gai_prefer_ipv6"]

    def __init__(self, gai_prefer_ipv6):
        typecheck.is_bool(gai_prefer_ipv6, AssertionError)

        self.gai_prefer_ipv6 = gai_prefer_ipv6

    @classmethod
    def decode(cls, json, agent):
        obj = cls(
            gai_prefer_ipv6 = json['gai_prefer_ipv6'],
        )
        return obj

    def encode(self):
        json = {}
        json['gai_prefer_ipv6'] = self.gai_prefer_ipv6
        return json

# structure
class IPv4RoutingEntry(Structure):
    idlType = "net.IPv4RoutingEntry:1.0.0"
    elements = ["dest", "nexthop", "intf"]

    def __init__(self, dest, nexthop, intf):
        typecheck.is_string(dest, AssertionError)
        typecheck.is_string(nexthop, AssertionError)
        typecheck.is_string(intf, AssertionError)

        self.dest = dest
        self.nexthop = nexthop
        self.intf = intf

    @classmethod
    def decode(cls, json, agent):
        obj = cls(
            dest = json['dest'],
            nexthop = json['nexthop'],
            intf = json['intf'],
        )
        return obj

    def encode(self):
        json = {}
        json['dest'] = self.dest
        json['nexthop'] = self.nexthop
        json['intf'] = self.intf
        return json

# structure
class NetworkConfigIPv4(Structure):
    idlType = "net.NetworkConfigIPv4:1.0.0"
    elements = ["enabled", "autocfg", "ipaddr", "netmask", "gateway", "hostname", "dns_suffixes", "override_dns", "dns_ip_1", "dns_ip_2", "domain_name"]

    def __init__(self, enabled, autocfg, ipaddr, netmask, gateway, hostname, dns_suffixes, override_dns, dns_ip_1, dns_ip_2, domain_name):
        typecheck.is_bool(enabled, AssertionError)
        typecheck.is_enum(autocfg, raritan.rpc.net.AutoConfigs, AssertionError)
        typecheck.is_string(ipaddr, AssertionError)
        typecheck.is_string(netmask, AssertionError)
        typecheck.is_string(gateway, AssertionError)
        typecheck.is_string(hostname, AssertionError)
        for x0 in dns_suffixes:
            typecheck.is_string(x0, AssertionError)
        typecheck.is_bool(override_dns, AssertionError)
        typecheck.is_string(dns_ip_1, AssertionError)
        typecheck.is_string(dns_ip_2, AssertionError)
        typecheck.is_string(domain_name, AssertionError)

        self.enabled = enabled
        self.autocfg = autocfg
        self.ipaddr = ipaddr
        self.netmask = netmask
        self.gateway = gateway
        self.hostname = hostname
        self.dns_suffixes = dns_suffixes
        self.override_dns = override_dns
        self.dns_ip_1 = dns_ip_1
        self.dns_ip_2 = dns_ip_2
        self.domain_name = domain_name

    @classmethod
    def decode(cls, json, agent):
        obj = cls(
            enabled = json['enabled'],
            autocfg = raritan.rpc.net.AutoConfigs.decode(json['autocfg']),
            ipaddr = json['ipaddr'],
            netmask = json['netmask'],
            gateway = json['gateway'],
            hostname = json['hostname'],
            dns_suffixes = [x0 for x0 in json['dns_suffixes']],
            override_dns = json['override_dns'],
            dns_ip_1 = json['dns_ip_1'],
            dns_ip_2 = json['dns_ip_2'],
            domain_name = json['domain_name'],
        )
        return obj

    def encode(self):
        json = {}
        json['enabled'] = self.enabled
        json['autocfg'] = raritan.rpc.net.AutoConfigs.encode(self.autocfg)
        json['ipaddr'] = self.ipaddr
        json['netmask'] = self.netmask
        json['gateway'] = self.gateway
        json['hostname'] = self.hostname
        json['dns_suffixes'] = [x0 for x0 in self.dns_suffixes]
        json['override_dns'] = self.override_dns
        json['dns_ip_1'] = self.dns_ip_1
        json['dns_ip_2'] = self.dns_ip_2
        json['domain_name'] = self.domain_name
        return json

# structure
class NetworkConfigIPv6(Structure):
    idlType = "net.NetworkConfigIPv6:1.0.0"
    elements = ["enabled", "autocfg", "ipaddr", "gateway", "hostname", "dns_suffixes", "override_dns", "dns_ip_1", "dns_ip_2", "domain_name"]

    def __init__(self, enabled, autocfg, ipaddr, gateway, hostname, dns_suffixes, override_dns, dns_ip_1, dns_ip_2, domain_name):
        typecheck.is_bool(enabled, AssertionError)
        typecheck.is_enum(autocfg, raritan.rpc.net.AutoConfigs, AssertionError)
        typecheck.is_string(ipaddr, AssertionError)
        typecheck.is_string(gateway, AssertionError)
        typecheck.is_string(hostname, AssertionError)
        for x0 in dns_suffixes:
            typecheck.is_string(x0, AssertionError)
        typecheck.is_bool(override_dns, AssertionError)
        typecheck.is_string(dns_ip_1, AssertionError)
        typecheck.is_string(dns_ip_2, AssertionError)
        typecheck.is_string(domain_name, AssertionError)

        self.enabled = enabled
        self.autocfg = autocfg
        self.ipaddr = ipaddr
        self.gateway = gateway
        self.hostname = hostname
        self.dns_suffixes = dns_suffixes
        self.override_dns = override_dns
        self.dns_ip_1 = dns_ip_1
        self.dns_ip_2 = dns_ip_2
        self.domain_name = domain_name

    @classmethod
    def decode(cls, json, agent):
        obj = cls(
            enabled = json['enabled'],
            autocfg = raritan.rpc.net.AutoConfigs.decode(json['autocfg']),
            ipaddr = json['ipaddr'],
            gateway = json['gateway'],
            hostname = json['hostname'],
            dns_suffixes = [x0 for x0 in json['dns_suffixes']],
            override_dns = json['override_dns'],
            dns_ip_1 = json['dns_ip_1'],
            dns_ip_2 = json['dns_ip_2'],
            domain_name = json['domain_name'],
        )
        return obj

    def encode(self):
        json = {}
        json['enabled'] = self.enabled
        json['autocfg'] = raritan.rpc.net.AutoConfigs.encode(self.autocfg)
        json['ipaddr'] = self.ipaddr
        json['gateway'] = self.gateway
        json['hostname'] = self.hostname
        json['dns_suffixes'] = [x0 for x0 in self.dns_suffixes]
        json['override_dns'] = self.override_dns
        json['dns_ip_1'] = self.dns_ip_1
        json['dns_ip_2'] = self.dns_ip_2
        json['domain_name'] = self.domain_name
        return json

# structure
class IPv6RoutingEntry(Structure):
    idlType = "net.IPv6RoutingEntry:1.0.0"
    elements = ["dest", "nexthop", "intf"]

    def __init__(self, dest, nexthop, intf):
        typecheck.is_string(dest, AssertionError)
        typecheck.is_string(nexthop, AssertionError)
        typecheck.is_string(intf, AssertionError)

        self.dest = dest
        self.nexthop = nexthop
        self.intf = intf

    @classmethod
    def decode(cls, json, agent):
        obj = cls(
            dest = json['dest'],
            nexthop = json['nexthop'],
            intf = json['intf'],
        )
        return obj

    def encode(self):
        json = {}
        json['dest'] = self.dest
        json['nexthop'] = self.nexthop
        json['intf'] = self.intf
        return json

# structure
class NetworkActiveValuesIPv6(Structure):
    idlType = "net.NetworkActiveValuesIPv6:1.0.0"
    elements = ["enabled", "autocfg", "ipaddrs", "routes", "ra_managed", "ra_otherconf", "dns_suffixes", "dns_ip_1", "dns_ip_2"]

    def __init__(self, enabled, autocfg, ipaddrs, routes, ra_managed, ra_otherconf, dns_suffixes, dns_ip_1, dns_ip_2):
        typecheck.is_bool(enabled, AssertionError)
        typecheck.is_enum(autocfg, raritan.rpc.net.AutoConfigs, AssertionError)
        for x0 in ipaddrs:
            typecheck.is_string(x0, AssertionError)
        for x0 in routes:
            typecheck.is_struct(x0, raritan.rpc.net.IPv6RoutingEntry, AssertionError)
        typecheck.is_bool(ra_managed, AssertionError)
        typecheck.is_bool(ra_otherconf, AssertionError)
        for x0 in dns_suffixes:
            typecheck.is_string(x0, AssertionError)
        typecheck.is_string(dns_ip_1, AssertionError)
        typecheck.is_string(dns_ip_2, AssertionError)

        self.enabled = enabled
        self.autocfg = autocfg
        self.ipaddrs = ipaddrs
        self.routes = routes
        self.ra_managed = ra_managed
        self.ra_otherconf = ra_otherconf
        self.dns_suffixes = dns_suffixes
        self.dns_ip_1 = dns_ip_1
        self.dns_ip_2 = dns_ip_2

    @classmethod
    def decode(cls, json, agent):
        obj = cls(
            enabled = json['enabled'],
            autocfg = raritan.rpc.net.AutoConfigs.decode(json['autocfg']),
            ipaddrs = [x0 for x0 in json['ipaddrs']],
            routes = [raritan.rpc.net.IPv6RoutingEntry.decode(x0, agent) for x0 in json['routes']],
            ra_managed = json['ra_managed'],
            ra_otherconf = json['ra_otherconf'],
            dns_suffixes = [x0 for x0 in json['dns_suffixes']],
            dns_ip_1 = json['dns_ip_1'],
            dns_ip_2 = json['dns_ip_2'],
        )
        return obj

    def encode(self):
        json = {}
        json['enabled'] = self.enabled
        json['autocfg'] = raritan.rpc.net.AutoConfigs.encode(self.autocfg)
        json['ipaddrs'] = [x0 for x0 in self.ipaddrs]
        json['routes'] = [raritan.rpc.net.IPv6RoutingEntry.encode(x0) for x0 in self.routes]
        json['ra_managed'] = self.ra_managed
        json['ra_otherconf'] = self.ra_otherconf
        json['dns_suffixes'] = [x0 for x0 in self.dns_suffixes]
        json['dns_ip_1'] = self.dns_ip_1
        json['dns_ip_2'] = self.dns_ip_2
        return json

# structure
class ServiceConfig(Structure):
    idlType = "net.ServiceConfig:1.0.0"
    elements = ["service", "enable", "port"]

    def __init__(self, service, enable, port):
        typecheck.is_string(service, AssertionError)
        typecheck.is_bool(enable, AssertionError)
        typecheck.is_int(port, AssertionError)

        self.service = service
        self.enable = enable
        self.port = port

    @classmethod
    def decode(cls, json, agent):
        obj = cls(
            service = json['service'],
            enable = json['enable'],
            port = json['port'],
        )
        return obj

    def encode(self):
        json = {}
        json['service'] = self.service
        json['enable'] = self.enable
        json['port'] = self.port
        return json

# enumeration
class LanSpeed(Enumeration):
    idlType = "net.LanSpeed:1.0.0"
    values = ["LAN_SPEED_AUTO", "LAN_SPEED_10MBIT", "LAN_SPEED_100MBIT", "LAN_SPEED_1000MBIT", "LAN_SPEED_UNKNOWN"]

LanSpeed.LAN_SPEED_AUTO = LanSpeed(0)
LanSpeed.LAN_SPEED_10MBIT = LanSpeed(1)
LanSpeed.LAN_SPEED_100MBIT = LanSpeed(2)
LanSpeed.LAN_SPEED_1000MBIT = LanSpeed(3)
LanSpeed.LAN_SPEED_UNKNOWN = LanSpeed(4)

# enumeration
class LanDuplex(Enumeration):
    idlType = "net.LanDuplex:1.0.0"
    values = ["LAN_DUPLEX_AUTO", "LAN_DUPLEX_HALF", "LAN_DUPLEX_FULL", "LAN_DUPLEX_UNKNOWN"]

LanDuplex.LAN_DUPLEX_AUTO = LanDuplex(0)
LanDuplex.LAN_DUPLEX_HALF = LanDuplex(1)
LanDuplex.LAN_DUPLEX_FULL = LanDuplex(2)
LanDuplex.LAN_DUPLEX_UNKNOWN = LanDuplex(3)

# structure
class LanLinkMode(Structure):
    idlType = "net.LanLinkMode:1.0.0"
    elements = ["speed", "duplex"]

    def __init__(self, speed, duplex):
        typecheck.is_enum(speed, raritan.rpc.net.LanSpeed, AssertionError)
        typecheck.is_enum(duplex, raritan.rpc.net.LanDuplex, AssertionError)

        self.speed = speed
        self.duplex = duplex

    @classmethod
    def decode(cls, json, agent):
        obj = cls(
            speed = raritan.rpc.net.LanSpeed.decode(json['speed']),
            duplex = raritan.rpc.net.LanDuplex.decode(json['duplex']),
        )
        return obj

    def encode(self):
        json = {}
        json['speed'] = raritan.rpc.net.LanSpeed.encode(self.speed)
        json['duplex'] = raritan.rpc.net.LanDuplex.encode(self.duplex)
        return json

# enumeration
class InterfaceMode(Enumeration):
    idlType = "net.InterfaceMode:2.0.0"
    values = ["IF_MODE_WIRED", "IF_MODE_WIRELESS", "IF_MODE_USB_DEVICE"]

InterfaceMode.IF_MODE_WIRED = InterfaceMode(0)
InterfaceMode.IF_MODE_WIRELESS = InterfaceMode(1)
InterfaceMode.IF_MODE_USB_DEVICE = InterfaceMode(2)

# structure
class InterfaceState(Structure):
    idlType = "net.InterfaceState:2.0.0"
    elements = ["mode", "activeMode", "wirelessSupported"]

    def __init__(self, mode, activeMode, wirelessSupported):
        typecheck.is_enum(mode, raritan.rpc.net.InterfaceMode, AssertionError)
        typecheck.is_enum(activeMode, raritan.rpc.net.InterfaceMode, AssertionError)
        typecheck.is_bool(wirelessSupported, AssertionError)

        self.mode = mode
        self.activeMode = activeMode
        self.wirelessSupported = wirelessSupported

    @classmethod
    def decode(cls, json, agent):
        obj = cls(
            mode = raritan.rpc.net.InterfaceMode.decode(json['mode']),
            activeMode = raritan.rpc.net.InterfaceMode.decode(json['activeMode']),
            wirelessSupported = json['wirelessSupported'],
        )
        return obj

    def encode(self):
        json = {}
        json['mode'] = raritan.rpc.net.InterfaceMode.encode(self.mode)
        json['activeMode'] = raritan.rpc.net.InterfaceMode.encode(self.activeMode)
        json['wirelessSupported'] = self.wirelessSupported
        return json

# structure
class LanInterfaceSettings(Structure):
    idlType = "net.LanInterfaceSettings:1.0.0"
    elements = ["speed", "duplex"]

    def __init__(self, speed, duplex):
        typecheck.is_enum(speed, raritan.rpc.net.LanSpeed, AssertionError)
        typecheck.is_enum(duplex, raritan.rpc.net.LanDuplex, AssertionError)

        self.speed = speed
        self.duplex = duplex

    @classmethod
    def decode(cls, json, agent):
        obj = cls(
            speed = raritan.rpc.net.LanSpeed.decode(json['speed']),
            duplex = raritan.rpc.net.LanDuplex.decode(json['duplex']),
        )
        return obj

    def encode(self):
        json = {}
        json['speed'] = raritan.rpc.net.LanSpeed.encode(self.speed)
        json['duplex'] = raritan.rpc.net.LanDuplex.encode(self.duplex)
        return json

# structure
class LanInterfaceParameters(Structure):
    idlType = "net.LanInterfaceParameters:2.0.0"
    elements = ["speed", "duplex", "autonegotiation", "link", "supportedModes"]

    def __init__(self, speed, duplex, autonegotiation, link, supportedModes):
        typecheck.is_enum(speed, raritan.rpc.net.LanSpeed, AssertionError)
        typecheck.is_enum(duplex, raritan.rpc.net.LanDuplex, AssertionError)
        typecheck.is_bool(autonegotiation, AssertionError)
        typecheck.is_bool(link, AssertionError)
        for x0 in supportedModes:
            typecheck.is_struct(x0, raritan.rpc.net.LanLinkMode, AssertionError)

        self.speed = speed
        self.duplex = duplex
        self.autonegotiation = autonegotiation
        self.link = link
        self.supportedModes = supportedModes

    @classmethod
    def decode(cls, json, agent):
        obj = cls(
            speed = raritan.rpc.net.LanSpeed.decode(json['speed']),
            duplex = raritan.rpc.net.LanDuplex.decode(json['duplex']),
            autonegotiation = json['autonegotiation'],
            link = json['link'],
            supportedModes = [raritan.rpc.net.LanLinkMode.decode(x0, agent) for x0 in json['supportedModes']],
        )
        return obj

    def encode(self):
        json = {}
        json['speed'] = raritan.rpc.net.LanSpeed.encode(self.speed)
        json['duplex'] = raritan.rpc.net.LanDuplex.encode(self.duplex)
        json['autonegotiation'] = self.autonegotiation
        json['link'] = self.link
        json['supportedModes'] = [raritan.rpc.net.LanLinkMode.encode(x0) for x0 in self.supportedModes]
        return json

# enumeration
class AuthenticationMode(Enumeration):
    idlType = "net.AuthenticationMode:1.0.0"
    values = ["AUTH_NONE", "AUTH_PSK", "AUTH_EAP"]

AuthenticationMode.AUTH_NONE = AuthenticationMode(0)
AuthenticationMode.AUTH_PSK = AuthenticationMode(1)
AuthenticationMode.AUTH_EAP = AuthenticationMode(2)

# enumeration
class EapOuterMethod(Enumeration):
    idlType = "net.EapOuterMethod:1.0.0"
    values = ["EAP_PEAP"]

EapOuterMethod.EAP_PEAP = EapOuterMethod(0)

# enumeration
class EapInnerMethod(Enumeration):
    idlType = "net.EapInnerMethod:1.0.0"
    values = ["EAP_MSCHAPv2"]

EapInnerMethod.EAP_MSCHAPv2 = EapInnerMethod(0)

# structure
class EapSettings(Structure):
    idlType = "net.EapSettings:2.0.0"
    elements = ["identity", "password", "outerMethod", "innerMethod", "caCertificate", "forceTrustedCert", "allowOffTimeRangeCerts", "allowNotYetValidCertsIfTimeBeforeBuild"]

    def __init__(self, identity, password, outerMethod, innerMethod, caCertificate, forceTrustedCert, allowOffTimeRangeCerts, allowNotYetValidCertsIfTimeBeforeBuild):
        typecheck.is_string(identity, AssertionError)
        typecheck.is_string(password, AssertionError)
        typecheck.is_enum(outerMethod, raritan.rpc.net.EapOuterMethod, AssertionError)
        typecheck.is_enum(innerMethod, raritan.rpc.net.EapInnerMethod, AssertionError)
        typecheck.is_string(caCertificate, AssertionError)
        typecheck.is_bool(forceTrustedCert, AssertionError)
        typecheck.is_bool(allowOffTimeRangeCerts, AssertionError)
        typecheck.is_bool(allowNotYetValidCertsIfTimeBeforeBuild, AssertionError)

        self.identity = identity
        self.password = password
        self.outerMethod = outerMethod
        self.innerMethod = innerMethod
        self.caCertificate = caCertificate
        self.forceTrustedCert = forceTrustedCert
        self.allowOffTimeRangeCerts = allowOffTimeRangeCerts
        self.allowNotYetValidCertsIfTimeBeforeBuild = allowNotYetValidCertsIfTimeBeforeBuild

    @classmethod
    def decode(cls, json, agent):
        obj = cls(
            identity = json['identity'],
            password = json['password'],
            outerMethod = raritan.rpc.net.EapOuterMethod.decode(json['outerMethod']),
            innerMethod = raritan.rpc.net.EapInnerMethod.decode(json['innerMethod']),
            caCertificate = json['caCertificate'],
            forceTrustedCert = json['forceTrustedCert'],
            allowOffTimeRangeCerts = json['allowOffTimeRangeCerts'],
            allowNotYetValidCertsIfTimeBeforeBuild = json['allowNotYetValidCertsIfTimeBeforeBuild'],
        )
        return obj

    def encode(self):
        json = {}
        json['identity'] = self.identity
        json['password'] = self.password
        json['outerMethod'] = raritan.rpc.net.EapOuterMethod.encode(self.outerMethod)
        json['innerMethod'] = raritan.rpc.net.EapInnerMethod.encode(self.innerMethod)
        json['caCertificate'] = self.caCertificate
        json['forceTrustedCert'] = self.forceTrustedCert
        json['allowOffTimeRangeCerts'] = self.allowOffTimeRangeCerts
        json['allowNotYetValidCertsIfTimeBeforeBuild'] = self.allowNotYetValidCertsIfTimeBeforeBuild
        return json

# structure
class WirelessInterfaceSettings(Structure):
    idlType = "net.WirelessInterfaceSettings:2.0.0"
    elements = ["ssid", "authentication", "psk", "eap", "bssid"]

    def __init__(self, ssid, authentication, psk, eap, bssid):
        typecheck.is_string(ssid, AssertionError)
        typecheck.is_enum(authentication, raritan.rpc.net.AuthenticationMode, AssertionError)
        typecheck.is_string(psk, AssertionError)
        typecheck.is_struct(eap, raritan.rpc.net.EapSettings, AssertionError)
        typecheck.is_string(bssid, AssertionError)

        self.ssid = ssid
        self.authentication = authentication
        self.psk = psk
        self.eap = eap
        self.bssid = bssid

    @classmethod
    def decode(cls, json, agent):
        obj = cls(
            ssid = json['ssid'],
            authentication = raritan.rpc.net.AuthenticationMode.decode(json['authentication']),
            psk = json['psk'],
            eap = raritan.rpc.net.EapSettings.decode(json['eap'], agent),
            bssid = json['bssid'],
        )
        return obj

    def encode(self):
        json = {}
        json['ssid'] = self.ssid
        json['authentication'] = raritan.rpc.net.AuthenticationMode.encode(self.authentication)
        json['psk'] = self.psk
        json['eap'] = raritan.rpc.net.EapSettings.encode(self.eap)
        json['bssid'] = self.bssid
        return json

# interface
class Net(Interface):
    idlType = "net.Net:3.0.0"

    ERR_INVALID_PARAMS = 1

    class _setNetworkConfigIP(Interface.Method):
        name = 'setNetworkConfigIP'

        @staticmethod
        def encode(cfg):
            typecheck.is_struct(cfg, raritan.rpc.net.NetworkConfigIP, AssertionError)
            args = {}
            args['cfg'] = raritan.rpc.net.NetworkConfigIP.encode(cfg)
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = rsp['_ret_']
            typecheck.is_int(_ret_, DecodeException)
            return _ret_

    class _getNetworkConfigIP(Interface.Method):
        name = 'getNetworkConfigIP'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            cfg = raritan.rpc.net.NetworkConfigIP.decode(rsp['cfg'], agent)
            typecheck.is_struct(cfg, raritan.rpc.net.NetworkConfigIP, DecodeException)
            return cfg

    class _setNetworkConfigIPv4(Interface.Method):
        name = 'setNetworkConfigIPv4'

        @staticmethod
        def encode(cfg4):
            typecheck.is_struct(cfg4, raritan.rpc.net.NetworkConfigIPv4, AssertionError)
            args = {}
            args['cfg4'] = raritan.rpc.net.NetworkConfigIPv4.encode(cfg4)
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = rsp['_ret_']
            typecheck.is_int(_ret_, DecodeException)
            return _ret_

    class _getNetworkConfigIPv4(Interface.Method):
        name = 'getNetworkConfigIPv4'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            cfg4 = raritan.rpc.net.NetworkConfigIPv4.decode(rsp['cfg4'], agent)
            cfg4current = raritan.rpc.net.NetworkConfigIPv4.decode(rsp['cfg4current'], agent)
            typecheck.is_struct(cfg4, raritan.rpc.net.NetworkConfigIPv4, DecodeException)
            typecheck.is_struct(cfg4current, raritan.rpc.net.NetworkConfigIPv4, DecodeException)
            return (cfg4, cfg4current)

    class _getNetworkConfigRoutesIPv4(Interface.Method):
        name = 'getNetworkConfigRoutesIPv4'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            static_routes = [raritan.rpc.net.IPv4RoutingEntry.decode(x0, agent) for x0 in rsp['static_routes']]
            active_routes = [raritan.rpc.net.IPv4RoutingEntry.decode(x0, agent) for x0 in rsp['active_routes']]
            for x0 in static_routes:
                typecheck.is_struct(x0, raritan.rpc.net.IPv4RoutingEntry, DecodeException)
            for x0 in active_routes:
                typecheck.is_struct(x0, raritan.rpc.net.IPv4RoutingEntry, DecodeException)
            return (static_routes, active_routes)

    class _setNetworkConfigRoutesIPv4(Interface.Method):
        name = 'setNetworkConfigRoutesIPv4'

        @staticmethod
        def encode(static_routes):
            for x0 in static_routes:
                typecheck.is_struct(x0, raritan.rpc.net.IPv4RoutingEntry, AssertionError)
            args = {}
            args['static_routes'] = [raritan.rpc.net.IPv4RoutingEntry.encode(x0) for x0 in static_routes]
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = rsp['_ret_']
            typecheck.is_int(_ret_, DecodeException)
            return _ret_

    class _getNetworkConfigRoutesIPv6(Interface.Method):
        name = 'getNetworkConfigRoutesIPv6'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            static_routes = [raritan.rpc.net.IPv6RoutingEntry.decode(x0, agent) for x0 in rsp['static_routes']]
            active_routes = [raritan.rpc.net.IPv6RoutingEntry.decode(x0, agent) for x0 in rsp['active_routes']]
            for x0 in static_routes:
                typecheck.is_struct(x0, raritan.rpc.net.IPv6RoutingEntry, DecodeException)
            for x0 in active_routes:
                typecheck.is_struct(x0, raritan.rpc.net.IPv6RoutingEntry, DecodeException)
            return (static_routes, active_routes)

    class _setNetworkConfigRoutesIPv6(Interface.Method):
        name = 'setNetworkConfigRoutesIPv6'

        @staticmethod
        def encode(static_routes):
            for x0 in static_routes:
                typecheck.is_struct(x0, raritan.rpc.net.IPv6RoutingEntry, AssertionError)
            args = {}
            args['static_routes'] = [raritan.rpc.net.IPv6RoutingEntry.encode(x0) for x0 in static_routes]
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = rsp['_ret_']
            typecheck.is_int(_ret_, DecodeException)
            return _ret_

    class _setNetworkConfigIPv6(Interface.Method):
        name = 'setNetworkConfigIPv6'

        @staticmethod
        def encode(cfg6):
            typecheck.is_struct(cfg6, raritan.rpc.net.NetworkConfigIPv6, AssertionError)
            args = {}
            args['cfg6'] = raritan.rpc.net.NetworkConfigIPv6.encode(cfg6)
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = rsp['_ret_']
            typecheck.is_int(_ret_, DecodeException)
            return _ret_

    class _getNetworkConfigIPv6(Interface.Method):
        name = 'getNetworkConfigIPv6'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            cfg6 = raritan.rpc.net.NetworkConfigIPv6.decode(rsp['cfg6'], agent)
            ipv6current = raritan.rpc.net.NetworkActiveValuesIPv6.decode(rsp['ipv6current'], agent)
            typecheck.is_struct(cfg6, raritan.rpc.net.NetworkConfigIPv6, DecodeException)
            typecheck.is_struct(ipv6current, raritan.rpc.net.NetworkActiveValuesIPv6, DecodeException)
            return (cfg6, ipv6current)

    class _setNetworkConfigServices(Interface.Method):
        name = 'setNetworkConfigServices'

        @staticmethod
        def encode(services):
            for x0 in services:
                typecheck.is_struct(x0, raritan.rpc.net.ServiceConfig, AssertionError)
            args = {}
            args['services'] = [raritan.rpc.net.ServiceConfig.encode(x0) for x0 in services]
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = rsp['_ret_']
            typecheck.is_int(_ret_, DecodeException)
            return _ret_

    class _getNetworkConfigServices(Interface.Method):
        name = 'getNetworkConfigServices'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            services = [raritan.rpc.net.ServiceConfig.decode(x0, agent) for x0 in rsp['services']]
            for x0 in services:
                typecheck.is_struct(x0, raritan.rpc.net.ServiceConfig, DecodeException)
            return services

    class _getNetworkConfigInterface(Interface.Method):
        name = 'getNetworkConfigInterface'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            state = raritan.rpc.net.InterfaceState.decode(rsp['state'], agent)
            lan = raritan.rpc.net.LanInterfaceSettings.decode(rsp['lan'], agent)
            lancurrent = raritan.rpc.net.LanInterfaceParameters.decode(rsp['lancurrent'], agent)
            wlan = raritan.rpc.net.WirelessInterfaceSettings.decode(rsp['wlan'], agent)
            typecheck.is_struct(state, raritan.rpc.net.InterfaceState, DecodeException)
            typecheck.is_struct(lan, raritan.rpc.net.LanInterfaceSettings, DecodeException)
            typecheck.is_struct(lancurrent, raritan.rpc.net.LanInterfaceParameters, DecodeException)
            typecheck.is_struct(wlan, raritan.rpc.net.WirelessInterfaceSettings, DecodeException)
            return (state, lan, lancurrent, wlan)

    class _getMACs(Interface.Method):
        name = 'getMACs'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            state = raritan.rpc.net.InterfaceState.decode(rsp['state'], agent)
            ethmac = rsp['ethmac']
            wlanmac = rsp['wlanmac']
            typecheck.is_struct(state, raritan.rpc.net.InterfaceState, DecodeException)
            typecheck.is_string(ethmac, DecodeException)
            typecheck.is_string(wlanmac, DecodeException)
            return (state, ethmac, wlanmac)

    class _setNetworkConfigLan(Interface.Method):
        name = 'setNetworkConfigLan'

        @staticmethod
        def encode(lancfg):
            typecheck.is_struct(lancfg, raritan.rpc.net.LanInterfaceSettings, AssertionError)
            args = {}
            args['lancfg'] = raritan.rpc.net.LanInterfaceSettings.encode(lancfg)
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = rsp['_ret_']
            typecheck.is_int(_ret_, DecodeException)
            return _ret_

    class _setNetworkConfigWLan(Interface.Method):
        name = 'setNetworkConfigWLan'

        @staticmethod
        def encode(wlancfg):
            typecheck.is_struct(wlancfg, raritan.rpc.net.WirelessInterfaceSettings, AssertionError)
            args = {}
            args['wlancfg'] = raritan.rpc.net.WirelessInterfaceSettings.encode(wlancfg)
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = rsp['_ret_']
            typecheck.is_int(_ret_, DecodeException)
            return _ret_

    class _getBridgeSlaveCount(Interface.Method):
        name = 'getBridgeSlaveCount'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = rsp['_ret_']
            typecheck.is_int(_ret_, DecodeException)
            return _ret_
    def __init__(self, target, agent):
        super(Net, self).__init__(target, agent)
        self.setNetworkConfigIP = Net._setNetworkConfigIP(self)
        self.getNetworkConfigIP = Net._getNetworkConfigIP(self)
        self.setNetworkConfigIPv4 = Net._setNetworkConfigIPv4(self)
        self.getNetworkConfigIPv4 = Net._getNetworkConfigIPv4(self)
        self.getNetworkConfigRoutesIPv4 = Net._getNetworkConfigRoutesIPv4(self)
        self.setNetworkConfigRoutesIPv4 = Net._setNetworkConfigRoutesIPv4(self)
        self.getNetworkConfigRoutesIPv6 = Net._getNetworkConfigRoutesIPv6(self)
        self.setNetworkConfigRoutesIPv6 = Net._setNetworkConfigRoutesIPv6(self)
        self.setNetworkConfigIPv6 = Net._setNetworkConfigIPv6(self)
        self.getNetworkConfigIPv6 = Net._getNetworkConfigIPv6(self)
        self.setNetworkConfigServices = Net._setNetworkConfigServices(self)
        self.getNetworkConfigServices = Net._getNetworkConfigServices(self)
        self.getNetworkConfigInterface = Net._getNetworkConfigInterface(self)
        self.getMACs = Net._getMACs(self)
        self.setNetworkConfigLan = Net._setNetworkConfigLan(self)
        self.setNetworkConfigWLan = Net._setNetworkConfigWLan(self)
        self.getBridgeSlaveCount = Net._getBridgeSlaveCount(self)