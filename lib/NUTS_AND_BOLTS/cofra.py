#!/usr/bin/env python3


import datetime
import sys
import anturlar
import re
import liabhar
import csv
import os



class doFirmwareDownload():
    """
        do a firmware download to 7.3.0 build of  firmware
        then close the telnet connection and
        wait 1200 seconds before closing ending the function
        Return could be
                1. a message that firmware version are the same
                2. server is inaccessible
                3. the user prompt after firmware download is started
    """
    def __init__(self, firmvrsn ):
        self.firmvrsn = firmvrsn
        self.start()
    
    def check_status(self):
        capture_cmd = anturlar.fos_cmd("firmwaredownloadstatus")
        if "firmware versions" in capture_cmd:
            return("1")
        else:
            liabhar.count_down(30)
            self.check_status()
            
    def check_version(self):
         
        capture_cmd = anturlar.fos_cmd("firmwareshow") 
        ras = re.compile('FOS\s+([\._a-z0-9]{6,18})\\r\\n\s+([\._a-z0-9]{6,18})')
        ras = re.compile('FOS\s+([\._a-z0-9]{6,18})\\r\\n\s+([\._a-z0-9]{6,18})')
        ras_dir = re.compile('[ 0-9CPFOS]{19}\s+([\._a-z0-9]{6,18})\s+\w+\\r\\n\s+([\._a-z0-9]{6,18})')
        ras = ras.search(capture_cmd)
        ras_dir = ras_dir.search(capture_cmd)
        f=""
        try:
            if ras.group(0) != "none":
                f= ras.group(1)
        except:
            pass
        try:
            if ras_dir(0) != "none":
                f=ras_dir.group(1)
        except:
            pass
        
        return(f)

    def start(self):
        ras = self.check_version()
        #print("FIRMUP IS %s\n"%(self.firmup))
        #print("RAS IS     %s\n"%(ras))
        if ras != self.firmvrsn:
            firmware_cmd = "firmwaredownload -sfbp scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.4.0/%s,fwdlacct"%(self.firmvrsn)
        else:
            return "fail to perform Firmwaredownload since versions were the same"
            #firmware_cmd = "firmwaredownload -sfbp scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.2.1/%s,fwdlacct"%(self.firmdown)
        reg_ex_list = [b'root> ', b'Y/N\) \[Y]:', b'HA Rebooting', b'Connection to host lost.']
        capture_own_regex = anturlar.fos_cmd_regex(firmware_cmd, reg_ex_list)
        if "the same firmware" in capture_own_regex:
            return(capture_own_regex)
        if "server is inaccessible" in capture_own_regex:
            return(capture_own_regex)
        
        capture_cmd = anturlar.fos_cmd("Y")
        close_tel()
        liabhar.email_sender_html("smckie@brocade.com", "smckie@brocade.com", "Started Firmware Download ", "%s"%(self.firmvrsn))
        liabhar.count_down(1200) 
        return(capture_cmd)
###############################################################################

class DoSupportsave():
    """
    start a supportsave on the current switch
    the ip user password chassisname and if to do tracedump (default yes)
        
    """
    def __init__(self, ip, user, passw, chas_name, tr = 'yes'):
        self.tr = tr
        self.ip = ip
        self.user = user
        self.passw = passw
        self.chas_name = chas_name
        self.dirname = ""
        self.createdir()
        self.start()
        
    def start(self):
        """
         doc here
        """
        
        self.tracedump()
        
        capture = ""
        reg_ex_list = [b'root> ', b'.*\r\n']
        reg_ex_list = [b'root>', b'please retry later', b'SupportSave complete', b'Supportsave failed.']
        cmd = "supportsave -n -u %s -p %s -h %s -l ftp -d %s" % (self.user, self.passw, self.ip, self.dirname)
        reg_ex_list_only_root = [b'(.*\d\\r\\n )']
        reg_ex_list_only_cmd = [ cmd.encode()]
        print(cmd)
        cmd_cap = anturlar.fos_cmd(cmd)
        #tn.write(cmd.encode('ascii') + b"\n")
        #capture = tn.expect(reg_ex_list_only_cmd, 10)
        #capture = tn.expect(reg_ex_list, 3600)
        #capture = capture[2]
        #capture = capture.decode()
        print( cmd_cap )
    
    def tracedump(self):
        if self.tr == "yes":
            capture_cmd = anturlar.fos_cmd("tracedump -n")
            capture_cmd = anturlar.fos_cmd("")
         
    def createdir(self):
        global tn
        i = str(datetime.datetime.today())  #### ISO format 2013-02-21 06:35:45.707450
        print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii\n")
        print(i)
        d = [" ", "-", ":", "."]
        for k in d:
            print(k)
            i = i.replace(k, "_")
         
        print("\niiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii\n")
        print(i)
        self.dirname = self.chas_name
        self.dirname += "__"
        self.dirname += i
        print("new directory name\n")
        print(self.dirname)
        print("\niiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii\n")
            
        #reg_ex_list_ftp = [b'root\):', b'none\)\):']
        reg_ex_list_ftp = [b'root\):', b'none\)\):']
        cmd = "ftp "
        cmd += self.ip
        cmd_cap = anturlar.fos_cmd_regex(cmd, reg_ex_list_ftp)
        
        #tn.write(cmd.encode('ascii') + b"\n")
        #capture = tn.expect(reg_ex_list_ftp, 10)
        print(cmd_cap)
        reg_ex_list_ftp = [b'assword:']
        cmd = self.user
        cmd_cap = anturlar.fos_cmd_regex(cmd, reg_ex_list_ftp)
        
        #tn.write(cmd.encode('ascii') + b"\n")
        #capture = tn.expect(reg_ex_list_ftp, 10)
        print(cmd_cap)
        
        reg_ex_list_ftp = [b'ftp> ']
        cmd = self.passw
        cmd_cap = anturlar.fos_cmd_regex(cmd, reg_ex_list_ftp)
        #tn.write(cmd.encode('ascii') + b"\n")
        #capture = tn.expect(reg_ex_list_ftp, 10)
        print(cmd_cap)
     
        reg_ex_list_ftp = [b'ftp', b'denied ', b'timeout']
        cmd = "mkdir "
        cmd += self.dirname
        cmd_cap = anturlar.fos_cmd_regex(cmd, reg_ex_list_ftp)
        #tn.write(cmd.encode('ascii') + b"\n")
        #capture = tn.expect(reg_ex_list_ftp, 10)
        print(cmd_cap)
        
        reg_ex_list_ftp = [b'ftp', b'denied ', b'timeout']
        cmd = "exit"
        cmd_cap = anturlar.fos_cmd_regex(cmd, reg_ex_list_ftp)
        #tn.write(cmd.encode('ascii') + b"\n")
        #capture = tn.expect(reg_ex_list_ftp, 10)
        print(cmd_cap)
        
        return 0
