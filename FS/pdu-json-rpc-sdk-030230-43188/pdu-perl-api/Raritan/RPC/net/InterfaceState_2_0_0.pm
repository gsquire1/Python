# Do NOT edit this file!
# It was generated by IdlC from Net.idl.

use strict;

package Raritan::RPC::net::InterfaceState_2_0_0;


sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'mode'} = $in->{'mode'};
    $encoded->{'activeMode'} = $in->{'activeMode'};
    $encoded->{'wirelessSupported'} = ($in->{'wirelessSupported'}) ? JSON::true : JSON::false;
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'mode'} = $in->{'mode'};
    $decoded->{'activeMode'} = $in->{'activeMode'};
    $decoded->{'wirelessSupported'} = ($in->{'wirelessSupported'}) ? 1 : 0;
    return $decoded;
}

1;