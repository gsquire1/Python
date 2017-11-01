# Do NOT edit this file!
# It was generated by IdlC from Log.idl.

use strict;

package Raritan::RPC::logging::LogEntry;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'id'} = 1 * $in->{'id'};
    $encoded->{'timestamp'} = 1 * $in->{'timestamp'};
    $encoded->{'eventClass'} = "$in->{'eventClass'}";
    $encoded->{'message'} = "$in->{'message'}";
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'id'} = $in->{'id'};
    $decoded->{'timestamp'} = $in->{'timestamp'};
    $decoded->{'eventClass'} = $in->{'eventClass'};
    $decoded->{'message'} = $in->{'message'};
    return $decoded;
}

1;