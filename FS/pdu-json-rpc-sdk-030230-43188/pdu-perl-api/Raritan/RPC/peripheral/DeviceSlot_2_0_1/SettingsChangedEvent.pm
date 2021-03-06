# Do NOT edit this file!
# It was generated by IdlC from PeripheralDeviceSlot.idl.

use strict;

package Raritan::RPC::peripheral::DeviceSlot_2_0_1::SettingsChangedEvent;

use constant typeId => "peripheral.DeviceSlot_2_0_1.SettingsChangedEvent:1.0.0";
use Raritan::RPC::event::UserEvent;
use Raritan::RPC::peripheral::DeviceSlot_2_0_1::Settings;
use Raritan::RPC::peripheral::DeviceSlot_2_0_1::Settings;

sub encode {
    my ($in) = @_;
    my $encoded = Raritan::RPC::event::UserEvent::encode($in);
    $encoded->{'oldSettings'} = Raritan::RPC::peripheral::DeviceSlot_2_0_1::Settings::encode($in->{'oldSettings'});
    $encoded->{'newSettings'} = Raritan::RPC::peripheral::DeviceSlot_2_0_1::Settings::encode($in->{'newSettings'});
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = Raritan::RPC::event::UserEvent::decode($agent, $in);
    $decoded->{'oldSettings'} = Raritan::RPC::peripheral::DeviceSlot_2_0_1::Settings::decode($agent, $in->{'oldSettings'});
    $decoded->{'newSettings'} = Raritan::RPC::peripheral::DeviceSlot_2_0_1::Settings::decode($agent, $in->{'newSettings'});
    return $decoded;
}

Raritan::RPC::Registry::registerCodecClass('peripheral.DeviceSlot_2_0_1.SettingsChangedEvent', 1, 0, 0, 'Raritan::RPC::peripheral::DeviceSlot_2_0_1::SettingsChangedEvent');
1;
