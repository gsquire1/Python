# Do NOT edit this file!
# It was generated by IdlC from DebugLog.idl.

use strict;

package Raritan::RPC::logging::DebugLog_2_0_0;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "logging.DebugLog:2.0.0";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::logging::DebugLog_2_0_0::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

sub clear($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'clear', $args);
}

use Raritan::RPC::logging::LogInfo;

sub getInfo($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getInfo', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::logging::LogInfo::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

use Raritan::RPC::logging::LogChunk;

sub getChunk($$$$) {
    my ($self, $refId, $count, $direction) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'refId'} = 1 * $refId;
    $args->{'count'} = 1 * $count;
    $args->{'direction'} = $direction;
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getChunk', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::logging::LogChunk::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

Raritan::RPC::Registry::registerProxyClass('logging.DebugLog', 2, 0, 0, 'Raritan::RPC::logging::DebugLog_2_0_0');
1;
