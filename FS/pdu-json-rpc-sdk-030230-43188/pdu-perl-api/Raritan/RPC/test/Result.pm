# Do NOT edit this file!
# It was generated by IdlC from testrpc.idl.

use strict;

package Raritan::RPC::test::Result;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'code'} = 1 * $in->{'code'};
    $encoded->{'errtext'} = "$in->{'errtext'}";
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'code'} = $in->{'code'};
    $decoded->{'errtext'} = $in->{'errtext'};
    return $decoded;
}

1;
