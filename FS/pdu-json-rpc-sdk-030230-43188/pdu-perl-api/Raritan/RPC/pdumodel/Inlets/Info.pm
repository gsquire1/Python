# Do NOT edit this file!
# It was generated by IdlC from Inlets.idl.

use strict;

package Raritan::RPC::pdumodel::Inlets::Info;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'numberOfInlets'} = 1 * $in->{'numberOfInlets'};
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'numberOfInlets'} = $in->{'numberOfInlets'};
    return $decoded;
}

1;
