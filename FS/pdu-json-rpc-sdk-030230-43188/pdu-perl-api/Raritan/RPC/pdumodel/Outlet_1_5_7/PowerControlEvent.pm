# Do NOT edit this file!
# It was generated by IdlC from Outlet.idl.

use strict;

package Raritan::RPC::pdumodel::Outlet_1_5_7::PowerControlEvent;

use constant typeId => "pdumodel.Outlet_1_5_7.PowerControlEvent:1.0.0";
use Raritan::RPC::event::UserEvent;

sub encode {
    my ($in) = @_;
    my $encoded = Raritan::RPC::event::UserEvent::encode($in);
    $encoded->{'state'} = $in->{'state'};
    $encoded->{'cycle'} = ($in->{'cycle'}) ? JSON::true : JSON::false;
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = Raritan::RPC::event::UserEvent::decode($agent, $in);
    $decoded->{'state'} = $in->{'state'};
    $decoded->{'cycle'} = ($in->{'cycle'}) ? 1 : 0;
    return $decoded;
}

Raritan::RPC::Registry::registerCodecClass('pdumodel.Outlet_1_5_7.PowerControlEvent', 1, 0, 0, 'Raritan::RPC::pdumodel::Outlet_1_5_7::PowerControlEvent');
1;
