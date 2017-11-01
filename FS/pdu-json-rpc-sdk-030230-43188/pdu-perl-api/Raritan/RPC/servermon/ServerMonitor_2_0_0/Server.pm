# Do NOT edit this file!
# It was generated by IdlC from ServerMonitor.idl.

use strict;

package Raritan::RPC::servermon::ServerMonitor_2_0_0::Server;

use Raritan::RPC::servermon::ServerMonitor_2_0_0::ServerSettings;
use Raritan::RPC::servermon::ServerMonitor_2_0_0::ServerStatus;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'settings'} = Raritan::RPC::servermon::ServerMonitor_2_0_0::ServerSettings::encode($in->{'settings'});
    $encoded->{'status'} = Raritan::RPC::servermon::ServerMonitor_2_0_0::ServerStatus::encode($in->{'status'});
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'settings'} = Raritan::RPC::servermon::ServerMonitor_2_0_0::ServerSettings::decode($agent, $in->{'settings'});
    $decoded->{'status'} = Raritan::RPC::servermon::ServerMonitor_2_0_0::ServerStatus::decode($agent, $in->{'status'});
    return $decoded;
}

1;