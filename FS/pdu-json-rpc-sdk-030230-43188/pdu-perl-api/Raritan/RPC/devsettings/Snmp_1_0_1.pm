# Do NOT edit this file!
# It was generated by IdlC from Snmp.idl.

use strict;

package Raritan::RPC::devsettings::Snmp_1_0_1;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "devsettings.Snmp:1.0.1";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::devsettings::Snmp_1_0_1::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use constant ERR_INVALID_PARAMS => 1;

use Raritan::RPC::devsettings::Snmp_1_0_1::Configuration;

sub getConfiguration($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getConfiguration', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::devsettings::Snmp_1_0_1::Configuration::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

use Raritan::RPC::devsettings::Snmp_1_0_1::Configuration;

sub setConfiguration($$) {
    my ($self, $cfg) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'cfg'} = Raritan::RPC::devsettings::Snmp_1_0_1::Configuration::encode($cfg);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setConfiguration', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

Raritan::RPC::Registry::registerProxyClass('devsettings.Snmp', 1, 0, 1, 'Raritan::RPC::devsettings::Snmp_1_0_1');
1;