###############################################################################

class DoFirmwaredownloadChoice():
    """
        do a firmware download to 7.3.x or 7.2.1 builds depending on what
        is already on the switch
        
    """
    def __init__(self, firmdown, firmup):
        self.firmdown = firmdown
        self.firmup = firmup
        #self.check_version()
        self.start()
        
    
    def check_status(self):
        capture_cmd = anturlar.fos_cmd("firmwaredownloadstatus")
        if "firmware versions" in capture_cmd:
            return("1")
        else:
            liabhar.count_down(30)
            self.check_status()
               
    def check_version(self):
         
        capture_cmd = anturlar.fos_cmd("firmwareshow") 
        ras = re.compile('FOS\s+([\._a-z0-9]{6,18})\\r\\n\s+([\._a-z0-9]{6,18})')
        ras = re.compile('FOS\s+([\._a-z0-9]{6,18})\\r\\n\s+([\._a-z0-9]{6,18})')
        ras_dir = re.compile('[ 0-9CPFOS]{19}\s+([\._a-z0-9]{6,18})\s+\w+[\\r\\n]*\s+([\._a-z0-9]{6,18})')
        ras = ras.search(capture_cmd)
        ras_dir = ras_dir.search(capture_cmd)
        
        f=""
        capture_cmd = anturlar.fos_cmd("hashow")
        if "hashow: Not supported" in capture_cmd:
            f = ras.group(1)
        else:
            f = ras_dir.group(1)
        
        
        #print("switch RAS is :  %s  " % ras.group(1))
        #print("director RAS is  : %s " % ras_dir.group(1))
        
        #try:
        #    if ras_dir(0) != "none":
        #        f=ras_dir.group(1)
        #except:
        #    pass
  
        return(f)
          
    def start(self):
        ras = self.check_version()
        download_success = False
        print("\n\nFIRMUP IS %s\n"%(self.firmup))
        print("RAS IS     %s\n"%(ras))
        if ras != self.firmup:
            #firmware_cmd = "firmwaredownload -sfbp scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.3.0/%s,fwdlacct"%(self.firmup)
            firmware_cmd = "firmwaredownload -p scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.3.0/%s,fwdlacct"%(self.firmup)
        else:
            #firmware_cmd = "firmwaredownload -sfbp scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.2.1/%s,fwdlacct"%(self.firmdown)
            firmware_cmd = "firmwaredownload -p scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.2.1/%s,fwdlacct"%(self.firmdown)
        reg_ex_list = [b'root> ', b'Y/N\) \[Y]:', b'HA Rebooting', b'Connection to host lost.', \
                       b'with new firmware', b'Firmware has been downloaded']
        
        #capture_own_regex = anturlar.fos_cmd_regex(firmware_cmd, reg_ex_list)
        print("\n\nstart firmwaredownload")
        capture_own_regex = anturlar.fos_cmd_regex(firmware_cmd, reg_ex_list, 9)
        
        if "Y]:" in capture_own_regex:
            
            print("\n\n\nsending yes \n\n\n\n")
            capture_cmd = anturlar.fos_cmd_regex("Y", reg_ex_list, 9)
            download_success = True
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            #print(capture_cmd)
            print("END OF SEND Y \n\n\n\n\n\n")
            anturlar.close_tel()
            liabhar.count_down(1800) 
            return(capture_cmd)
        
        #### does  capture_cmd include ha rebooting ???
        #if "HA Rebooting" in capture_cmd:
        #    print("\n\n\n")
        #    return(capture_cmd)
        #
        #if "with new firmware" in capture_cmd:
        #    return(capture_cmd)
        #
        #if "Firmware has been downloaded" in capture_cmd:
        #    return(capture_cmd)

        #######################################################################   
        #######################################################################
        ####
        #### port decommission  -- need to delete decom action in all FIDS
        ####         -- mapsconfig --actions raslog,email
        #### FPI monitor        -- need to disable FPI monitor in all FIDS
        ####         -- mapsconfig --disableFPImon
        #### discard frame logging --
        ####         -- framelog --disable -type du  and -type unroute
        #### SIM ports configured --
        ####         -- flow --control -simport [port] -disable 
        ####
        
        ####
        ####  if "root>" in capture_cmd_regex:
        ####
        capture_cmd = anturlar.fos_cmd("lscfg --show", 9)
        ras = re.compile('(\d{1,3})(?=\()')  
        ls_all = ras.findall(capture_cmd)
        
        message_check = ""
        if "the same firmware" in capture_own_regex:
            message_check = "Firmwaredownload failed"
        if "server is inaccessible" in capture_own_regex:
            message_check = "Firmwaredownload failed"
        
        if "Downgrade is not allowed" in capture_own_regex:
            pass
            #message_check = "failed"
        if "Firmwaredownload is already running" in capture_own_regex:
            pass
        if "Sanity check failed because system is non-redundant" in capture_own_regex:
            pass
        
        
        if "port decommission" in capture_own_regex:
            for l in ls_all:
                capture_cmd = anturlar.fos_cmd("setcontext %s " % l)
                capture_cmd = anturlar.fos_cmd("mapsconfig --actions raslog,email")
        
        if "FPI Monitor" in capture_own_regex:
            for l in ls_all:
                capture_cmd = anturlar.fos_cmd("setcontext %s " % l)
                capture_cmd = anturlar.fos_cmd("mapsconfig --disableFPImon")
            
        if "discard frame logging" in capture_own_regex:
            for l in ls_all:
                capture_cmd = anturlar.fos_cmd("setcontext %s " % l)
                capture_cmd = anturlar.fos_cmd("framelog --disable -type du")
                capture_cmd = anturlar.fos_cmd("framelog --disable -type unroute")
             
        if "SIM ports configured" in capture_own_regex:
            en = anturlar.SwitchInfo()
            #port_list = en.sim_ports()
            
            for l in ls_all:
                anturlar.fos_cmd("setcontext %s " % l)
                port_list = en.sim_ports()
                anturlar.fos_cmd("flow --control -portIdMode slotport")
                print("port list is \n")
                print(port_list)
                
                for p in port_list:
                    capture_cmd = anturlar.fos_cmd("flow --control -simport %s/%s -disable" % (p[0],p[1]) )
            
                anturlar.fos_cmd("flow --control -portIdMode index")
            #capture_cmd = anturlar.fos_cmd_regex("N", reg_ex_list)
            #message_check = "Firmwaredownload failed"
        
        ##if "SIM ports configured" in capture_own_regex:
        ##    message_check = "Firmwaredownload failed"
        
        if "Brocade FC16-64 blades" in capture_own_regex:
            message_check = "failed"
        
        
        
        if "failed" in message_check:
            print("\n\ndo you want to stop the test ?")
            print(message_check)
            sys.exit()
            #return(message_check)
        
        liabhar.count_down(20)
        capture_cmd = anturlar.fos_cmd_regex("Y", reg_ex_list)
        #anturlar.close_tel()
        
        liabhar.email_sender_html("smckie@brocade.com", "smckie@brocade.com", "Started Firmware Download ", "%s %s"%(self.firmdown, self.firmup))
        liabhar.count_down(1800) 
        return(capture_cmd)
