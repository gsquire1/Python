# Do NOT edit this file!
# It was generated by IdlC from Modbus.idl.

use strict;

package Raritan::RPC::devsettings::Modbus_2_0_0::Capabilities;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'hasModbusSerial'} = ($in->{'hasModbusSerial'}) ? JSON::true : JSON::false;
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'hasModbusSerial'} = ($in->{'hasModbusSerial'}) ? 1 : 0;
    return $decoded;
}

1;
