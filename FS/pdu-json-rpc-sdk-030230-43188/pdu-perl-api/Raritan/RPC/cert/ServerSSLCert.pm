# Do NOT edit this file!
# It was generated by IdlC from ServerSSLCert.idl.

use strict;

package Raritan::RPC::cert::ServerSSLCert;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "cert.ServerSSLCert:1.0.0";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::cert::ServerSSLCert::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use Raritan::RPC::cert::ServerSSLCert::ReqInfo;

sub generateUnsignedKeyPair($$$) {
    my ($self, $reqInfo, $challenge) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'reqInfo'} = Raritan::RPC::cert::ServerSSLCert::ReqInfo::encode($reqInfo);
    $args->{'challenge'} = "$challenge";
    my $rsp = $agent->json_rpc($self->{'rid'}, 'generateUnsignedKeyPair', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::cert::ServerSSLCert::ReqInfo;

sub generateSelfSignedKeyPair($$$) {
    my ($self, $reqInfo, $days) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'reqInfo'} = Raritan::RPC::cert::ServerSSLCert::ReqInfo::encode($reqInfo);
    $args->{'days'} = 1 * $days;
    my $rsp = $agent->json_rpc($self->{'rid'}, 'generateSelfSignedKeyPair', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

sub deletePending($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'deletePending', $args);
}

use Raritan::RPC::cert::ServerSSLCert::Info;

sub getInfo($$) {
    my ($self, $info) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getInfo', $args);
    $$info = Raritan::RPC::cert::ServerSSLCert::Info::decode($agent, $rsp->{'info'});
}

sub installPendingKeyPair($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'installPendingKeyPair', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

Raritan::RPC::Registry::registerProxyClass('cert.ServerSSLCert', 1, 0, 0, 'Raritan::RPC::cert::ServerSSLCert');
1;