###############################################################################

class SwitchUpdate():
    """
    Grab switch info needed for a complete rebuild. This includes ?????????
    
    """
    global tn
    def __init__(self, ip):
        self.ip = ip
        
    def playback_licenses_to_switch(self):
        """
        Replay Licenses back to switch. The ""Switch_Info_for_playback_",switch_ip,".txt" ""
        must already be written and available in logs/ file.
        """
        
        si = anturlar.SwitchInfo()
        cs = anturlar.configSwitch()
        switch_ip = si.ipaddress()
    
        f = ("%s%s%s"%("logs/Switch_Info_for_playback_",switch_ip,".txt"))
        try:
            with open(f, 'r') as file:
                a = file.read()
        except IOError:
            print("\n\nThere was a problem opening the file:" , f)
            sys.exit()
        ras = re.findall('LICENSE LIST\s+:\s+\[(.+)\]', a)
        b = ras[0]
        c = b.split(",")
        for i in c:
            anturlar.fos_cmd("licenseadd %s" % i)
        a = cs.reboot()
        if a != "Online":
            anturlar.fos_cmd("switchenable")    
        anturlar.fos_cmd('licenseshow')
        return(True)
    
    def reboot(self):
        host = sys.argv[1]
        user = sys.argv[2]
        password = sys.argv[7]
        fos_cmd("echo Y | reboot")
        liabhar.count_down(120)
        connect_tel_noparse(host, user, password)
        liabhar.count_down(10)
        state = SwitchInfo.switch_state(self)
        return(state)

    
    
    
###############################################################################
def bladeportmap_Info(blade = 0):
    """
    bladeportmap_Info
    
    """
    capture_cmd = anturlar.fos_cmd("bladeportmap %s " % blade)
 
    ras = re.compile('ENB\s(\d+)\s+([-\d]+)\s+([-\d]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([-\d]+)\s+(\d+)\s+([CONDOR324]+)\s+([:_/A-Za-z0-9]+)')
    ras = ras.findall(capture_cmd)
    
    
    return(ras)
###############################################################################

def clear_stats():
    """
        clear the following stats on a switch
        fcrlogclear     errclear    diagclearerror -all     tracedump -R
        supportsave -R  statsclear  portlogclear        coreshow -R
        slotstatsclear    fabstatsclear   history clear
        
    """
    switch_info = anturlar.fos_cmd("")
    switch_info = anturlar.fos_cmd("fcrlogclear")
    switch_info = anturlar.fos_cmd("supportsave -R")
    switch_info = anturlar.fos_cmd("errclear")
    switch_info = anturlar.fos_cmd("statsclear")
    switch_info = anturlar.fos_cmd("portlogclear")
    switch_info = anturlar.fos_cmd("diagclearerror -all")
    switch_info = anturlar.fos_cmd("tracedump -R")
    switch_info = anturlar.fos_cmd("coreshow -R")
    switch_info = anturlar.fos_cmd("slotstatsclear")
    switch_info = anturlar.fos_cmd("fabstatsclear")
    switch_info = anturlar.fos_cmd("history -c")
###############################################################################
   
