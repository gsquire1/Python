#!/usr/bin/env python3


import datetime
import sys
import anturlar
import re
import liabhar


"""
cofra is cabinet
"""



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
            firmware_cmd = "firmwaredownload -sfbp scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.3.0/%s,fwdlacct"%(self.firmvrsn)
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
        print("FIRMUP IS %s\n"%(self.firmup))
        print("RAS IS     %s\n"%(ras))
        if ras != self.firmup:
            firmware_cmd = "firmwaredownload -sfbp scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.3.0/%s,fwdlacct"%(self.firmup)
            firmware_cmd = "firmwaredownload -p scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.3.0/%s,fwdlacct"%(self.firmup)
        else:
            firmware_cmd = "firmwaredownload -sfbp scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.2.1/%s,fwdlacct"%(self.firmdown)
            firmware_cmd = "firmwaredownload -p scp 10.38.2.25,scp,/var/ftp/pub/sre/SQA/fos/v7.2.1/%s,fwdlacct"%(self.firmdown)
        reg_ex_list = [b'root> ', b'Y/N\) \[Y]:', b'HA Rebooting', b'Connection to host lost.']
        capture_own_regex = anturlar.fos_cmd_regex(firmware_cmd, reg_ex_list)
        if "the same firmware" in capture_own_regex:
            return(capture_own_regex)
        if "server is inaccessible" in capture_own_regex:
            return(capture_own_regex)
        
        capture_cmd = anturlar.fos_cmd_regex("Y", reg_ex_list)
        #anturlar.close_tel()
        
        liabhar.email_sender_html("smckie@brocade.com", "smckie@brocade.com", "Started Firmware Download ", "%s %s"%(self.firmdown, self.firmup))
        liabhar.count_down(1800) 
        return(capture_cmd)
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
        what for a switch to return to online state
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

    

