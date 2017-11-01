# Do NOT edit this file!
# It was generated by IdlC from AssetStripLogger.idl.

use strict;

package Raritan::RPC::assetmgrmodel::AssetStripLogger_1_0_4;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "assetmgrmodel.AssetStripLogger:1.0.4";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::assetmgrmodel::AssetStripLogger_1_0_4::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use constant NO_ERROR => 0;

use constant ERR_INVALID_PARAM => 1;

use Raritan::RPC::assetmgrmodel::AssetStripLogger_1_0_4::Info;

sub getInfo($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getInfo', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::assetmgrmodel::AssetStripLogger_1_0_4::Info::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

use Raritan::RPC::assetmgrmodel::AssetStripLogger_1_0_4::Record;

sub getRecords($$$$) {
    my ($self, $records, $id, $count) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'id'} = 1 * $id;
    $args->{'count'} = 1 * $count;
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getRecords', $args);
    $$records = [];
    for (my $i0 = 0; $i0 <= $#{$rsp->{'records'}}; $i0++) {
        $$records->[$i0] = Raritan::RPC::assetmgrmodel::AssetStripLogger_1_0_4::Record::decode($agent, $rsp->{'records'}->[$i0]);
    }
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

Raritan::RPC::Registry::registerProxyClass('assetmgrmodel.AssetStripLogger', 1, 0, 4, 'Raritan::RPC::assetmgrmodel::AssetStripLogger_1_0_4');
1;