def PortStats(counter="all", port_list = "all"):
    """
    PortStats Values
        los         --  Loss of Sync 
        lol         --  Link Failure
        losig       --  Loss of Signal
        swtxto      --  switch tx timeout
        swrxto      --  switch rx timeout
        proto       --  protocal error
        crc         --  crc with g_eof
        lrout       --  link reset out
        lrin        --  link reset in
        encout      --  encoding out error
        encin       --  encoding in error
        c3to        --  c3 timeout discard
        pcserr      --  pcs error ( ITW errors )
        statechange --  statechange
        txcrd_zero  --  Port TX credit zero
        
        A list of all the Port Stats Values will be return by default
        or the counter value can be passed from the list above
        the port_list will return all ports unless pass 
        
    """
    
    #### set the list of counters to get for each port
    if "all" in counter:
        counter_list = ['los', 'lol', 'losig', 'swtxto', 'swrxto', 'proto',\
                        'crc', 'lrout', 'lrin', 'encout', 'encin',\
                        'c3to', 'pcserr', 'statechange' ]
    else:
        counter_list = counter
        
    port_list = 2
    counter_list_capture = []
    
    los_count        = ["los"]
    lol_count        = ["lol"]
    losig_count      = ["losig"]
    c3to_tx_count    = ['swtxto']
    c3to_rx_count    = ['swrxto']
    c3_discard_count = ['c3to']
    proto_count      = ['proto']
    crc_geof_count   = ['crc']
    lr_out_count     = ['lrout']
    lr_in_count      = ['lrin']
    enc_out_count    = ['encout']
    enc_in_count     = ['encin']
    pcserr_count     = ['pcserr']
    st_change_count  = ['statechange']

    #### send the command portshow and capture the data for each counter
    ####
    capture_cmd = anturlar.fos_cmd("portshow %s " % port_list)
    
    ras_intr_link_fail    = re.compile('Interrupts:\s+(\d+)\s+Link_failure:\s+(\d+)')
    ras_intr_link_fail    = ras_intr_link_fail.findall(capture_cmd)
    ras_unknown_loss_sync = re.compile('Unknown:\s+(\d+)\s+Loss_of_sync:\s+(\d+)')
    ras_unknown_loss_sync = ras_unknown_loss_sync.findall(capture_cmd)
    ras_Lli_loss_signal   = re.compile('Lli:\s+(\d+)\s+Loss_of_sig:\s+(\d+)')
    ras_Lli_loss_signal   = ras_Lli_loss_signal.findall(capture_cmd)
    ras_proc_protoc_err   = re.compile('Proc_rqrd:\s+(\d+)\s+Protocol_err:\s+(\d+)')
    ras_proc_protoc_err   = ras_proc_protoc_err.findall(capture_cmd)
    ras_Suspend_lr_out    = re.compile('Suspended:\s+(\d+)\s+Lr_out:\s+(\d+)')
    ras_Suspend_lr_out    = ras_Suspend_lr_out.findall(capture_cmd)
    ras_Overrun_lr_in     = re.compile('Overrun:\s+(\d+)\s+Lr_in:\s+(\d+)')
    ras_Overrun_lr_in     = ras_Overrun_lr_in.findall(capture_cmd)
    ras_state_change      = re.compile('state transition count:\s+(\d+)')
    ras_state_change      = ras_state_change.findall(capture_cmd)
    
    
    #### send the command porterrshow and capture the data for each counter
    #### 
    caputre_porterrshow = anturlar.fos_cmd("porterrshow %s | grep :" % port_list)
    ras_porterrshow = re.compile('\s*\d+:\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)\s+([\.\dkgmt]+)')
    ras_porterrshow = ras_porterrshow.findall(caputre_porterrshow)
        
    
    for i in counter_list:
        
        print("\nvalue of i is  %s " % i)      
        #### start of portshow command 
        
        if i == 'lol' :
            los_count.append(ras_intr_link_fail[0][1])
            counter_list_capture.append(los_count)

        elif i == 'los':
            lol_count.append(ras_unknown_loss_sync[0][1])
            counter_list_capture.append(lol_count)

        elif i == 'losig':
            losig_count.append(ras_Lli_loss_signal[0][1])
            counter_list_capture.append(losig_count)
                
        elif i in 'proto':
            proto_count.append(ras_proc_protoc_err[0][1])
            counter_list_capture.append(proto_count)           
            
        elif i in "lrout":
            lr_out_count.append(ras_Suspend_lr_out[0][1])
            counter_list_capture.append(lr_out_count)
            
        elif i in "lrin":
            lr_in_count.append(ras_Overrun_lr_in[0][1])
            counter_list_capture.append(lr_in_count)
            
        elif i =='statechange':
            st_change_count.append(ras_state_change[0])
            counter_list_capture.append(st_change_count)
        
        ####  start of porterrshow command
        
        elif i == 'crc':
            crc_geof_count.append(ras_porterrshow[0][4])
            counter_list_capture.append(crc_geof_count)
        
        elif i == 'swtxto':
            c3to_tx_count.append(ras_porterrshow[0][15])
            counter_list_capture.append(c3to_tx_count)
        
        elif i == 'swrxto':
            c3to_rx_count.append(ras_porterrshow[0][16])
            counter_list_capture.append(c3to_rx_count)
            
        elif i == 'c3to':
            c3_discard_count.append(ras_porterrshow[0][9])
            counter_list_capture.append(c3_discard_count)
        
        elif i in 'encin':
            enc_in_count.append(ras_porterrshow[0][2])
            counter_list_capture.append(enc_in_count)
            
        elif i in 'encout':
            enc_out_count.append(ras_porterrshow[0][8])
            counter_list_capture.append(enc_out_count)
        
        elif i in 'pcserr':
            pcserr_count.append(ras_porterrshow[0][17])
            counter_list_capture.append(pcserr_count)
        
        else:
            pass
            
    return(counter_list_capture)
###############################################################################

def ha_failover( times=2):
    """
        do HA failover on directors
        do hareboot on pizza box
    """
    #### steps
    ####  1. Determine Pizza box or Director
    ####  2. save username and password
    ####  3. HA Failover 
    ####  4. wait some time
    ####  5. reconnect
    ####  6. 
    ####   
    sw_info = anturlar.SwitchInfo()
    fid_now = sw_info.ls_now()
    ip_addr = sw_info.ipaddress()
    go_or_not = sw_info.synchronized()
    cons_out = anturlar.fos_cmd(" ")
    username = 'root'
    pwrd = 'password'
    #counter = 1
    new_connect = True
    ####  add error checking here
    ####   the first step is to get original data before starting the test
    #print("\n\noutside the while loop the go or not is equal to %s  " % go_or_not)
    liabhar.count_down(10)
    
    while new_connect:
        
        try:
            
            while times > 0:
                print("\n\n\n")
                print("@"*60)
                print("HA Failovers remaining -- %s " % times)
                print("@"*60)
                anturlar.connect_tel_noparse(ip_addr,'root','password')
                liabhar.count_down(60)
                sw_info = anturlar.SwitchInfo()
                while sw_info.synchronized() is False:
                    liabhar.count_down(360)
                                
                sw_info = anturlar.fos_cmd("echo Y | hafailover")
                ####  add error checking here
                ####   get the same data as before the while loop and compare
                if "can't failover" in sw_info:
                    print("\n\n\nSwitch Not Ready")
                    print("Need to wait for LS/HA progress to complete\n\n")
                    liabhar.count_down(300)
                else:
                    times -= 1
                #liabhar.count_down(30)
        
        except:
        #except SocketError as e:
            #if e.errno != errno.ECONNRESET:
                #print("\n\n\nCONNECTION ERROR TRYING TO RECONNECT\n\n\n")
                #raise 
            print("===============================")
            print("Telnet was disconnected ")
            print("Attempting to reconnect shortly \n")
            print("===============================")
            liabhar.count_down(60)
        if times == 0:
            new_connect = False   
     
    liabhar.count_down(300)

    return()
