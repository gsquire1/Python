# Do NOT edit this file!
# It was generated by IdlC from ExternalSensorSlots.idl.

use strict;

package Raritan::RPC::sensors::ExternalSensorSlots::Info;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'count'} = 1 * $in->{'count'};
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'count'} = $in->{'count'};
    return $decoded;
}

1;
