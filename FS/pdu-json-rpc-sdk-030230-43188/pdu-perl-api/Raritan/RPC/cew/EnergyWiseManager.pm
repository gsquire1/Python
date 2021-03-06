# Do NOT edit this file!
# It was generated by IdlC from EnergyWiseManager.idl.

use strict;

package Raritan::RPC::cew::EnergyWiseManager;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "cew.EnergyWiseManager:1.0.0";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::cew::EnergyWiseManager::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use Raritan::RPC::cew::EnergyWiseSettings;

sub getSettings($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getSettings', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::cew::EnergyWiseSettings::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

use Raritan::RPC::cew::EnergyWiseSettings;

sub setSettings($$) {
    my ($self, $settings) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'settings'} = Raritan::RPC::cew::EnergyWiseSettings::encode($settings);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setSettings', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

Raritan::RPC::Registry::registerProxyClass('cew.EnergyWiseManager', 1, 0, 0, 'Raritan::RPC::cew::EnergyWiseManager');
1;
