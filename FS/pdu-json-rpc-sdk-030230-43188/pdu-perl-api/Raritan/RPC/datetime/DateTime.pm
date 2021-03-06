# Do NOT edit this file!
# It was generated by IdlC from DateTime.idl.

use strict;

package Raritan::RPC::datetime::DateTime;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "datetime.DateTime:1.0.0";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::datetime::DateTime::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use Raritan::RPC::datetime::DateTime::ZoneInfo;

sub getZoneInfos($$$) {
    my ($self, $zoneInfos, $useOlson) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'useOlson'} = ($useOlson) ? JSON::true : JSON::false;
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getZoneInfos', $args);
    $$zoneInfos = [];
    for (my $i0 = 0; $i0 <= $#{$rsp->{'zoneInfos'}}; $i0++) {
        $$zoneInfos->[$i0] = Raritan::RPC::datetime::DateTime::ZoneInfo::decode($agent, $rsp->{'zoneInfos'}->[$i0]);
    }
}

use Raritan::RPC::datetime::DateTime::NtpCfg;

sub testNtp($$) {
    my ($self, $ntpCfg) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'ntpCfg'} = Raritan::RPC::datetime::DateTime::NtpCfg::encode($ntpCfg);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'testNtp', $args);
    my $_ret_;
    $_ret_ = ($rsp->{'_ret_'}) ? 1 : 0;
    return $_ret_;
}

use Raritan::RPC::datetime::DateTime::Cfg;

sub getCfg($$) {
    my ($self, $cfg) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getCfg', $args);
    $$cfg = Raritan::RPC::datetime::DateTime::Cfg::decode($agent, $rsp->{'cfg'});
}

use Raritan::RPC::datetime::DateTime::Cfg;

sub setCfg($$) {
    my ($self, $cfg) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'cfg'} = Raritan::RPC::datetime::DateTime::Cfg::encode($cfg);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setCfg', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::datetime::DateTime::ZoneInfo;

sub getTime($$$$$$) {
    my ($self, $useOlson, $zone, $dstEnabled, $utcOffset, $currentTime) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'useOlson'} = ($useOlson) ? JSON::true : JSON::false;
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getTime', $args);
    $$zone = Raritan::RPC::datetime::DateTime::ZoneInfo::decode($agent, $rsp->{'zone'});
    $$dstEnabled = ($rsp->{'dstEnabled'}) ? 1 : 0;
    $$utcOffset = $rsp->{'utcOffset'};
    $$currentTime = $rsp->{'currentTime'};
}

Raritan::RPC::Registry::registerProxyClass('datetime.DateTime', 1, 0, 0, 'Raritan::RPC::datetime::DateTime');
1;
