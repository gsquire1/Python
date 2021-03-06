# Do NOT edit this file!
# It was generated by IdlC from StorageManager.idl.

use strict;

package Raritan::RPC::webcam::StorageManager::StorageImage;

use Raritan::RPC::webcam::Image_2_0_0;
use Raritan::RPC::webcam::StorageManager::StorageMetaData;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'image'} = Raritan::RPC::webcam::Image_2_0_0::encode($in->{'image'});
    $encoded->{'metaData'} = Raritan::RPC::webcam::StorageManager::StorageMetaData::encode($in->{'metaData'});
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'image'} = Raritan::RPC::webcam::Image_2_0_0::decode($agent, $in->{'image'});
    $decoded->{'metaData'} = Raritan::RPC::webcam::StorageManager::StorageMetaData::decode($agent, $in->{'metaData'});
    return $decoded;
}

1;
