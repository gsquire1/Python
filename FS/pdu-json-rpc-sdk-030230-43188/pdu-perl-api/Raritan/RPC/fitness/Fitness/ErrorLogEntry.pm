# Do NOT edit this file!
# It was generated by IdlC from Fitness.idl.

use strict;

package Raritan::RPC::fitness::Fitness::ErrorLogEntry;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'id'} = "$in->{'id'}";
    $encoded->{'value'} = 1 * $in->{'value'};
    $encoded->{'thresholdValue'} = 1 * $in->{'thresholdValue'};
    $encoded->{'rawValue'} = 1 * $in->{'rawValue'};
    $encoded->{'powerOnHours'} = 1 * $in->{'powerOnHours'};
    $encoded->{'timeStampUTC'} = 1 * $in->{'timeStampUTC'};
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'id'} = $in->{'id'};
    $decoded->{'value'} = $in->{'value'};
    $decoded->{'thresholdValue'} = $in->{'thresholdValue'};
    $decoded->{'rawValue'} = $in->{'rawValue'};
    $decoded->{'powerOnHours'} = $in->{'powerOnHours'};
    $decoded->{'timeStampUTC'} = $in->{'timeStampUTC'};
    return $decoded;
}

1;