###############################################################################

def ha_failover_check_adjacent( adjacent_ipaddr, times=2, wait=300):
    """
        do HA failover on directors 
        do hareboot on pizza box - # still to be implimented
    """
    #### steps
    ####  1. Determine Pizza box or Director
    ####  2. save username and password
    ####  3. HA Failover 
    ####  4. wait some time
    ####  5. reconnect
    ####  6. 
    ####   
    sw_info = anturlar.SwitchInfo()
    fid_now = sw_info.ls_now()
    ip_addr = sw_info.ipaddress()
    go_or_not = sw_info.synchronized()
    cons_out = anturlar.fos_cmd(" ")
    username = 'root'
    pwrd = 'password'
    counter = 1
    new_connect = True
    ####  add error checking here
    ####   the first step is to get original data before starting the test
    
    liabhar.count_down(10)
    
    while new_connect:
        
        try:
            
            while times > 0:
                print("@"*60)
                print("HA Failovers Remaining  --  %s " % times)
                print("@"*60)
                
                anturlar.connect_tel_noparse(ip_addr,'root','password')
                sw_info = anturlar.SwitchInfo()
                    
                sw_info = anturlar.fos_cmd("echo Y | hafailover")
                ####  add error checking here
                ####   get the same data as before the while loop and compare
                
                if "can't failover" in sw_info:
                    print("\n\n\nSwitch Not Ready")
                    print("Need to wait for LS/HA progress to complete\n\n")
                    liabhar.count_down(300)
                else:
                    times -= 1
                    
                liabhar.count_down(wait)
        
        except:
        #except SocketError as e:
            #if e.errno != errno.ECONNRESET:
                #print("\n\n\nCONNECTION ERROR TRYING TO RECONNECT\n\n\n")
                #raise 
            print("===============================")
            print("Telnet was disconnected ")
            print("Attempting to reconnect shortly \n")
            print("===============================")
            #pass
            #liabhar.count_down(10)
        if times == 0:
            new_connect = False   
     
     
        anturlar.connect_tel_noparse(adjacent_ipaddr,'root','password')
        sw_info = anturlar.SwitchInfo()
        sw_info = anturlar.fos_cmd("switchshow")
        sw_info = anturlar.fos_cmd("coreshow")
        if "panic" in sw_info:
            sys.exit()
        anturlar.close_tel()

    liabhar.count_down(300)
    return()
###############################################################################

def fids_check(self, fid, lscfgshow): 
        """
            Check if FID given is resident on switch.
        """
        self.fid = fid
        self.lscfgshow = lscfgshow
        #print("\n\n\nChecking if FID %s is a valid FID on switch.\n\n\n " % fid)
        fids = re.findall('(\d{1,3})\(', lscfgshow)
        #print("==================")
        #print("Below is list of available FIDs: ")
        #print(fids)
        #print("==================")
        b = (str(fid))
        if b in fids:
            #print("\n")
            #print("="*20)
            #print("%s is a valid FID on this switch " % fid)
            #print("="*20)
            return(1)
        else:
            print("\n")
            print("="*20)
            print("%s is a NOT valid FID on this switch " % fid)
            print("="*20)
            return(0)
###############################################################################

def waitForOnline(si):
    """
        wait for a switch to return to online state
        si = switch object from SwitchInfo
        
    """
    print("\n\n\n\n")
    s_state = si.switch_state()
    while "Offline" in s_state:
        s_state = si.switch_state()
        sleeping = liabhar.count_down(15)
        print("\n\nswitch is Offline ")
        print(s_state)
    sleeping = liabhar.count_down(10)
    return 1
###############################################################################

def mem_usage():
    """
        Returns the top memory users on the switch
    """
    
    capture = anturlar.fos_cmd("ps axu")
    
    return capture
###############################################################################

def mem_usage_top20():
    """
        Returns the top 20 memory users on the switch
    """
    capture = anturlar.fos_cmd("ps -eo vsz,rss,comm,pid | sort | tail -20")
    return capture
###############################################################################    

