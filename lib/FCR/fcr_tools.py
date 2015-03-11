#!/opt/python3/bin/python3

###############################################################################
#### Home location is
####
###############################################################################
"""
FCR TOOLS - different functions to get information from switches and/or fabrics in regards to FCR configuration

"""

import anturlar
import liabhar
import cofra
import sys, os, csv, re

"""
Naming conventions --

module_name                     package_name            
method_name                     ExceptionName           
global_var_name                 instance_var_name
function_parameter_name         local_var_name
GLOBAL_CONSTANT_NAME            ClassName
                                function_name
                                
"""

def test_anturlar_functions():
    #a = ex_port_list()
    #fcri = anturlar.FcrInfo()
    #si = anturlar.SwitchInfo()
    su = cofra.SwitchUpdate
    #a = si.allow_xisl()
    b = su.playback_licenses_to_switch()
    print(b)
    sys.exit()

def bb_fabric_switch_status():
    """
        OBSOLETE##############
        For all switches found in backbone fabric, returns a dictionary data structure for switch
        status for switch states:
        fcr_enabled (T or F); ip address; switch_name; vf_enabled (T or F); base (return base FID
        if T or False if not configured).
    """
    si = anturlar.FcrInfo()
    ips = si.all_switches_in_bb_ip()
    switch_dict = {}
    for i in ips:
        anturlar.connect_tel_noparse(i,'root','password')
        a = switch_status()
        switch_dict = switch_dict + a
        print(switch_dict)
    return(switch_dict)

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
    
    #for i in sw_info_ls:
    #    cons_out = anturlar.fos_cmd("setcontext "+i)   
    #    cons_out = anturlar.fos_cmd("mapsconfig --show")
    #    ff.write("="*80+"\n")
    #    ff.write("="*80+"\n")
    #    ff.write("LOGICAL SWITCH :: " +i+"\n")
    #    ff.write("="*80+"\n")
    #    ff.write("\nMAPS CONFIG::"+i+"\n")
    #    ff.write(cons_out+"\n\n")
    #    ff.write("#"*80+"\n")
    #    ff.write("#"*80+"\n")
    #    
    #    cons_out = anturlar.fos_cmd("mapspolicy --show -summary")
    #    ff.write("="*80+"\n")
    #    ff.write(cons_out+"\n\n")
    #    ff.write("#"*80+"\n")
    #    ff.write("#"*80+"\n")
    #    
    #    cons_out = anturlar.fos_cmd("flow --show")
    #    ff.write("="*80+"\n")
    #    ff.write(cons_out+"\n\n")
    #    ff.write("#"*80+"\n")
    #    ff.write("#"*80+"\n")
    #    
    #    cons_out = anturlar.fos_cmd("flow --show -ctrlcfg")
    #    ff.write("="*80+"\n")
    #    ff.write(cons_out+"\n\n")
    #    ff.write("#"*80+"\n")
    #    ff.write("#"*80+"\n")
    #    
    #    cons_out = anturlar.fos_cmd("relayconfig --show")
    #    ff.write("="*80+"\n")
    #    ff.write(cons_out+"\n\n")
    #    ff.write("#"*80+"\n")
    #    ff.write("#"*80+"\n")
    #    
    #    cons_out = anturlar.fos_cmd("bottleneckmon --status")
    #    ff.write("="*80+"\n")
    #    ff.write(cons_out+"\n\n")
    #    ff.write("#"*80+"\n")
    #    ff.write("#"*80+"\n")
    #    
    #ff.write("="*80+"\n")
    #ff.write("\n"*10)
    
    cons_out = anturlar.fos_cmd("setcontext %s" % fid_now)
    #cons_out = anturlar.fos_cmd(" ")
    configdown_cmd = ("configupload -all -p ftp %s,%s,/configs/%s.txt,%s") % (ftp_ip, ftp_user, sw_ip, ftp_pass)
    ftp_ip, ftp_user, ftp_pass
    cons_out = anturlar.fos_cmd (configdown_cmd)

def configdl(clear = 0):
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
    
    cons_out = anturlar.fos_cmd("setcontext %s" % fid_now)
    #cons_out = anturlar.fos_cmd(" ")
    configdown_cmd = ("configdownload -all -p ftp 10.38.35.131,ftp1,/configs/%s.txt,ftp2") % (sw_ip)
    cons_out = anturlar.fos_cmd (configdown_cmd)

