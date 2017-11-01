# Do NOT edit this file!
# It was generated by IdlC from ExternalSensorManager.idl.

use strict;

package Raritan::RPC::sensors::ExternalSensorManager::Settings;


sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'zCoordMode'} = $in->{'zCoordMode'};
    $encoded->{'deviceAltitude'} = 1 * $in->{'deviceAltitude'};
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'zCoordMode'} = $in->{'zCoordMode'};
    $decoded->{'deviceAltitude'} = $in->{'deviceAltitude'};
    return $decoded;
}

1;