def mem_monitor(wait_time=1800, iters=336):
    """
        Test Case   Monitor of memory
        Title:
        Feature:    No specific feature
        Objective:  confirm no memory leaks 
        
    """
    ###########################################################################
    ####  todo -
    ####    1.    
    ####
    ###########################################################################
    ####
    #### Steps:
    ####    1. get the memory usage every 1800 seconds ( 30 minute default)
    ####      count is set to 
    ###########################################################################
    #### start testing
    ####
    en = anturlar.Maps()
    sw_ip = en.ipaddress()
    
    baseline = anturlar.fos_cmd("ps -eo command,pid,pmem,rss,vsz ")
    ras = re.compile('([- \.:,\[\]\w\/@\d]+)\s+([\d]+)\s+([.\d]+)\s+([\d]+)\s+([\d]+)(?=\\r\\n)')
    ras = ras.findall(baseline)
    
    i = 0
    k = ras[i][0] + ras[i][1]  #### craete a key with the command name
                               #### and pid added together
    v = [ras[i][3]]   #### create the value as a list otherwise the first one
                      #### is a string and extend command later on will fail
    #print("K AND V ARE : %s   %s " % (k,v))
    d = {k:v}     #### create the first dictionary entry ras[0]
    i = 1         #### start a loop to add all the rest of the entries to the dict
    while i < len(ras):
        if "ps -eo" not in ras[i][0]:    #### exclude the ps command
            #print("\n\n\n\n VALUE OF I is : %s  " % i)
            #print(ras[i][0])
            k = ras[i][0]
            k = k + ras[i][1]
            v = [ras[i][3]]
            d.update({k:v})
        i += 1
    #### print the first baseline dictionary ####     
    for k,v in d.items():
        print("%s      %s   " % (k,v))
    #### wait to get the next set of usage stats
    liabhar.count_down(wait_time)  
 
    x = 0               #### x is the number of loops to run 
    while x <= iters:    ####default is 336 so the test goes 7 days
        x += 1         ####  when wait_time is 1800 seconds
        
        #### wrap with try expect or close any telnet session and reconnect
        #### after the wait time
        current_date = anturlar.fos_cmd("date") 
        capture = anturlar.fos_cmd("ps -eo command,pid,pmem,rss,vsz ")
        ####
        ####  do the calculations
        ####  capture the ps data and put it in a variable to add to the dictionary
        ras = re.compile('([- \.:,\[\]\w\/@\d]+)\s+([\d]+)\s+([.\d]+)\s+([\d]+)\s+([\d]+)(?=\\r\\n)')
        ras = ras.findall(capture)
        #### add the data to the dictionary
        value = []
        y = 0
        while y < len(ras):
            if "ps -eo" not in ras[y][0]:  #### exlude the ps command
                key = ras[y][0] + ras[y][1]
                if key in d:
                    value = d[key]
                    #print("\n\n\nvalue of d key is :  %s " % value )
                else:
                    value = []
                ras_value = [ras[y][3]]
                value.extend(ras_value)
                d[key] = value            #### add the value to the key
            y += 1                        #### if key does not exist add
                                          ####new key and value
        #### print the newest data and wait
        #### write the raw data to a file 
        print("@"*60)
        print("@"*60)
        print("@"*60)
        header_raw = "%s%s%s%s" % ("\nMEMORY WATCH       RAW DATA\n", "  sw_info ipaddr  ",\
                               sw_ip, "\n=================================================\n\n")
        footer_raw = "\n=======================================================================\n"
        fraw = "%s%s%s"%("logs/memory_log_raw_data",sw_ip,".txt")
        ffraw = liabhar.FileStuff(fraw, 'w+b')
        ffraw.write(header_raw)
        for kk, vv in d.items():
            print(kk,vv)    #### print to the crt
        print("@"*60)
        
        #######################################################################
        ####  write the same data to a file
        f = "%s%s%s"%("logs/memory_log_",sw_ip,".txt")
        clear = 1
        if clear == 1 :
            ff = liabhar.FileStuff(f, 'w+b')  #### reset the log file
        else:
            ff = liabhar.FileStuff(f, 'a+b')  #### open for appending
                
        st = "Runs  Percent  Ingrport  Egrport \n"        
        header = "%s%s%s%s" % ("\nMEMORY WATCH\n", "  sw_info ipaddr  ",\
                               sw_ip, "\n==============================\n\n")  
        ff.write(header)
        summary_string = ""
        for kk, vv in d.items():
            #print(kk,vv)
            list_of_value = str(vv)
            ' '.join(list_of_value)
            list_of_value = list_of_value.strip('[]')
            list_of_value = list_of_value.replace("'","")
            list_of_value = kk + ",   " + list_of_value + "\n"
            
            ff.write(list_of_value)
            ffraw.write(list_of_value)
            
            list_of_value = list_of_value.strip('\n')
            list_with_change_key = list_of_value.split(',')
            name_pid = list_with_change_key[0]
            values_for_name_pid = list_with_change_key[1:]
            print("Name pid  :  %s " % name_pid )
            print("VALUES for   %s " % values_for_name_pid)
            low_value = 999999
            high_value = 0
            for v in values_for_name_pid:
                n_to_compare = int(v)
                if low_value > n_to_compare:
                    low_value = n_to_compare
                elif high_value < n_to_compare:
                    high_value = n_to_compare
            print("NAME PID  %s  " % name_pid)
            print("HIGH   LOW   LAST  AMOUNT_of_CHANGE   VALUES %s : %s  " % ( high_value, low_value))
            any_change = high_value - low_value    
            summary_string = summary_string+name_pid+",   "+str(low_value)+",  "+str(high_value)+",  "+str(n_to_compare)+ ",  "+str(any_change)+"\n"
        
        ff.write("\n"*6)
        ff.write("@"*40)
        ff.write("\n")
        ff.write("@"*40)
        ff.write("\n")
        ff.write("SUMMARY OF MEMORY LOW AND HIGH VALUES")
        ff.write("\n\n")
        ff.write(summary_string)
        
        ff.close()
        
        ffraw.write(footer_raw)
        ffraw.close()
        
        liabhar.cls()
        print("Memory Watch   Step  %s  " % x )
        print("Your data is in %s  " % f )
        print("time to next data capture : ")
        liabhar.count_down(wait_time)
    
    return()
###############################################################################   

def switch_power_off_on(chassis_name, mode = 'on'):  
    """
        From hand edited Switch_Matrix csv file (should be in /home/RunFromHere/ini directory),
        find IP and port# of related Power Tower and power off all power supplies for that switch
        then power on again for a full power cycle.
          
        File name is SwitchMatrix.csv 
    """
    ####  cn is chassis name   
    ####
    cn = chassis_name
    test_file = '/home/RunFromHere/ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(test_file, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return(False)
    
    for line in csv_file:
        switch_name = (line['Nickname'])
        if switch_name == cn[0]:
            sn = (switch_name)
            power1 = (line['Power1 IP'])
            pp1 = (line['Power1 Port'])
            power2 = (line['Power2 IP'])
            pp2 = (line['Power2 Port'])
            power3 = (line['Power3 IP'])
            pp3 = (line['Power3 Port'])
            power4 = (line['Power4 IP'])
            pp4 = (line['Power4 Port'])            
            a = [power1, pp1, power2, pp2, power3, pp3, power4, pp4]
    for i in range(0,len(a),2):
        if a[i]:
            power = (a[i])
            pp = (a[i+1])
            db = 0
            anturlar.connect_tel_noparse_power(power,'user','pass', db)
            anturlar.power_cmd("cd access/1\t/1\t" + pp, db)
            for i in ["show", mode, "yes"]:
                anturlar.power_cmd(i, db)
            liabhar.JustSleep(10)
            anturlar.close_tel()
    return(True)

