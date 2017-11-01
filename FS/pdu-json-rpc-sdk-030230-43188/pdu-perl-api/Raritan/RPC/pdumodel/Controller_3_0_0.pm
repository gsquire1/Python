# Do NOT edit this file!
# It was generated by IdlC from Controller.idl.

use strict;

package Raritan::RPC::pdumodel::Controller_3_0_0;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "pdumodel.Controller:3.0.0";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::pdumodel::Controller_3_0_0::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}


sub getCommunicationStatus($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getCommunicationStatus', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::pdumodel::CtrlStatistic;

sub getStatistics($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getStatistics', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::pdumodel::CtrlStatistic::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

use Raritan::RPC::pdumodel::Controller_3_0_0::MetaData;

sub getMetaData($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getMetaData', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::pdumodel::Controller_3_0_0::MetaData::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

Raritan::RPC::Registry::registerProxyClass('pdumodel.Controller', 3, 0, 0, 'Raritan::RPC::pdumodel::Controller_3_0_0');
1;