def fab_wide_proxy_device_numbers():
    """
    Retrieve number of proxy device on all backbone switches in fabric. Drop those numbers
    into a file for later retreival (e.g. say after reboot testing). Also return a
    dictionary (e.g {switch_ip: # of proxy devices})
    """
    
    fcrinfo = anturlar.FcrInfo()
    backbone_ip = fcrinfo.fcr_backbone_ip()
    bb_fab_num = (len(backbone_ip))
    proxy_dev_count = []
    for ip in backbone_ip:
        anturlar.connect_tel_noparse(ip,'root','password')
        base = fcrinfo.base_check() # get the base FID number
        if base is not False:
            anturlar.fos_cmd("setcontext " + base)
            get_proxy = fcrinfo.fcr_proxy_dev()
            proxy_dev_count.extend(get_proxy)

        else:
            get_proxy = fcrinfo.fcr_proxy_dev()
            proxy_dev_count.extend(get_proxy)
    switch_list_with_proxy_dev = dict(zip(backbone_ip, proxy_dev_count))
    proxy_dev_count = (str(proxy_dev_count))
    f = ('logs/ProxyDev_Count.txt')
    ff = liabhar.FileStuff(f,'w+b') ###open new file or clobber old
    ff.write(proxy_dev_count)
    ff.close()
    print('\n\n'+ '='*20)        
    print('Backbone Fabric consists of %s switches.' % bb_fab_num)
    print('IP addresses: Number of proxy devices found')
    print(switch_list_with_proxy_dev)
    print('='*20 + '\n\n')
    return(switch_list_with_proxy_dev)


    

def switch_status():
    """
        Retrieve FCR fabric and return info. Variable #'s:
        0) Switch name
        1) IP address
        1) Chassis or Pizza Box
        2) VF or not
        3) FCR Enabled
        4) Base Configured
        
        return dictionary with {switch_name, ipaddr, chassis, vf_enabled, base, fcr_enabled}}
    """
    fcrinfo = anturlar.FcrInfo()
    initial_checks = fcrinfo.sw_basic_info()
    print('\n\n'+ '='*20)
    print("Switch Name :  %s" % initial_checks[0])
    print("IP address :  %s" % initial_checks[1])
    print("Chassis :  %s" % initial_checks[2])
    print("VF enabled :  %s" % initial_checks[3])
    print("FCR enabled :  %s" % initial_checks[4])
    print("Base configured :  %s" % initial_checks[5])
    print('='*20 + '\n\n')
    switch_info = { 'switch_name' : initial_checks[0],'ipaddr' : initial_checks[1], 'chassis' : initial_checks[2],'vf_enabled' : initial_checks[3], 'fcr_enabled' : initial_checks[4], 'base' : initial_checks[5]}
    return (switch_info)

#def ex_deconfig():
#    fcri = anturlar.FcrInfo()
#    test = fcri.ex_deconfig()
#    print('\n\nAll EX_ports found are now deconfigured.')

def ex_port_list():
    """
    Grabs only ONLINE EX-Ports. Parses "switchshow" for EX-Ports.
    """
    si = anturlar.SwitchInfo()
    ex_list = si.ex_ports()
    #print('*************')
    #print(ex_list)
    
   
def ex_deconfig():
    """
    Find all EX-Ports AND VEX-Ports on either director or pizzabox and deconfigure.
    This parses "portcfgshow" command for any EX-Port, online or not, and deconfigures. This includes
    VEX ports as well.
    """
    si = anturlar.SwitchInfo()
    anturlar.fos_cmd("switchdisable")
    portlist =  si.all_ports()
    if si.am_i_director:
        for i in portlist:
            slot = i[0]
            port = i[1]
            pattern = re.compile(r'(?:\EX\sPort\s+)(?P<state> ON)')
            cmd = anturlar.fos_cmd("portcfgshow %a/%a" % (slot, port))
            ex = pattern.search(cmd)
            if ex:
                anturlar.fos_cmd("portcfgexport %s/%s %s"%(slot,port,"-a2"))
                anturlar.fos_cmd("portcfgvexport %s/%s %s"%(slot,port,"-a2"))
    else: 
        for i in portlist:
            print(i)
            port = i[1]
            pattern = re.compile(r'(?:\EX\sPort\s+)(?P<state> ON)')
            cmd = anturlar.fos_cmd("portcfgshow %a" % port)
            ex = pattern.search(cmd)
            if ex:
                anturlar.fos_cmd("portcfgexport %s %s"%(port,"-a2"))
                anturlar.fos_cmd("portcfgvexport %s %s"%(port,"-a2"))
    cmd_cap = anturlar.fos_cmd("switchenable")
    print('\n\nAll EX_ports found are now deconfigured.')
    return(cmd_cap)

def ex_slots_find():
    """
    Find EX/VEX ports and return slot number/port number.
    """
    fcri = anturlar.FcrInfo()
    fcipi = anturlar.FcipInfo()
    vex_port_list = fcri.vex_ports()
    ex_port_list = fcri.ex_ports()
    disabled_port_list = fcri.disabled_ports()
    ge_port_list = fcipi.all_ge_ports()
    print("PORTLISTPORTLIST")
    print(vex_port_list)
    sys.exit(0)
    print(ex_port_list)
    print(disabled_port_list)

    #################################
    print(ex_port_list)
    print(disabled_port_list)
    if self.am_i_director:
       for i in portlist:
            slot = i[0]
            port = i[1]
            pattern = re.compile(r'(?:\EX\sPort\s+)(?P<state> ON)')
            cmd = fos_cmd("portcfgshow %a/%a" % (slot, port))
            ex = pattern.search(cmd)
            if ex:
                fos_cmd("portcfgexport %s/%s %s"%(slot,port,"-a2") )
    else: 
        for i in portlist:
            pattern = re.compile(r'(?:\EX\sPort\s+)(?P<state> ON)')
            cmd = fos_cmd("portcfgshow %a" % i)
            ex = pattern.search(cmd)
            if ex:
                fos_cmd("portcfgexport "+i+" -a2")
        cmd_cap = fos_cmd("switchenable")        
        return(cmd_cap)
    
