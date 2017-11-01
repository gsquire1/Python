# Do NOT edit this file!
# It was generated by IdlC from AssetStrip.idl.

use strict;

package Raritan::RPC::assetmgrmodel::AssetStrip::LEDColor;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'r'} = 1 * $in->{'r'};
    $encoded->{'g'} = 1 * $in->{'g'};
    $encoded->{'b'} = 1 * $in->{'b'};
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'r'} = $in->{'r'};
    $decoded->{'g'} = $in->{'g'};
    $decoded->{'b'} = $in->{'b'};
    return $decoded;
}

1;