def cfgupload(ftp_ip, ftp_user, ftp_pass, clear = 0):
    """
        capture any information for testing of the configdownload 
        - including mapspolicy --show
                    mapsconfig --show
                    flow --show
                    flow --show -ctrlcfg
                    relayconfig --show
                    bottleneckmon --status
                    
        then perform configupload
        
        config upload 
        
        Nimbus_______________Odin_86__:FID25:root> configupload
        Protocol (scp, ftp, sftp, local) [ftp]: ftp 
        Server Name or IP Address [host]: 10.38.38.138
        User Name [user]: ftp2
        Path/Filename [<home dir>/config.txt]: Odin_configupload.txt
        Section (all|chassis|FID# [all]): all
        Password:
        
        or
        
        configdownload [- all ] [-p ftp | -ftp] ["host","user","path"[,"passwd"]]
        configdownload [- all ] [-p scp | -scp ] ["host","user","path"]
        
    """
    #### capture maps config all FIDS
    #### capture flow config all FIDS
    ####
    
    sw_info = anturlar.SwitchInfo()
    sw_info_ls = sw_info.ls()
    fid_now = sw_info.ls_now()
    
    cons_out = anturlar.fos_cmd(" ")
    sw_ip = sw_info.ipaddress()
     
    f = "%s%s%s"%("logs/Configupload_test_case_file",sw_ip,".txt")
    
    if clear == 1 :
        ff = liabhar.FileStuff(f, 'w+b')  #### reset the log file
    else:
        ff = liabhar.FileStuff(f, 'a+b')  #### open for appending
        
    header = "%s%s%s%s" % ("\nCONFIGUPLOAD CAPTURE FILE \n", "  sw_info ipaddr  ",sw_ip, "\n==============================\n\n")  
    ff.write(header)
    ff.close()
    
    ff = liabhar.FileStuff(f, 'a+b')  #### open the log file for writing
    ff.write(str(sw_info_ls))
    ff.write("\n"*2)
    
    cons_out = anturlar.fos_cmd("setcontext %s" % fid_now)
    #cons_out = anturlar.fos_cmd(" ")
    configup_cmd = ("configupload -all -p ftp %s,%s,/configs/%s.txt,%s") % (ftp_ip, ftp_user, sw_ip, ftp_pass)
    ftp_ip, ftp_user, ftp_pass
    cons_out = anturlar.fos_cmd (configup_cmd)
    return(cons_out)

def cfgdownload(ftp_ip, ftp_user, ftp_pass, clear = 0):
    """
        capture any information for testing of the configdownload 
        - including mapspolicy --show
                    mapsconfig --show
                    flow --show
                    flow --show -ctrlcfg
                    relayconfig --show
                    bottleneckmon --status
                    
        then perform configupload
        
        config upload 
        
        Nimbus_______________Odin_86__:FID25:root> configupload
        Protocol (scp, ftp, sftp, local) [ftp]: ftp 
        Server Name or IP Address [host]: 10.38.38.138
        User Name [user]: ftp2
        Path/Filename [<home dir>/config.txt]: Odin_configupload.txt
        Section (all|chassis|FID# [all]): all
        Password:
        
        or
        
        configdownload [- all ] [-p ftp | -ftp] ["host","user","path"[,"passwd"]]
        configdownload [- all ] [-p scp | -scp ] ["host","user","path"]
        
    """
    #### capture maps config all FIDS
    #### capture flow config all FIDS
    ####
    
    sw_info = anturlar.SwitchInfo()
    sw_info_ls = sw_info.ls()
    fid_now = sw_info.ls_now()
    switch_state = sw_info.switch_state()
    
    cons_out = anturlar.fos_cmd(" ")
    sw_ip = sw_info.ipaddress()
     
    if switch_state == "Online":
        anturlar.fos_cmd("switchdisable")
    else:
        pass
    
    cons_out = anturlar.fos_cmd("setcontext %s" % fid_now)
    configdown_cmd = ("echo Y | configdownload -all -p ftp %s,%s,/configs/%s.txt,%s") % (ftp_ip, ftp_user, sw_ip, ftp_pass)
    cons_out = anturlar.fos_cmd (configdown_cmd)
    return(cons_out)
    
    