def fcr_state_persist_enabled():
    #print(sys.argv)
    host = (sys.argv[1])
    user = sys.argv[2]
    password = sys.argv[7]
    test_file = '/home/RunFromHere/ini/SwitchMatrix.csv'
    csv_file = csv.DictReader(open(test_file, 'r'), delimiter=',', quotechar='"')
    fcr_state = switch_status()
    state = fcr_state['fcr_enabled']
    if state is True:
        anturlar.fos_cmd("switchdisable")
        print('\n\nSleeping: 10')
        liabhar.JustSleep(10)
        enabled = switch_status()
        if enabled['fcr_enabled'] is True:
            anturlar.fos_cmd("switchenable")
            print('\n\nSleeping: 10')
            liabhar.JustSleep(10)
            print("\n\nENABLE/DISABLE TEST PASSED")
        else:
            pass
    else:
        print("\n\nENABLE/DISABLE TEST FAILED")
        print("Please enable fcr for this test and try again")
        sys.exit(0)
    print('\n\nSleeping: 10')
    liabhar.JustSleep(10)
    si = anturlar.SwitchInfo()
    cn = si.chassisname()
    a = cofra.switch_power_off_on(cn, 'off')
    print('\n\nSleeping: 20')
    liabhar.JustSleep(20)
    a = cofra.switch_power_off_on(cn, 'on')
    print('\n\nSleeping: 120')
    liabhar.JustSleep(120)
    anturlar.connect_tel_noparse(host, user, password)
    si = anturlar.SwitchInfo()
    print("GETTINGFCRSTATE")
    fcr_state = switch_status()
    state = fcr_state['fcr_enabled']
    if state is True:
        print('Reboot Complete. FCR State remains consistent')
        print('TEST PASSED')
    else:
        print('FCR State changed.')
        print('TEST FAILED')
        
def fcr_state_persist_disabled():
    host = (sys.argv[1])
    user = sys.argv[2]
    password = sys.argv[7]
    test_file = '/home/RunFromHere/ini/SwitchMatrix.csv'
    csv_file = csv.DictReader(open(test_file, 'r'), delimiter=',', quotechar='"')
    fcr_state = switch_status()
    state = fcr_state['fcr_enabled']
    if state is False: #the same to here disabled is false, enabled is true
        anturlar.fos_cmd("switchdisable")
        print('\n\nSleeping: 10')
        liabhar.JustSleep(10)
        enabled = switch_status()
        if enabled['fcr_enabled'] is False:
            anturlar.fos_cmd("switchenable")
            print('\n\nSleeping: 10')
            liabhar.JustSleep(10)
            print("\n\nENABLE/DISABLE TEST PASSED")
        else:
            pass
    else:
        print("\n\nENABLE/DISABLE TEST FAILED")
        print("Please disable fcr for this test and try again")
        sys.exit(0)
    print('\n\nSleeping: 10')
    liabhar.JustSleep(10)
    si = anturlar.SwitchInfo()
    cn = si.chassisname()
    a = cofra.switch_power_off_on(cn, 'off')
    print('\n\nSleeping: 20')
    liabhar.JustSleep(20)
    a = cofra.switch_power_off_on(cn, 'on')
    print('\n\nSleeping: 120')
    liabhar.JustSleep(120)
    anturlar.connect_tel_noparse(host, user, password)
    fcr_state = switch_status()
    state = fcr_state['fcr_enabled']
    if state is False:
        print('Reboot Complete. FCR State remains consistent')
        print('TEST PASSED')
    else:
        print('FCR State changed.')
        print('TEST FAILED')

    sys.exit(0)#######################
    
def license_restore(): #### NEED TO ADD supportftp settings AND Timeserver
    host = sys.argv[1]
    user = sys.argv[2]
    password = sys.argv[7]
    si = anturlar.SwitchInfo()
    cn = si.chassisname()
    test_file = '/home/RunFromHere/ini/SwitchLicenses.csv'
    csv_file = csv.DictReader(open(test_file, 'r'), delimiter=',', quotechar='"')
    for line in csv_file:
        a = (type(line))
        switch_name = (line['Nickname'])
        if switch_name == cn[0]:
            del (line[''])
            del (line ['Nickname'])
            del (line['IP Address'])
            a = (list(line.values()))
            for i in a:
                if i != (''):
                    anturlar.fos_cmd("licenseadd %s" % i)
                    liabhar.JustSleep(5)
    anturlar.fos_cmd("echo y | reboot")
    print('\n\nSleeping: 150')
    liabhar.JustSleep(150)   
    anturlar.connect_tel_noparse(host, user, password)
    anturlar.fos_cmd('licenseshow')
    return(True)


    