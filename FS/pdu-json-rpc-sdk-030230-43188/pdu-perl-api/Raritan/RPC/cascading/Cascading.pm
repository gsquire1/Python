# Do NOT edit this file!
# It was generated by IdlC from Cascading.idl.

use strict;

package Raritan::RPC::cascading::Cascading;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "cascading.Cascading:1.0.0";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::cascading::Cascading::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use constant ERR_NOT_AVAILABLE => 1;

use constant ERR_NOT_SUPPORTED_ON_SLAVE => 2;


sub setType($$) {
    my ($self, $type) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'type'} = $type;
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setType', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}


sub getType($$) {
    my ($self, $type) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getType', $args);
    $$type = $rsp->{'type'};
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

sub getIndex($$) {
    my ($self, $idx) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getIndex', $args);
    $$idx = $rsp->{'idx'};
}

sub getMasterIpAddress($$) {
    my ($self, $masterIpAddress) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getMasterIpAddress', $args);
    $$masterIpAddress = $rsp->{'masterIpAddress'};
}

use Raritan::RPC::cascading::Cascading::ProtocolMapping;

sub getProtocolMappings($$) {
    my ($self, $mappings) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getProtocolMappings', $args);
    $$mappings = [];
    for (my $i0 = 0; $i0 <= $#{$rsp->{'mappings'}}; $i0++) {
        $$mappings->[$i0] = Raritan::RPC::cascading::Cascading::ProtocolMapping::decode($agent, $rsp->{'mappings'}->[$i0]);
    }
}

Raritan::RPC::Registry::registerProxyClass('cascading.Cascading', 1, 0, 0, 'Raritan::RPC::cascading::Cascading');
1;