def get_info_from_the_switch():
    """
    
    """
    
    #cons_out = anturlar.login()
    
    si = anturlar.SwitchInfo()
    mi = anturlar.Maps()
    fi = anturlar.FlowV()
    
    switch_ip = si.ipaddress()
    license_list = si.getLicense()
    ls_list = si.ls()
    first_ls = si.ls_now()
    switch_id = si.switch_id()
    theswitch_name = si.switch_name()
    chassis_name = si.chassisname()
    director_pizza = si.director()
    vf_enabled = si.vf_enabled()
    sw_type = si.switch_type()
    base_sw = si.base_check()
    fcr_state = si.fcr_enabled()
    ports_and_ls = si.all_ports_fc_only()
    psw_reset_value = "YES"
    xisl_st_per_ls = si.allow_xisl()
    maps_policy_sum = mi.get_policies()
    maps_non_dflt_policy = mi.get_nondflt_policies()
    
    flow_per_ls = fi.flow_names()
    
    #############################################################
    #### create a dict for ls and ports in the ls
    ####
    k = str(first_ls)    #### craete a key with the command name
                               #### and pid added together
    v = ports_and_ls     #### create the value as a list otherwise the first one
                         #### is a string and extend command later on will fail
    d_port_list = {k:v}     #### create the first dictionary entry ras[0]
    #v_sn = theswitch_name
    d_switch_name = {k:theswitch_name}
    d_domain_list = {k:switch_id}
    d_xisl_state  = {k:xisl_st_per_ls}
    d_flow_names  = {k:flow_per_ls}
    
    ####
    ###########################################################################
    #### add logical switch specific values to a dictionary
    for ls in ls_list:
        cons_out = anturlar.fos_cmd("setcontext %s " % ls)
        ports_and_ls = si.all_ports_fc_only()
        theswitch_name = si.switch_name()
        domain_for_ls = si.switch_id()
        xisl_st_per_ls = si.allow_xisl()
        flow_per_ls = fi.flow_names()
        
        if ls != str(first_ls):
            #value = []
            #value_sn = []
            #value = ports_and_ls
            #value_sn = theswitch_name
            d_port_list[ls] = ports_and_ls       #### add the value to the key
            d_switch_name[ls] = theswitch_name 
            d_domain_list[ls] = domain_for_ls
            d_xisl_state[ls] = xisl_st_per_ls
            d_flow_names[ls] = flow_per_ls
        
    
    ###########################################################################
    ####
    ####  Create a dictionary
    ####
    switch_dict = {"switch_ip":switch_ip}
    
    switch_dict["switch_name"]  = d_switch_name
    switch_dict["chassis_name"] = chassis_name
    switch_dict["director"]     = director_pizza
    switch_dict["domain_list"]  = d_domain_list
    switch_dict["ls_list"]      = ls_list
    switch_dict["base_sw"]      = base_sw
    switch_dict["xisl_state"]   = d_xisl_state
    switch_dict["switch_type"]  = sw_type
    switch_dict["license_list"] = license_list
    switch_dict["vf_setting"]   = vf_enabled
    switch_dict["fcr_enabled"]  = fcr_state
    switch_dict["port_list"]    = d_port_list
        
    ###########################################################################
    #### print the variables for review
    ####
    print("\n\n\n")
    print("SWITCH IP         :  %s  " % switch_ip)
    print("SWITCH NAME       :  %s  " % d_switch_name)
    print("SWITCH DOMAIN     :  %s  " % d_domain_list)
    print("LS LIST           :  %s  " % ls_list)
    print("BASE SWITCH       :  %s  " % base_sw)
    print("VF SETTING        :  %s  " % vf_enabled)
    print("SWITCH TYPE       :  %s  " % sw_type)
    print("TIMEOUT VALUE     :  0   " )
    print("RESET PASSWORD    :  %s " % psw_reset_value)
    print("FCR ENABLED       :  %s " % fcr_state)
    print("LICENSE LIST      :  %s  " % license_list)
    
    for kk, vv in d_port_list.items():
        print(kk,vv)    #### print to the crt
        print("@"*60)
    print("*"*80)
    print("\n\n\n")
    for kk,vv in d_switch_name.items():
        print(kk,vv)    #### print switchnames
    print('*'*80)
    
    f = "%s%s%s"%("logs/Switch_Info_for_playback_",switch_ip,".txt")
    header = "%s%s%s%s" % ("\nSwitch_info_for_playback CAPTURE FILE \n",\
                           "","", "==============================\n")  
    ff = liabhar.FileStuff(f, 'w+b')  #### open the log file for writing
    ff.write(header)
    #ff.write(str(switch_ip))
    ff.write("SWITCH IP                :  %s  \n" % switch_ip)
    ff.write("SWITCH DOMAIN            :  %s  \n" % d_domain_list)
    ff.write("LS LIST                  :  %s  \n" % ls_list)
    ff.write("BASE SWITCH              :  %s  \n" % base_sw)
    ff.write("SWITCH NAME              :  %s  \n" % d_switch_name)
    ff.write("CHASSIS NAME             :  %s  \n" % chassis_name)
    ff.write("DIRECTOR STATUS          :  %s  \n" % director_pizza)
    ff.write("VF SETTING               :  %s  \n" % vf_enabled)
    ff.write("SWITCH TYPE              :  %s  \n" % sw_type)
    ff.write("TIMEOUT VALUE            :  0   \n" )
    ff.write("RESET PASSWORD           :  %s  \n" % psw_reset_value)
    ff.write("FCR ENABLED              :  %s  \n" % fcr_state)
    ff.write("ALLOW XISL               :  %s  \n" % d_xisl_state)
    ff.write("Ports             :  %s  \n" % d_port_list)
    ff.write("LICENSE LIST      :  %s  \n" % license_list)

    ff.write("="*80)
    ff.write("\n")
    ff.write("MAPS POLICIES            :  %s  \n" % maps_policy_sum )
    ff.write("MAPS NON DFLT POLICIES   :  %s  \n" % maps_non_dflt_policy)
    
    ff.write("="*80)
    ff.write("\n")
    ff.write("FLOW CONFIGURATION       :  %s  \n" % d_flow_names)
    
    
    
    ff.write("\n"*2)
    ff.close()
    #switch_dict = ""
    
    
    return(switch_dict)
    
#def playback_info_from_the_switch():
#    """
#    scratch area for SwitchUpdate class
#    """
#    
#    host = sys.argv[1]
#    user = sys.argv[2]
#    password = sys.argv[7]
#    si = anturlar.SwitchInfo()
#    switch_ip = si.ipaddress()
#
#    f = ("%s%s%s"%("logs/Switch_Info_for_playback_",switch_ip,".txt"))
#    try:
#        with open(f, 'r') as file:
#            a = file.read()
#    except IOError:
#        print("\n\nThere was a problem opening the file:" , f)
#        sys.exit()
#    #ras = re.findall('LICENSE LIST\s+:\s+(\[.+\])', a)
#    ras = re.findall('LICENSE LIST\s+:\s+\[(.+)\]', a)
#    b = ras[0]
#    c = b.split(",")
#    for i in c:
#        #d = i.strip(" '")
#        anturlar.fos_cmd("licenseadd %s" % i)
#        #liabhar.JustSleep(1)
#    #anturlar.fos_cmd("echo y | reboot") ##### Not sure if we need reboot here or somwhere else in the class
#    #print('\n\nSleeping: 150')
#    #liabhar.JustSleep(150)   
#    #anturlar.connect_tel_noparse(host, user, password)
#    anturlar.fos_cmd('licenseshow')
#    return(True)
    
    
    
    
    
    
    
    
    
    
    
    
    
