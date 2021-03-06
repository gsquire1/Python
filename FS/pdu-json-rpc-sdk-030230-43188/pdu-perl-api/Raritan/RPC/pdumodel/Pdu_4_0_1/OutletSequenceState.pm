# Do NOT edit this file!
# It was generated by IdlC from Pdu.idl.

use strict;

package Raritan::RPC::pdumodel::Pdu_4_0_1::OutletSequenceState;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'sequenceRunning'} = ($in->{'sequenceRunning'}) ? JSON::true : JSON::false;
    $encoded->{'nextOutletToSwitch'} = 1 * $in->{'nextOutletToSwitch'};
    $encoded->{'timeUntilNextSwitch'} = 1 * $in->{'timeUntilNextSwitch'};
    $encoded->{'outletsRemaining'} = 1 * $in->{'outletsRemaining'};
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'sequenceRunning'} = ($in->{'sequenceRunning'}) ? 1 : 0;
    $decoded->{'nextOutletToSwitch'} = $in->{'nextOutletToSwitch'};
    $decoded->{'timeUntilNextSwitch'} = $in->{'timeUntilNextSwitch'};
    $decoded->{'outletsRemaining'} = $in->{'outletsRemaining'};
    return $decoded;
}

1;
