# Do NOT edit this file!
# It was generated by IdlC from PeripheralDeviceManager.idl.

use strict;

package Raritan::RPC::peripheral::DeviceManager_2_0_0::PackageRemovedEvent;

use constant typeId => "peripheral.DeviceManager_2_0_0.PackageRemovedEvent:1.0.0";
use Raritan::RPC::peripheral::DeviceManager_2_0_0::PackageEvent;

sub encode {
    my ($in) = @_;
    my $encoded = Raritan::RPC::peripheral::DeviceManager_2_0_0::PackageEvent::encode($in);
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = Raritan::RPC::peripheral::DeviceManager_2_0_0::PackageEvent::decode($agent, $in);
    return $decoded;
}

Raritan::RPC::Registry::registerCodecClass('peripheral.DeviceManager_2_0_0.PackageRemovedEvent', 1, 0, 0, 'Raritan::RPC::peripheral::DeviceManager_2_0_0::PackageRemovedEvent');
1;
