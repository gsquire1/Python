# Do NOT edit this file!
# It was generated by IdlC from PowerLogicPowerMeter.idl.

use strict;

package Raritan::RPC::powerlogic::PowerMeter_1_2_3::ErrorStatusChangedEvent;

use constant typeId => "powerlogic.PowerMeter_1_2_3.ErrorStatusChangedEvent:1.0.0";
use Raritan::RPC::idl::Event;
use Raritan::RPC::powerlogic::PowerMeter_1_2_3::ErrorStatus;
use Raritan::RPC::powerlogic::PowerMeter_1_2_3::ErrorStatus;

sub encode {
    my ($in) = @_;
    my $encoded = Raritan::RPC::idl::Event::encode($in);
    $encoded->{'oldStatus'} = Raritan::RPC::powerlogic::PowerMeter_1_2_3::ErrorStatus::encode($in->{'oldStatus'});
    $encoded->{'newStatus'} = Raritan::RPC::powerlogic::PowerMeter_1_2_3::ErrorStatus::encode($in->{'newStatus'});
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = Raritan::RPC::idl::Event::decode($agent, $in);
    $decoded->{'oldStatus'} = Raritan::RPC::powerlogic::PowerMeter_1_2_3::ErrorStatus::decode($agent, $in->{'oldStatus'});
    $decoded->{'newStatus'} = Raritan::RPC::powerlogic::PowerMeter_1_2_3::ErrorStatus::decode($agent, $in->{'newStatus'});
    return $decoded;
}

Raritan::RPC::Registry::registerCodecClass('powerlogic.PowerMeter_1_2_3.ErrorStatusChangedEvent', 1, 0, 0, 'Raritan::RPC::powerlogic::PowerMeter_1_2_3::ErrorStatusChangedEvent');
1;
