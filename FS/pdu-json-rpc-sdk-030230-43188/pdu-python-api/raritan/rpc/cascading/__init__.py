# Do NOT edit this file!
# It was generated by IdlC class idl.json.python.ProxyAsnVisitor.

#
# Section generated from "/home/nb/builds/MEGA/px2-3.2.30-3.2.39-branch-20160511-none-release-none-pdu-raritan/fwcomponents/mkdist/tmp/px2_final/libisys/src/idl/Cascading.idl"
#

import raritan.rpc
from raritan.rpc import Interface, Structure, ValueObject, Enumeration, typecheck, DecodeException
import raritan.rpc.cascading


# interface
class Cascading(Interface):
    idlType = "cascading.Cascading:1.0.1"

    ERR_NOT_AVAILABLE = 1

    ERR_NOT_SUPPORTED_ON_SLAVE = 2

    # enumeration
    class Type(Enumeration):
        idlType = "cascading.Cascading_1_0_1.Type:1.0.0"
        values = ["USB_MULTI_IP", "USB_SINGLE_IP_NAT"]

    Type.USB_MULTI_IP = Type(0)
    Type.USB_SINGLE_IP_NAT = Type(1)

    # structure
    class ProtocolMapping(Structure):
        idlType = "cascading.Cascading_1_0_1.ProtocolMapping:1.0.0"
        elements = ["appProtoId", "appProtoName", "transportProtoName"]

        def __init__(self, appProtoId, appProtoName, transportProtoName):
            typecheck.is_int(appProtoId, AssertionError)
            typecheck.is_string(appProtoName, AssertionError)
            typecheck.is_string(transportProtoName, AssertionError)

            self.appProtoId = appProtoId
            self.appProtoName = appProtoName
            self.transportProtoName = transportProtoName

        @classmethod
        def decode(cls, json, agent):
            obj = cls(
                appProtoId = json['appProtoId'],
                appProtoName = json['appProtoName'],
                transportProtoName = json['transportProtoName'],
            )
            return obj

        def encode(self):
            json = {}
            json['appProtoId'] = self.appProtoId
            json['appProtoName'] = self.appProtoName
            json['transportProtoName'] = self.transportProtoName
            return json

    class _setType(Interface.Method):
        name = 'setType'

        @staticmethod
        def encode(type):
            typecheck.is_enum(type, raritan.rpc.cascading.Cascading.Type, AssertionError)
            args = {}
            args['type'] = raritan.rpc.cascading.Cascading.Type.encode(type)
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = rsp['_ret_']
            typecheck.is_int(_ret_, DecodeException)
            return _ret_

    class _getType(Interface.Method):
        name = 'getType'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = rsp['_ret_']
            type = raritan.rpc.cascading.Cascading.Type.decode(rsp['type'])
            typecheck.is_int(_ret_, DecodeException)
            typecheck.is_enum(type, raritan.rpc.cascading.Cascading.Type, DecodeException)
            return (_ret_, type)

    class _getIndex(Interface.Method):
        name = 'getIndex'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            idx = rsp['idx']
            typecheck.is_int(idx, DecodeException)
            return idx

    class _getMasterIpAddress(Interface.Method):
        name = 'getMasterIpAddress'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            masterIpAddress = rsp['masterIpAddress']
            typecheck.is_string(masterIpAddress, DecodeException)
            return masterIpAddress

    class _getMasterIpV6Address(Interface.Method):
        name = 'getMasterIpV6Address'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            masterIpV6Address = rsp['masterIpV6Address']
            typecheck.is_string(masterIpV6Address, DecodeException)
            return masterIpV6Address

    class _getProtocolMappings(Interface.Method):
        name = 'getProtocolMappings'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            mappings = [raritan.rpc.cascading.Cascading.ProtocolMapping.decode(x0, agent) for x0 in rsp['mappings']]
            for x0 in mappings:
                typecheck.is_struct(x0, raritan.rpc.cascading.Cascading.ProtocolMapping, DecodeException)
            return mappings
    def __init__(self, target, agent):
        super(Cascading, self).__init__(target, agent)
        self.setType = Cascading._setType(self)
        self.getType = Cascading._getType(self)
        self.getIndex = Cascading._getIndex(self)
        self.getMasterIpAddress = Cascading._getMasterIpAddress(self)
        self.getMasterIpV6Address = Cascading._getMasterIpV6Address(self)
        self.getProtocolMappings = Cascading._getProtocolMappings(self)
