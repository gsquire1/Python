#!/opt/python3/bin/python3


###############################################################################
####
####  net install a switch of any 
####
###############################################################################

import os,sys
import os.path

sys.path.append('/home/automation/lib/FOS')
sys.path.append('/home/automation/lib/MAPS')
sys.path.append('/home/automation/lib/NUTS_AND_BOLTS')

import telnetlib
import getpass

import struct

import argparse
import re
import anturlar
import liabhar
import cofra
import csv
import time

###############################################################################
####
####  switch types
####
####  62  DCX
####  64  5300
####  66  5100
####  67  Encryption switch
####  70  5410 - embedded switch
####  71  300
####  72  5480 - embedded switch
####  73  5470 - embedded switch
####  75  M5424 - embedded switch
####  77  DCX-4S
####  83  7800
####  86  5450 - embedded switch
####  87  5460 - embedded switch
####  92  VA-40FC
####  109  6510
####  117  6547  - embedded switch
####  118  6505
####  120  DCX 8510-8
####  121  DCX 8510-4
####  124  5430  - embedded switch
####  125  5431
####  129  6548  - embedded switch
####  130  M6505  - embedded switch
####  133  6520 - odin
####  134  5432  - embedded switch
####  
####  141  Yoda DCX
####  142  Yoda pluto
####  148  Skybolt
####
####  162.0  Wedge
####  165   X6-4 (Venator)
####  166   X6-8 (Allegience)
###############################################################################


def parent_parser():
    
    pp = argparse.ArgumentParser(add_help=False)
    #pp.add_argument("--repeat", help="repeat repeat")
    pp.add_argument("firmware", help="firmware verison 8.1.0_bldxx")
    pp.add_argument("-fa", "--file_action", help="0 to stop after creating file 1 to create new file and continue 2 skip file create and use your own file", type=int, default=0 )
    #pp.add_argument("ip", help="IP address of SUT")
    #pp.add_argument("user", help="username for SUT")
    #pp.add_argument("fid", type=int, default=0, help="Choose the FID to operate on")
    group = pp.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", help="increase output verbosity", default=0, action="count")
    group.add_argument("-q", "--quiet", action="store_true")
    return pp 

def parse_args(args):
    
    verb_value = "99"
    parent_p = parent_parser()      
    parser = argparse.ArgumentParser(description = "PARSER", parents = [parent_p])
    #parser.add_argument('-x', '--xtreme', action="store_true", help="Extremify")
    #parser.add_argument('-f', '--fabwide', action="store_true", help="Execute fabric wide")
    parser.add_argument('-c',   '--chassis_name', type=str, help="Chassis Name in the SwitchMatrix file")
    parser.add_argument('-ip',  '--ipaddr',     help="IP address of target switch")
    parser.add_argument('-cp',   '--cmdprompt', help="switch is already at command prompt", action="store_true")
    parser.add_argument('-t',   '--switchtype', help="switch type number - required with -cp")
    parser.add_argument('-f',    '--filename',   help="File name to use instead of the default file", default="for_playback")
    parser.add_argument('-d',    '--cust_date',      help=argparse.SUPPRESS, )
    #parser.add_argument('-s', '--suite', type=str, help="Suite file name", required=True)
    #parser.add_argument('-p', '--password', help="password")
    #group = parser.add_mutually_exclusive_group()
    #group.add_argument("-v", "--verbose", help="increase output verbosity", default=0, action="count")
    #group.add_argument("-q", "--quiet", action="store_true")
    #parser.add_argument('-ipf', '--ipfile', help="a file with a set of IP address")
    #parser.add_argument("ip", help="IP address of SUT")
    #parser.add_argument("user", help="username for SUT")    
        
    args = parser.parse_args()
    print(args)
    
    if not args.chassis_name and not args.ipaddr:
        print("Chassis Name or IP address is required")
        sys.exit()
        
    if args.cmdprompt and not args.switchtype:
        print("To start at the command prompt the switch type is needed.")
        sys.exit()
        
    if not args.cmdprompt and args.switchtype:
        print('To start at the command prompt both switch type and command prompt is requried')
        sys.exit()
    
    
    #sys.exit()
    #print("Connecting to IP :  " + args.ip)
    #print("user             :  " + args.user)
    #verbose    = args.verbose
     
     

    return(parser.parse_args())


def info_help_OSError():
    """
    """
    print("\n  If the Switch is at the command prompt use the -cp and -t switch")
    print("\n  ./APM/switch_playback.py -cp -t <no> -c <chassisname> <firmware>")
    print("\n\n  Popular switch types are:\n")
    print("       Type      Model\n")
    print("\t62       DCX\n\t64       5300\n\t66       5100\n\t71       300 \n")
    print("\t77       DCX-4S\n\t83       7800\n\t109      6510\n\t118      6505\n")
    print("\t120      DCX 8510-8\n\t121      DCX 8510-4")
    print("\t133      6520/Odin\n\t148      Skybolt ")
    print("\t165      Venator\n\t166      Allegiance ")
    print("\n"*5)
    sys.exit()

def connect_console_enable_root(HOST,usrname,password,port,db=10, *args):
    
    global tn
    
    var = 1
    reg_list = [ b"Enter your option : ", \
                b"login: ", \
                b"assword: ", \
                b"root> ", \
                b".*?users: ", \
                b"Login incorrect", \
                b"=>" , \
                b"admin>", \
                b"key to proceed.", \
                b"Authentication failure" , \
                b" login: ", \
                b"no]"                     ]


    password = "pass"
    capture = ""
    option = 1
    #############################################################################
    #### parse the user name for console login
    ####
    port = str(port)
    usrname = parse_port(port)
    print("connecting via Telnet to  " + HOST + " on port " + port )
    print(HOST)
    print(usrname)
    print(password)
    print(port)
    ###########################################################################
    ####
    #### connect to the console via telnet
    ####   this is connection to console before login 
    ####
    tn = telnetlib.Telnet(HOST,port)
    print("tn value is  ", tn)
    tn.set_debuglevel(db)
    print("@"*80)
    print("CONSOLE==="*8)
    print("CONNECTED VIA TELNET TO THE CONSOLE ")
    print("NEXT STEP IS TO LOGIN TO THE CONSOLE")
    print("\n"*4)
    
    ####liabhar.JustSleep(120)
    
    #############################################################################
    #### login console  
    ####  start the login procedure
    ####
    #############################################################################
    ####
    #### some consoles would not need to login steps so if the capture after the
    ####    telnet login are the words 'Enter your login: '  or reglist 0
    ####     if this is found we can move to the next step if not then login
    ####      to the console
    ####
    ####   steps for both types of consoles
    ####    1. console 1 displays a message "Welcome to Console Server Managment Server .....port SXXX
    ####       - look for this message
    ####          - login to the console
    ####
    ####    2. check for timeout of so many seconds
    ####       - if timeout send a \n and look for login
    ####
    ####    3. should be at switch login 
    ####
    ####
    tn = connect_console(HOST,usrname,password,port,db=10, *args)
  
    #capture = tn.expect(reg_list, 20)
    #if capture[0] == 10:     #### console server management
    #    #######################################################################
    #    ####
    #    #### send the username and password for the console login
    #    ####
    #    ####
    #    capture = tn.expect(reg_list, 130)
    #    print("@"*80)
    #    print(capture)
    #    print("@"*80)
    #    print("STEP TWO OF LOGIN TO THE CONSOLE ")
    #    print("CONSOLE==LOGIN======"*4)
    #
    #    tn.write(usrname.encode('ascii') + b"\r\n")
    #    capture = tn.expect(reg_list)
    #    tn.write(password.encode('ascii') + b"\r\n\n")
    #    capture = tn.expect(reg_list,120)
    #    
    #    tn.write(struct.pack('!b', 49))   #### use the struct to send a integer       
    #    capture = tn.expect(reg_list,120)
    #    
    #    print(capture)
    #else:
    #    tn.write(b"\n")
    #print("1___"*20)
    #print(capture)
    #print(capture[0])
    #print("*"*10)
    #tn.write(b"\n")
    #capture = tn.expect(reg_list, 130)
    #print("2___"*20)
    #print(capture)
    #print(capture[0])
    #print("*"*10)

    ###################################################################################################################
    ####
    ####  this sends number 1 when there are more than one user on the console
    ####
    ###################################################################################################################
    print("CONNECTED TO CONSOLE IN PLAYBACK ")
    liabhar.JustSleep(60)
    
    #if capture[0] == 0:
    #    tn.write(struct.pack('!b', 49))   #### use the struct to send a integer
    #    #print("\n"*11)
    #    #tn.write(b"\n")
    #    capture = tn.expect(reg_list)
    #    print(capture)
    #    print("END CAPTURE PRINT OUT !!!!!!!!!!!!!!!!!!!!! ")
    #else:
    #    tn.write(b"\n")
    
    print("3___"*20)
    tn.write(b"\n")
    capture = tn.expect(reg_list)
    print(capture)
    ###################################################################################################################
    ####
    ####  find login or the user that is logged in. 
    ####
    ###################################################################################################################
    print("4___"*20)
    
    
    if capture[0] == 0:
        tn.write(struct.pack('!b', 49))   #### use the struct to send a integer
        #print("\n"*11)
        #tn.write(b"\n")
        capture = tn.expect(reg_list)
        print(capture)
    else:
        tn.write(b"\n")
        capture = tn.expect(reg_list)
        print(capture)
    
    if capture[0] == 4:          ####  found the users: after starting a regular session
        print("FOUND USER ")
        tn.write(b"\n")
        capture = tn.expect(reg_list)  ####  nothing to do execpt wait for the login or user prompt
        
    if capture[0] == 2:#### if Password is found we did not enter the user name yet.
        print("FOUND PASSWORD  ")
        tn.write(b"\n")          ####  so send a \n so we can get the login prompt
        capture = tn.expect(reg_list)

    if capture[0] == 3:           ##### if root is logged in should be able to continue from here
        print("FOUND ROOT : ")
             
    if capture[0] == 7:           #### if admin is found log out and see if passwords are changed and root is enabled
        print("FOUND ADMIN : ")   #### 
        tn.write(b"exit\n")
        capture = tn.expect(reg_list)
          
    if capture[0] == 1:            ####  found login login as Admin 
        print("FOUND LOGIN : ")    ####    change the root permissions for root then loggin as root
        tn.write(b"admin\n")
        capture = tn.expect(reg_list)
        if capture[0] == 2:                 ####  is password
            print("FIND 2  "*10 )
            tn.write(b"password\n")
            capture = tn.expect(reg_list)
        if capture[0] == 8:                 ####   old password for admin
            tn.write(b"password\n")
            capture = tn.expect(reg_list)
            tn.write(b"password1\n")         #### enter new password
            capture = tn.expect(reg_list)
            tn.write(b"password1\n")         #### enter new password
            capture = tn.expect(reg_list)
            tn.write(b"password\n")         #### enter new user password
            capture = tn.expect(reg_list)
            tn.write(b"password\n")         #### enter new user password
            capture = tn.expect(reg_list) 
            tn.write(b"userconfig --change root -e yes\n")         #### enable root
            capture = tn.expect(reg_list)
            
            tn.write(b"rootaccess --set all\n")         #### enable root
            capture = tn.expect(reg_list)
            
            tn.write(b"yes\n")         #### question Please confirm to proceed
            capture = tn.expect(reg_list)
            
            
            tn.write(b"exit\n")         #### enable root
            capture = tn.expect(reg_list)   
            tn.write(b"root\n")         #### enable root
            capture = tn.expect(reg_list)   
            tn.write(b"fibranne\n")         #### enable root
            capture = tn.expect(reg_list) 
            
            tn.write(b"fibranne\n")         #### enable root
            capture = tn.expect(reg_list) 
           
            tn.write(b"password\n")         #### enable root
            capture = tn.expect(reg_list) 
            tn.write(b"password\n")         #### enable root
            capture = tn.expect(reg_list) 
            tn.write(b"firmwareshow\n")         #### enable root
            capture = tn.expect(reg_list) 


                        
    print("\n"*8)
    print("@"*30)
    print("@"*30)
    print("@"*30)
    print(capture)
    tn.write(b"timeout 0\n")
    capture = tn.expect(reg_list)
    print("\n"*10)
    print(capture)
    print("\n"*10)
    liabhar.JustSleep(10)

    return(tn)



def connect_console(HOST,usrname,password,port,db=10, *args):
    
    global tn
    
    
    var = 1
    reg_list = [b"aaaaa: ",  b"Login incorrect", b"option : ", b"root> ", b".*?login: ", b"r of users: ", b"admin> "]   #### using b for byte string
    reg_list_r = [b".*\n", b":root> ", b":admin> "]
    
    password = "pass"
    capture = ""
    option = 1
    #############################################################################
    #### parse the user name for console login
    ####
    port = str(port)
    usrname = parse_port(port)
    print("connecting via Telnet to  " + HOST + " on port " + port )
    print(HOST)
    print(usrname)
    print(password)
    print(port)
    
    tn = telnetlib.Telnet(HOST,port)
    print("tn value is  ", tn)
    tn.set_debuglevel(db)
    print("\n\n")
    print("-"*80)
    print("-"*80)
    print("CONNECTING TO THE CONSOLE-------------------------------------------")
    print("-------------------------CONNECT CONSOLE FUNCTION-------------------")
    print("-------------------------------------------------ready to read lines")
    tn.write(b"\n")
    #############################################################################
    #### login
    capture = tn.expect(reg_list)
    #capture = tn.read_until(b".*?login: ")
    print(capture)
    if capture[0] == 4:        
        tn.write(usrname.encode('ascii') + b"\n")
        #if password:
        capture = tn.read_until(b"assword: ")
        print(capture)
        tn.write(password.encode('ascii') + b"\n")  
        print("\n\n\n\n\n\n\n\n")
    #tn.close()
    #sys.exit()
    
    #############################################################################
    ####
    #### login to the switch
    ####
    ####
    ####
    reg_list = [ b"Enter your option : ", b"login: ", b"assword: ", b"root> ", b"users: ", b"=>" , b"admin> ", b"sh-2.04#"]  
    while var <= 4:
        #print("start of the loop var is equal to ")
        capture = ""
        capture = tn.expect(reg_list,20)
        if capture == -1:
            print(capture)
            sys.exit()
        print(capture)
        
        if capture[0] == 0:
            
            tn.write(struct.pack('!b', 49))   #### use the struct to send a integer 
            ####
                    
        if capture[0] == 1:
            tn.write(b"root\n")
            capture = tn.expect(reg_list,20)
            tn.write(b"password\n")
            capture = tn.expect(reg_list,20)
            if capture[0] == 1:
                tn.write(b"admin\n")
                capture = tn.expect(reg_list,20)
                tn.write(b"password\n")
                if capture[0] == 1:
                    tn.write(b"admin\n")
                    capture = tn.expect(reg_list,20)
                    tn.write(b"fibranne\n")   
                
            
        if capture[0] == 2:
            tn.write(b"password\n")
                    
        if capture[0] == 3:
            #print(capture)
            print("this found root")
            tn.write(b"\n")
            break
        
        if capture[0] == 4:
            #print(capture)
            print("\n\n\n\n\n\nFOUND USERS: \n\n")
            #capture = ""
            
            tn.write(b"\n")
            #capture = tn.expect(reg_list)
            #break
        if capture[0] == 5:
            print(capture)
            tn.write(b"\n")
            var += 4
            break
        
        if capture[0] == 7:  #### at the bash prompt ready to power cycle
            print("\n\nswitch is at the BASH prompt\n\n")
            print("I was expecting the command prompt or FOS prompt\n\n")
            #tn.write(b"\n")
            #sys.exit()
            #break
        
        var += 1
    capture = ""  
    capture = tn.expect(reg_list, 20)
    print("*"*80)
    print(capture)
    print("*"*80)    
    if capture[0] == 1 :
        #print("SENDINGROOT")
        tn.write(b"root\n")
        capture = tn.expect(reg_list, 20)
        tn.write(b"password\n")
        capture = tn.expect(reg_list, 20)
        

    #capture = tn.expect(reg_list, 20)
    
    return(tn)

    
def stop_at_cmd_prompt(db=9):
    global tn
    
    tn.set_debuglevel(db)
    print("\n\n\n\n\n\n\n\nlooking for stop autoboot\n\n")
    
    #cons_out = send_cmd("/sbin/reboot")
    #
    #
    reg_list = [ b"Hit ESC to stop autoboot: "]
    
    tn.write(b"/sbin/reboot\n")
    capture = tn.expect(reg_list, 3600)
    
    #tn.write( b"char(27)")  #### char(27) or \x1b are both ESC 
    tn.write(b"\x1b")
    reg_list = [b"Option?"]
    
    capture = tn.expect(reg_list)
    #tn.write(b"3\n")
    tn.write(b"3\r\n")
    
    reg_list = [ b"=>"]
    capture = tn.expect(reg_list, 300)
    
    return(capture)
       
def env_variables(swtype, gateway_ip, db=10): #put new gateway variable here

    #liabhar.count_down(10)
    
    db = 9
    capture = ""
    ras = re.compile('.\d{1,3}.\d{1,3}.(\d{1,3}).\d{1,3}')
    gw_octet = ras.findall(gateway_ip)
    gw_octet = int(gw_octet[0])
    
    #### set the temp ip address --it has to have some ip so add a temp one
    ####   if gw_octet is 128 it for the raised flow other wise the rest
    ####    of 3rd floor
    ####
    if gw_octet == 128:
        fake_ip = "10.38.134.2"
    else:
        fake_ip = "10.38.34.100"
    tn.set_debuglevel(db)
    #tn.write(b"printenv\n")
    reg_list = [b"=>"]
    reg_list_done = [b"done",b"NVRAM..."]
    
    #### check if the switch is at the boot prompt
    #### if it is at the switch prompt it is wrong
    
    
    #tn.write(b"\n")
    #
    #capture = tn.expect(reg_list, 120)
    #print("env_variable - capture")
    #print("@"*80)
    #print(capture)
    #print("@"*80)
    tn.write(b"date\n")
    
    capture = tn.expect(reg_list, 120)
    
    tn.write(b"printenv\n")
    capture = tn.expect(reg_list, 120)
    
    netmask   = "255.255.240.0"
    #### for all switches except WEDGE (for now) need the bootargs ip=off setting
    ###  the exceptions are below for skybolt and wedge
    bootargs  = "bootargs ip=off"
    
    ethrotate = "no"
    server_ip = "10.38.2.40" #Pass server in as a varialble for a later date
                              # So if server changes or multiple servers etc.
    ethact    = "ENET0"
    
    if swtype == '162' or swtype == "170":
        ethact = "FM1@DTSEC2"
    
    if swtype == '148':   #### HANDLE SKYBOLT and ethact here
        #print("SKYBOLT")
        ethact = "FM1@DTSEC2"
    if swtype == '162' or swtype == '166' or swtype == '165' or swtype == '170' :   #### HANDLE WEDGE and Allegiance bootargs here and CHEWBACCA
        bootargs  = "root=/dev/sda/\$prt rootfstype=ext4 console=ttyS0,9600 quiet"
        
    if swtype == '166' or swtype == '165': #ethprime is a new env variable and "ethact =" between Allegiance and Wedge are different
        ethact = "FM2@DTSEC4"
        a = ("setenv ethprime FM2@DTSEC4 \n")
        tn.write(a.encode('ascii'))
        capture = tn.expect(reg_list, 30)
        
    capture = tn.expect(reg_list, 10) ####   ### add this capture since the next two writes are running together.
                                      ####
    
    a = ("setenv ethact %s \n" % ethact)
    tn.write(a.encode('ascii'))
    capture = tn.expect(reg_list, 30) #######Changed all these to 30
    g = ("setenv gatewayip %s \n" % gateway_ip)
    tn.write(g.encode('ascii'))
    capture = tn.expect(reg_list, 30)
    n = ("setenv netmask %s\n"%netmask)
    tn.write(n.encode('ascii'))
    capture = tn.expect(reg_list, 30)
    b = ("setenv bootargs %s\n"%bootargs)
    tn.write(b.encode('ascii'))
    capture = tn.expect(reg_list, 30)
    e = ("setenv ethrotate %s\n"%ethrotate)
    tn.write(e.encode('ascii'))
    capture = tn.expect(reg_list, 30)
    s = ("setenv serverip %s\n"%server_ip)
    tn.write(s.encode('ascii'))
    capture = tn.expect(reg_list, 30)
    
    #i = ("setenv ipaddr 10.38.134.2\n")
    i = ("setenv ipaddr %s\n" % fake_ip)
    tn.write(i.encode('ascii'))
    capture = tn.expect(reg_list, 30)
    
    tn.write(b"saveenv\n")
    capture = tn.expect(reg_list_done,60)
    capture = tn.expect(reg_list, 30)
    tn.write(b"printenv\n")    
    capture = tn.expect(reg_list, 90)
    
    
    #liabhar.JustSleep(60)
    
    p = ("ping %s  \n" % gateway_ip)
    tn.write(p.encode('ascii'))
    tn.write(b"\n")
    capture = tn.expect(reg_list, 30)
    
    print("oh my \n")
    print("\n\nCOMPLETE with loading ENV VARIABLES\n\n")
    #liabhar.JustSleep(60)
    
    return(capture)

def pwr_cycle(pwr_ip, pp, stage, db=10):
    
    tnn = anturlar.connect_tel_noparse_power(pwr_ip, 'user', 'pass', db)
    
    anturlar.power_cmd("" ,10)
    anturlar.power_cmd("cli" ,10)
    anturlar.power_cmd("cd access/1\t/1\t%s" % pp ,10)
    #anturlar.power_cmd("show\n" ,10)
    
    anturlar.power_cmd(stage, 5)
    anturlar.power_cmd("yes", 5)
    
    #liabhar.JustSleep(10)
    anturlar.power_cmd("exit", 10)
     
    print("\n"*10)
    print("Just sent power pole  %s port %s   %s command " % (pp, stage,pwr_ip))
    print("\n"*5)
    
    return(0) 
    
def load_kernel(switch_type, sw_ip, gateway_ip, frm_version): ###ADDED GATEWAY HERE
    
    reg_list = [ b"^=> "]
    reg_bash = [ b".*?bash-2.04#", b".*?=> ", b"bash-2.04#"]
    #reg_bash = [ b"bash-2.04", b"=> "]
    reg_bash_only = [ b"bash-2.04" ]
    reg_linkup = [ b".*?ink is up"]
    
    #### set tftp command
    
    #ras = re.compile('([\.a-z0-9]+)(?:_)?')
    ras = re.compile('([\.v0-9]+)(?:_)?')
    ras = ras.search(frm_version)
    frm_no_bld = ras.group(1)
    if 'amp' in frm_version:
        frm_no_bld = frm_no_bld + '_amp'
    
    
    if switch_type == '170':  ####  CHEWBACCA
        nbt = "makesinrec 0x1000000 \n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_bash)
        ####
        nbt = "tftpboot 0x2000000 chewbacca/uImage \n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_bash)
        ####
        nbt = "tftpboot 0x3000000 chewbacca/ramdisk_v1.0.img \n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_bash)
        ####
        nbt = "tftpboot 0xc00000 chewbacca/silkworm.dtb \n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_bash)
        ####
        nbt = "bootm 0x2000000 0x3000000 0xc00000 \n"
        tn.write(nbt.encode('ascii'))
        capture = tn.expect(reg_bash)
    
    if switch_type == '133':  ####  ODIN
        nbt = "tftpboot 0x1000000 net_install26_odin.img\n"
        tn.write(nbt.encode('ascii'))
        #capture = tn.expect(reg_list, 30)
        capture = tn.expect(reg_bash)
        tn.write(b"bootm 0x1000000\n")
        #capture = tn.expect(reg_bash_only, 30)
        capture = tn.expect(reg_bash)
        
    if (switch_type == '66' or switch_type == '71' or switch_type == '118' or switch_type == '109'):
        #### 5100  Stinger   tomahawk  tom_too
        nbt = "tftpboot 0x1000000 net_install_v7.2.img\n"
        tn.write(nbt.encode('ascii'))
        #capture = tn.expect(reg_list, 30)
        capture = tn.expect(reg_bash)
        tn.write(b"bootm 0x1000000\n")
        #capture = tn.expect(reg_bash_only, 30)
        capture = tn.expect(reg_bash)
        
    if (switch_type == '120' or switch_type == '121' or switch_type == '64' or switch_type == '83' or switch_type == '62' or switch_type == '77'):
        ####  DCX zentron  pluto zentron  thor  7800
        nbt = "tftpboot 0x1000000 net_install26_8548.img\n"
        tn.write(nbt.encode('ascii'))
        #capture = tn.expect(reg_list, 30)
        capture = tn.expect(reg_bash)
        tn.write(b"bootm 0x1000000\n")
        #capture = tn.expect(reg_bash_only, 30)
        capture = tn.expect(reg_bash)
        
        
    if switch_type == '148':  #### SKYBOLT
        tn.write(b"makesinrec 0x1000000 \n")
        #capture = tn.expect(reg_list,30)
        capture = tn.expect(reg_bash)
        tn.write(b"tftpboot 0x2000000 skybolt/uImage \n")
        #capture = tn.expect(reg_list,30)
        capture = tn.expect(reg_bash)
        tn.write(b"tftpboot 0x3000000 skybolt/ramdisk.skybolt \n")
        #capture = tn.expect(reg_list,30
        capture = tn.expect(reg_bash)
        tn.write(b"tftpboot 0x4000000 skybolt/silkworm.dtb \n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_bash)
        tn.write(b"bootm 0x2000000 0x3000000 0x4000000 \n")
        #caputure = tn.expect(reg_bash_only,30)
        capture = tn.expect(reg_bash)
        
    if (switch_type == '141' or switch_type == '142'):  #### YODA 
        tn.write(b"makesinrec 0x1000000 \n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_bash)
        tn.write(b"tftpboot 0x2000000 yoda/uImage\n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_bash)
        tn.write(b"tftpboot 0x3000000 yoda/ramdisk.yoda\n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_bash)
        tn.write(b"tftpboot 0x4000000 yoda/silkworm_yoda.dtb\n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_bash)
        tn.write(b"bootm 0x2000000 0x3000000 0x4000000\n")
        #caputure = tn.expect(reg_bash_only,30)
        capture = tn.expect(reg_bash)
        
        
        
    if (switch_type == '162'):  #### WEDGE
        tn.write(b"makesinrec 0x1000000 \n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_bash)
        tn.write(b"tftpboot 0x2000000 wedge/uImage.netinstall\n")
        #capture = tn.expect(reg_bash,10)
        capture = tn.expect(reg_bash)
        tn.write(b"tftpboot 0x3000000 wedge/ramdisk_v1.0.img\n")
        #capture = tn.expect(reg_bash,20)
        capture = tn.expect(reg_bash)
        tn.write(b"tftpboot 0x4000000 wedge/silkworm.dtb.netinstall\n")
        #capture = tn.expect(reg_bash,10)
        capture = tn.expect(reg_bash)
        tn.write(b"bootm 0x2000000 0x3000000 0x4000000\n")
        #caputure = tn.expect(reg_bash,60)
        capture = tn.expect(reg_bash)
        
    if (switch_type == '166' or switch_type == '165'):  #### Allegiance
        tn.write(b"makesinrec 0x1000000 \n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_bash)
        tn.write(b"tftpboot 0x2000000 lando/uImage.netinstall\n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_bash)
        tn.write(b"tftpboot 0x3000000 lando/ramdisk_v1.0.img\n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_bash)
        tn.write(b"tftpboot 0xc00000 lando/silkworm.dtb.netinstall\n")
        #capture = tn.expect(reg_bash,30)
        capture = tn.expect(reg_bash)
        tn.write(b"bootm 0x2000000 0x3000000 0xc00000\n")
        #caputure = tn.expect(reg_bash,60)
        capture = tn.expect(reg_bash)

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
####
####  this section is common for all switches after the kernel is loaded
####
####
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
    tn.write(b"export PATH=/usr/sbin:/sbin:$PATH\n")
    capture = tn.expect(reg_bash, 30)
    i = "ifconfig eth0 %s netmask 255.255.240.0 up\n" % sw_ip 
    tn.write(i.encode('ascii'))
    capture = tn.expect(reg_bash, 30)
    gw = "route add default gw %s \n" % gateway_ip
    tn.write(gw.encode('ascii'))
    capture = tn.expect(reg_linkup,30)
    #tn.write(b"\n")
    capture = tn.expect(reg_bash, 20)
    m = "mount -o tcp,nolock,rsize=32768,wsize=32768 10.38.2.20:/export/sre /load\n" ####CHANGE SERVER TO VARIABLE
    tn.write(m.encode('ascii'))
    capture = tn.expect(reg_bash, 30)
    ### firmwarepath
    firmpath = "cd /load/SQA/fos/%s/%s\n" % (frm_no_bld, frm_version)
    tn.write(firmpath.encode('ascii'))
    capture = tn.expect(reg_bash,160)
    #### need to capture when this hangs anc was not able to connect to the server
    ####  this appears to timeout and the last recieve string was
    ####    \xco\xc0\x80  80 repeated 10 times
    tn.write(b"./install release\n")
    capture = tn.expect(reg_bash,160)
    ####  this does not capture the bash  and from the console the last recv b'30`\x00\x180\xf0
    

    return(0)

def do_net_install(sw_info_filename):
    """
    
    """
    global tn
    pa = parse_args(sys.argv)
    pa.filename = sw_info_filename
    print(pa.filename)
    
    if pa.ipaddr:
        print("do IP steps")
        pa.chassis_name = console_info_from_ip(pa.ipaddr)
    
    cons_info         = console_info(pa.chassis_name)
    console_ip        = cons_info[0]
    console_port      = cons_info[1]
    console_ip_bkup   = cons_info[2]
    console_port_bkup = cons_info[3]
    power_pole_info   = pwr_pole_info(pa.chassis_name)    
    usr_pass          = get_user_and_pass(pa.chassis_name)
    user_name         = usr_pass[0]
    usr_psswd         = usr_pass[1]
    ipaddr_switch     = get_ip_from_file(pa.chassis_name)
    print("IPADDR")
    print(ipaddr_switch)
    print("@"*80)
    ras = re.compile('.\d{1,3}.\d{1,3}.(\d{1,3}).\d{1,3}')
    gw_octet = ras.findall(ipaddr_switch)
    gw_octet = int(gw_octet[0])
    if gw_octet >= 129:
        gateway_ip = "10.38.128.1"
    else:
        gateway_ip = "10.38.32.1"
    print("@"*80)
    print(gateway_ip)
    print("\nuser name and password  \n\n")
    print(user_name)
    print(usr_psswd)
    print(usr_pass)
    print(pa.filename)
     
     
    if not pa.cmdprompt:
        try:
            tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,usr_psswd)
        except OSError:
            info_help_OSError()
            #### this will exit here
        
        sw_dict = cofra.get_info_from_the_switch(pa.filename, 128)
        
        anturlar.close_tel()
     
    
        my_ip                = sw_dict["switch_ip"]
        my_cp_ip_list        = sw_dict["cp_ip_list"]
        sw_name              = sw_dict["switch_name"]
        sw_chass_name        = sw_dict["chassis_name"]
        sw_director_or_pizza = sw_dict["director"]
        sw_domains           = sw_dict["domain_list"]
        sw_ls_list           = sw_dict["ls_list"]
        sw_base_fid          = sw_dict["base_sw"]
        sw_xisl              = sw_dict["xisl_state"]
        sw_type              = sw_dict["switch_type"]
        sw_license           = sw_dict["license_list"]
        sw_vf_setting        = sw_dict["vf_setting"]
        sw_fcr_enabled       = sw_dict["fcr_enabled"]
        sw_port_list         = sw_dict["port_list"]
        sw_ex_port_list      = sw_dict["ex_ports"]
    
    else:
        sw_director_or_pizza = False
        sw_type = pa.switchtype
        my_ip = ipaddr_switch
        print("SETTING THE DIRECTOR OR PIZZA BOX VARIABLE")
    #sys.exit()
 
###################################################################################################################
###################################################################################################################
####
####  if I am Director then connect to console 1 and find the cmdprompt
####     then connect to console 2 and find the cmdprompt
####
####     switch IP now needs to be the CP0 and CP1 values
####
    tn_list = []
    print("\n\nCONNECT TO THE CONSOLE NOW\n\n")
    #if sw_director_or_pizza:
    tn_cp0 = connect_console(console_ip, user_name, usr_pass, console_port, 0)
    tn_list.append(tn_cp0)
    
    if sw_director_or_pizza:
        tn_cp1 = connect_console(console_ip_bkup, user_name,usr_pass,console_port_bkup,0)
        tn_list.append(tn_cp1)
    
    
    #for tn in tn_list:
    #    cons_out = send_cmd("switchshow")
    
    print("\n\nOUT OF CONNECTION TO CONSOLE\n\n")
#######################################################################################################################
####
####  reboot and find the command prompt 
####
    cnt = 1
    if not pa.cmdprompt:
        for tn in tn_list:
            cons_out = stop_at_cmd_prompt(0)
            print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print("FIND THE COMMAND PROMPT    \n")
            print(cons_out)
            print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print("NOW SET THE ENV VARIABLES  ")
            print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    
    for tn in tn_list:
        cons_out = env_variables(sw_type,gateway_ip, 0)
        print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") 
        print(cons_out)
        if sw_director_or_pizza:
            load_kernel(sw_type, my_cp_ip_list[cnt], gateway_ip, pa.firmware)
            cnt += 1
        else:
            load_kernel(sw_type, my_ip, gateway_ip, pa.firmware)
 
    
#######################################################################################################################
#######################################################################################################################
#### this step is the same for director or pizza box
####
####  turn each port off then turn each port on (otherwise the delay between did not power cycle the switch)
####
#######################################################################################################################
    reg_list_bash = [b"bash-2.04#"]
    cons_out = tn.expect(reg_list_bash,900)
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") 
    print("LOOKING FOR BASH PROMPT AFTER LOADING THE KERNEL")
    print(cons_out)
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("\nLINE 1176\n")


    try:
        for pp in range(0, len(power_pole_info), 2):
            print('POWERPOLE')
            print(power_pole_info[pp])
            print(power_pole_info[pp+1])
            pwr_cycle(power_pole_info[pp],power_pole_info[pp+1], "off",10)
            time.sleep(4)
            
        for pp in range(0, len(power_pole_info), 2):
            print('POWERPOLE')
            print(power_pole_info[pp])
            print(power_pole_info[pp+1])
            pwr_cycle(power_pole_info[pp],power_pole_info[pp+1], "on",10)
            time.sleep(4)
    except:
        if  '' == power_pole_info[0]:
            print("\n"*20)
            print("NO POWER POLE INFO FOUND ")
            print("HA "*10)
            print("you have to walk to power cycle the switch")
            print("I will wait ")
            liabhar.JustSleep(30)
        else:
            print("POWER TOWER INFO")
            print(power_pole_info[0])
            print(power_pole_info)
            liabhar.JustSleep(30)
            
#######################################################################################################################
#######################################################################################################################
####
#### 
    #### is there another way to tell if switch is ready ??
    #### instead of waiting
    ####  maybe looking at switch Domain and if it is uncomfirmed then switch is not ready
    ####
#######################################################################################################################
#######################################################################################################################
####
####
#######################################################################################################################

    print("\n"*6)
    print("@"*40)
    print("Close Console sessions and login via telnet")
    print("Sleep for a minute at line 1144")
    print("\n"*6)     
    #liabhar.count_down(300)
    #time.sleep(360)
    #cons_out = sw_set_pwd_timeout(usr_psswd,10)
    #print("@"*40)
    #print("TN   TN    TN")
    #print(tn_list)
    #print("@"*40)


    reg_list_after_reboot = [b"is in sync", b"initialization completed."]
    cons_out = tn.expect(reg_list_after_reboot,900)
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") 
    print("HERE WE ARE WAITING FOR THE SWITCH TO REBOOT SOMETIMES TOO LONG OTHERS NOT LONG ENOUGH")
    print(cons_out)
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("IF WE SEE BASH PROMPT HAS BEEN DETECTED WE CAN TAKE OUT THE WAIT 600")
    print("SEARCH FOR LOOKLOOK ")
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") 
    liabhar.count_down(60)
    
    for tn in tn_list:
        tn.close()
    #liabhar.JustSleep(600)
    #liabhar.count_down(600)
    tn_list = []
    print("\n\nCONNECT TO THE CONSOLE NOW\n\n")
    #if sw_director_or_pizza:
    #tn_cp0 = connect_console_enable_root(console_ip, user_name, usr_pass, console_port, 0)
    #tn_list.append(tn_cp0)
    #
    #if sw_director_or_pizza:
    #    tn_cp1 = connect_console_enable_root(console_ip_bkup, user_name,usr_pass,console_port_bkup,0)
    #    tn_list.append(tn_cp1)
    #
    tn_cp0 = connect_console_enable_root(console_ip, user_name, usr_pass, console_port, 0)
    tn_list.append(tn_cp0)
    
    if sw_director_or_pizza:
        tn_cp1 = connect_console(console_ip_bkup, user_name,usr_pass,console_port_bkup,0)
        tn_list.append(tn_cp1)
    
    for tn in tn_list:
        tn.close()
    
    
    
    

def parse_port(port):
    print("port number " , port )
    print("\n\n")
    print("My type is %s"%type(port))
    print("\n\n\n\n")
    ras = re.compile('([0-9]{2})([0-9]{2})')
    ras_result = ras.search(port)
    print("port front  is  ",  ras_result.group(1))
    print("port back is    ",  ras_result.group(2))
    usrname = ras_result.group(2)
    if usrname < "10":
        ras = re.compile('([0]{1})([0-9]{1})')
        ras_result = ras.search(usrname)
        usrname = ras_result.group(2)
    usrname = "port" + usrname
    return usrname

def send_cmd(cmd, db=10):
    global tn
    
    tn.set_debuglevel(db)
    
    capture = ""
    cmd_look = cmd.encode()
    
    #reg_ex_list = [b".*:root> "]
    reg_ex_list = [b"root> ", b"admin> "]
    print(cmd)
    tn.write(cmd.encode('ascii') + b"\n")
    capture = tn.expect(reg_ex_list,3600)
    #print(capture[0])
    #print(capture[1])
    #print(capture[2])
    capture = capture[2]
    capture = capture.decode()
    print(capture, end="")
    
    return(capture)

def console_info_from_ip(ipaddr):
    """
    
    """
    switchmatrix = '/home/RunFromHere/ini/SwitchMatrix.csv'
    switchmatrix = 'ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(switchmatrix, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return(False)
    
    for line in csv_file:
        ip_address_from_file = (line['IP Address'])
        
        if ip_address_from_file == ipaddr:
            swtch_name = (line['Chassisname'])
         
        else:
            print("\n\nIPaddress was not found    please check the numbers and try again\n\n")
            print("@"*80)
            #sys.exit()
            
    return(swtch_name)
    
    
def console_info(chassis_name):
    """
    
    """
    
    switchmatrix = '/home/RunFromHere/ini/SwitchMatrix.csv'
    switchmatrix = 'ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(switchmatrix, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return(False)
    
    for line in csv_file:
        chassis_name_from_file = (line['Chassisname'])
        
        if chassis_name_from_file == chassis_name:
            
            cons_1_ip   = (line['Console1 IP'])
            cons_1_port = (line['Console1 Port']) 
            cons_2_ip   = (line['Console2 IP'])
            cons_2_port = (line['Console2 Port']) 
        
            a = []
            a = [cons_1_ip, cons_1_port]
            
            if cons_2_ip:

                a += [cons_2_ip]
                a += [cons_2_port]
            else:
                a += ["0"]
                a += ["0"]
        else:
            print("\n\n\nChassis Name unknown   please check the spelling and try again \n\n")
            print("@"*80)
            
            #sys.exit()
            
    return(a)


def pwr_pole_info(chassis_name):
    """
    
    """
    switchmatrix = '/home/RunFromHere/ini/SwitchMatrix.csv'
    switchmatrix = 'ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(switchmatrix, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return(False)
    
    #print("@"*80)
    #print("@"*80)
    #print("@"*80)
    
    for line in csv_file:
        chassis_name_from_file = (line['Chassisname'])
        
        #if chassis_name_from_file == chassis_name[0]:
        if chassis_name_from_file == chassis_name:
            #sn = (switch_name)
            
            pwer1_ip = (line['Power1 IP'])
            pwer2_ip = (line['Power2 IP'])
            pwer3_ip = (line['Power3 IP'])
            pwer4_ip = (line['Power4 IP'])
            
            pwer1_prt = (line['Power1 Port'])
            pwer2_prt = (line['Power2 Port'])
            pwer3_prt = (line['Power3 Port'])
            pwer4_prt = (line['Power4 Port'])
            
            p = []
            p =[pwer1_ip, pwer1_prt]
            if pwer2_ip:
                p += [pwer2_ip]
                p += [pwer2_prt]
            if pwer3_ip:
                p += [pwer3_ip]
                p += [pwer3_prt]
            if pwer4_ip:
                p += [pwer4_ip]
                p += [pwer4_prt]
            

    
    return(p)

def get_user_and_pass(chassis_name):
    """
    
    """
    switchmatrix = '/home/RunFromHere/ini/SwitchMatrix.csv'
    switchmatrix = 'ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(switchmatrix, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return(False)
     
    u_and_p = []
    for line in csv_file:
        chassis_name_from_file = (line['Chassisname'])
        if chassis_name_from_file == chassis_name:
            u = (line['Username'])
            p = (line['Password'])
            u_and_p += [u]
            u_and_p += [p]
            
    return(u_and_p)
 
def get_ip_from_file(chassis_name):
    """
    
    """
    switchmatrix = '/home/RunFromHere/ini/SwitchMatrix.csv'
    switchmatrix = 'ini/SwitchMatrix.csv'
    try:
        csv_file = csv.DictReader(open(switchmatrix, 'r'), delimiter=',', quotechar='"')
    except OSError:
        print("Cannot find the file SwitchMatrix.csv")
        return(False)
     
    for line in csv_file:
        chassis_name_from_file = (line['Chassisname'])
        if chassis_name_from_file == chassis_name:
            ip = (line['IP Address'])
                        
    return(ip)

def sw_set_pwd_timeout(pswrd, tn):
    """
        
        set the password for the root, factory, admin user accounts
        
    """
     
    
    reg_list = [ b"Enter your option", b".*?login: ", b"Password: ", b"root> ", b"users: " ]
    reg_login = [ b".*?login: "]
    reg_assword = [ b"assword: ", b"root> "]
    reg_change_pass = [ b"key to proceed.", b"incorrect" ]
    reg_complete   = [ b"zation completed", b"root> "]
    reg_linertn    = [ b"\\r\\n" ]
    
    
    
    print("@"*80)
    print("\n\nlooking for completed task or root>\n\n")
    capture = tn.expect(reg_complete, 10)
    tn.write(b"\n")
    print("\n\nwrite to tn a newline \n\n")
    print("\n\nlooking for login and send root\n\n")
        #capture = tn.expect(reg_linertn)
    capture = tn.expect(reg_login, 10)
    
    tn.write(b"root\n")
    capture = tn.expect(reg_assword, 10)
    print("\n\nlooking for password and send fibranne\n\n")
    print("new login requires old password first\n\n")
    
    tn.write(b"fibranne\n")
    capture = tn.expect(reg_change_pass, 10)
    #### looking for message - press 'Enter' key to proceed. - so send \n  
    tn.write(b"\n")
    capture = tn.expect(reg_linertn,10)

    #### looking for old password:
    tn.write(b"fibranne\n")
    capture = tn.expect(reg_assword,10)
    
    
    
    while True:    
        capture = tn.expect(reg_assword, 20)  #### looking for Enter new password
        #### if root is found break out
        print("CAPTURE is  ")
        print(capture)
        
        if capture[0] == 1:
            print(capture)
            print("this found root")
            break
        if "old password" in capture:
            tn.write(b"fibranne\n")
        elif "Login Failure" in capture:    
            tn.write(b"fibranne\n")
        else:
            tn.write(b"password\n")
            
    capture = tn.expect(reg_list, 20)
    tn.write(b"root\n")
    capture = tn.expect(reg_list, 20)
    tn.write(b"password\n")
    capture = tn.expect(reg_list, 20)
    tn.write(b"timeout 0 \n")
    capture = tn.expect(reg_list, 20)
    
    
    #sys.exit()
    
    
    return(True)
   
def replay_from_file(switch_ip, lic=False, ls=False, base=False, sn=False, vf=False, fcr=False ):
    """
        open the log file for reading and add the following
        1. license
        2. create fids and base switch is previously set
        3. put ports into the FIDS
        4. update domains
        5. update switch name
        6. enable fcr
        7.
    """
    
    ff = ""
    f = ("%s%s%s"%("logs/Switch_Info_%s_for_playback.txt" % switch_ip))
    print(f)
    
    try:
        with open(f, 'r') as file:
            ff = file.read()
    except IOError:
        print("\n\nThere was a problem opening the file" , f)
        sys.exit()
        
    print("look for the info\n")
    print(ff)
    ras_license     = re.findall('LICENSE LIST\s+:\s+\[(.+)\]', ff)
    
    print(ras_license)
    ras_ls_list     = re.findall('LS LIST\s+:\s+\[(.+)\]', ff)
    ras_base        = re.findall('BASE SWITCH\s+:\s+\[(.+)\]', ff)
    ras_switchname  = re.findall('SWITCH NAME\s+:\s+\[(.+)\]', ff)
    ras_vf          = re.findall('VF SETTING\s+:\s+\[(.+)\]', ff)
    ras_fcr         = re.findall('FCR ENABLED\s+:\s+\[(.+)\]', ff)
    ras_xisl        = re.findall('ALLOW XISL\s+:\s+\[(.+)\]', ff)
    ras_ports       = re.findall('Ports\s+:\s+\[(.+)\]', ff)
    
    ll = ras_license[0]
    ll.replace("'","")        #### remove the comma with string command  
    lic_list = ll.split(",")  #### change the data from string to list

    all_list = []
    all_list += [lic_list]
    all_list += [ras_ls_list]
    all_list += [ras_base]
    all_list += [ras_switchname]
        
    
    return(all_list)

   
def user_start():
    go = False
    go = True
    start = 'n'
    while not go : 
              
        is_valid = 0
        while not is_valid:
            try:
                start = str(input("\n\n\n\nCONTINUE WITH RESTORING THE SWITCH  [y/no] : "))
                is_valid = 1 
            except:
                print("\n\nthere was an error with the input")
                #sys.exit()
                
        if start == 'y' :
            go = True
        else:
            print("START VALUE is  %s" % start)
            if start == 'no':
                sys.exit()
            else:
                start = 'n'           
    return()

def load_config(ipaddr_switch, user_name,usr_psswd, filename):
    """
       read from config files and configure the switch
    
    """
    
    try:
        tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,"password")
        
        if tn == "":
            tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,"fibranne")
    
    except:
        tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,"fibranne")
    
    
    
    cons_out = sw_set_pwd_timeout(usr_psswd, tn)
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") 
    print("tn is   %s  " % tn )
    #tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,usr_psswd)
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") 
    
    
    user_start()
    
    print("\n\nLICENSE ADD TO SWITCH \n\n")
    print(ipaddr_switch)
    
    ###################################################################################################################
    ####  
    ####  ask the user which file to use
    ####   prepopulate with the file from above
    ####    check the existience of the file
    ####    correct it or exit
    ####
    ###################################################################################################################
    print("USE USER INPUTED FILE NAME OR DEFAULT")
    
    #cc = cofra.SwitchUpdate("for_playback")
    cc = cofra.SwitchUpdate(filename)
    
    cons_out = cc.playback_licenses()
    cons_out = cc.playback_ls()
    cons_out = cc.playback_switch_names()
    cons_out = cc.playback_switch_domains()
    cons_out = cc.playback_add_ports()
    cons_out = cc.playback_add_ports_ex()
    tn       = cc.reboot_reconnect()
    cons_out = anturlar.fos_cmd("switchshow")
    print(cons_out)
    cons_out = anturlar.fos_cmd("timeout 0")
    print(cons_out)
     
    anturlar.close_tel()
    #tn.write(b"exit\n")
    #tn.close()
    
    
    return(True)

def cant_find_file_message(complete_name,filename):
    """
    
    """
    print("\ncomplete file path")
    print(complete_name)
    print("\nparser  filename ")
    print(filename)
    print("\n\nNO FILE FOUND")
    print("@"*80)
    print("@"*80)
    print("@"*80)
    print("@"*80)
    print("\n\nformat for filename is stinger for the info file\n\n   Switch_Info_10.20.30.40_stinger_for_playback.txt")
    print("                           ^^^^^^^\n")
    print("This part may be a time stamp of when the file was created unless you changed it...\nsince I know the rest of the info I only need the unique part :) \n\n")
    print("@"*80)
    print("@"*80)
    print("@"*80)
    print("@"*80)
 
    sys.exit()
    


def enter_file_ext():
    go = False
    start = 'n'
    ###################################################################################################################
    ####
    ####  enter a file extension for the replay file instead of the default
    ####  otherwise use the defualt
    ####  stop if the user pushes esc 
    ####
    ###################################################################################################################

#######################################################################################################################
####
####  standard way to handle user input
####    - while loop looking for a valid 'go' variable
####       - while loop waiting for a string input
####       - if start variable is y set go to true and exit the procedure
####
#######################################################################################################################
    while not go : 
              
        is_valid = 0
        while not is_valid:
            try:
                start = str(input("\n\n\n\nCONTINUE WITH RESTORING THE SWITCH  [y/no] : "))
                is_valid = 1 
            except:
                print("\n\nthere was an error with the input")
                #sys.exit()        
        if start == 'y' :
            go = True
        else:
            print("START VALUE is  %s" % start)
            if start == 'no':
                sys.exit()
            else:
                start = 'n'
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################   
    
    
def main():

    global tn
     
    
#######################################################################################################################
####
#### 
####
#######################################################################################################################
    pa = parse_args(sys.argv)
    #print(pa)
    print(pa.chassis_name)
    print(pa.ipaddr)
    print(pa.quiet)
    print(pa.verbose)
    print(pa.firmware)
    print(pa.cmdprompt)
    print(pa.file_action)
    print(pa.filename)
    print(pa.cust_date)
    print("@"*40)
    
#######################################################################################################################
####   TO DO
#######################################################################################################################
####
####  if pa.file_action
####        0  -  create the file ONLY             -- if option 0 or 1 then add the date to the filename
####        1  -  Default file and NET INSTALL     -- if option 0 or 1 then add the date to the filename
####        2  -  USER file and NET INSTALL        -- if option 2 we only need the extention from the end of
####                                                      the switch_ip_ to the _ before _playback ????   because the
####                                                      user could change the file or use a previous one and
####                                                      the cust_date would not match
####        3  -  USER FILE and NO net install     -- CONFIGURATION CHANGES ONLY                   < working 11/20/15 >
####
####  if pa.cmdprompt
####       Ignore pa.file_action ( shold be blocked in parser)
####  
####  
####  if pa.filename       is supplied then check for the files existence
####  if pa.type           is supplied then check for the correct type
####  if pa.chassis_name   then get the IP from the SwitchMatrix file
####   
####
    
#######################################################################################################################
#######################################################################################################################
####
#### if user enter ip address then get the chassisname from the
####   SwitchMatrix file
#### then get the info from the SwitchMatrix file using the Chassis Name
####
####  parse the arguments
####
    if pa.ipaddr:
        print("do IP steps")
        pa.chassis_name = console_info_from_ip(pa.ipaddr)
        
    cons_info         = console_info(pa.chassis_name)
    console_ip        = cons_info[0]
    console_port      = cons_info[1]
    console_ip_bkup   = cons_info[2]
    console_port_bkup = cons_info[3]
    power_pole_info   = pwr_pole_info(pa.chassis_name)    
    usr_pass          = get_user_and_pass(pa.chassis_name)
    user_name         = usr_pass[0]
    usr_psswd         = usr_pass[1]
    ipaddr_switch     = get_ip_from_file(pa.chassis_name)
    print("IPADDR")
    print(ipaddr_switch)
    print("@"*80)
    ras = re.compile('.\d{1,3}.\d{1,3}.(\d{1,3}).\d{1,3}')
    gw_octet = ras.findall(ipaddr_switch)
    gw_octet = int(gw_octet[0])
    if gw_octet >= 129:
        gateway_ip = "10.38.128.1"
    else:
        gateway_ip = "10.38.32.1"
    print("@"*80)
    print(gateway_ip)
    print("\nuser name and password  \n\n")
    print(user_name)
    print(usr_psswd)
    print(usr_pass)
    
    #sys.exit()

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
####
#### check the options and start 
####
    print("&"*80)
    print("&"*80)
    print("&"*80)
    print("&"*80)
    print("IF I FIND COMMAND PROMPT SWITCH DO THE NET INSTALL ONLY")
    print("COMAND PROMPT VALUE IS : %s " % (pa.cmdprompt))
    print("THE FOLLOWING ACTION PER THE VALUE OF CAPTURE SWITCH ")
    print("0:  CREATE USER FILE ONLY ")
    print("1:  NET INSTALL AND REPLAY ONLY ")
    print("2:  USER FILE and NETINSTALL ")
    print("3:  USER FILE AND NO NETINSTALL")
    print("\n%s " % pa.file_action)
    print(type(pa.file_action))
    
    #sys.exit()
    

    if pa.cmdprompt:
        do_net_install(pa.filename)
    #### in the netinstall proc you need to check for the bash prompt
    
    if pa.file_action == 3:
        print("USER FILE and NO NETINSTALL")
        ####what is file name
        pa.filename = pa.filename + "_for_playback"
        complete_name = "%s"%("logs/Switch_Info_%s_%s.txt" % (ipaddr_switch, pa.filename))  #### substitute this way
        pa.filename   = "%s"%(pa.filename)                                                  ####  or file might not be
        #### see note at the end of this line                                               ####   found
        if not os.path.isfile(complete_name):  #### this should be checked in parser
            cant_find_file_message(complete_name,pa.filename)
        
        connect_console_enable_root(console_ip,user_name,usr_pass,console_port,10)
        
        if console_ip_bkup != "" and console_ip_bkup != "0":
            connect_console_enable_root(console_ip_bkup,user_name,usr_pass,console_port_bkup,10)
        
        load_config(ipaddr_switch,user_name, usr_pass, pa.filename)
        
        sys.exit()
    
    
    if pa.file_action == 0:
        print("CREATE USER FILE ONLY")
        #### for this section create the file name with Switch_Info + ipaddress + date_stamp + .txt
        ####   user can change the file name afterwords to shorten or make unique to remember
        d = liabhar.dateTimeStuff()
        pa.cust_date = d.simple_no_dash()
        pa.cust_date = d.current_no_dash()
        pa.filename = pa.cust_date + pa.filename
    
        try:
            tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,usr_psswd)
        except OSError:
            info_help_OSError()
            #### this will exit here
        sw_dict = cofra.get_info_from_the_switch(pa.filename, 128)
        anturlar.close_tel()
        
        sys.exit()
    
    
    
    if pa.file_action == 1:
        print("NET INSTALL AND REPLAY ")
        ####   capture data from the switch
        ####   net install the switch
        ####   play back the configuration
        d = liabhar.dateTimeStuff()
        pa.cust_date = d.simple_no_dash()
        pa.cust_date = d.current_no_dash()
        pa.filename = pa.cust_date + pa.filename
        sw_info_filename = pa.filename
        complete_name = "%s"%("logs/Switch_Info_%s_%s.txt" % (ipaddr_switch, pa.filename))
        do_net_install(sw_info_filename)
    
        if not os.path.isfile(complete_name):  #### this should be checked in parser
            cant_find_file_message(complete_name,pa.filename)
        
        connect_console_enable_root(console_ip,user_name,usr_pass,console_port,10)
        
        if console_ip_bkup != "" and console_ip_bkup != "0":
            connect_console_enable_root(console_ip_bkup,user_name,usr_pass,console_port_bkup,10)
        
        load_config(ipaddr_switch,user_name, usr_pass, pa.filename)
    
        sys.exit()    
    #
    
    
    if pa.file_action == 2:
        print("USER FILE and NETINSTALL")
        ####what is file name
        
        d = liabhar.dateTimeStuff()
        pa.cust_date = d.simple_no_dash()
        pa.cust_date = d.current_no_dash()
        pa.filename = pa.filename + "_for_playback"
        pa.filename = pa.cust_date + pa.filename
        sw_info_filename = pa.filename
        complete_name = "%s"%("logs/Switch_Info_%s_%s.txt" % (ipaddr_switch, pa.filename))
        do_net_install(sw_info_filename)
        
        
        complete_name = "%s"%("logs/Switch_Info_%s_%s.txt" % (ipaddr_switch, pa.filename))  #### substitute this way
        pa.filename   = "%s"%(pa.filename)                                                  ####  or file might not be
        #### see note at the end of this line                                               ####   found
        if not os.path.isfile(complete_name):  #### this should be checked in parser
            cant_find_file_message(complete_name,pa.filename)
            
        connect_console_enable_root(console_ip,user_name,usr_pass,console_port,10)
           
        if console_ip_bkup != "" and console_ip_bkup != "0":
            connect_console_enable_root(console_ip_bkup,user_name,usr_pass,console_port_bkup,10)
         
        load_config(ipaddr_switch,user_name, usr_pass, pa.filename)
        
        sys.exit()
        
    #    try:
    #        tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,usr_psswd)
    #    except OSError:
    #        info_help_OSError()
         
    if pa.file_action != 2:
        d = liabhar.dateTimeStuff()
        pa.cust_date = d.simple_no_dash()
        pa.cust_date = d.current_no_dash()
        pa.filename = pa.cust_date + pa.filename
        print(pa.filename)
        print(pa.cust_date)
        print("++++++++++++++++++++++++++")
    



        
###################################################################################################################
###################################################################################################################
#### if the switch is NOT at the command prompt 
#### then get all the info from the switch and save to a file
####  cofra.get_info_from_the_switch creates a file
####
#### If the switch is at the command prompt
####  then args -cp must be used
####

    if pa.file_action == 2:
        print("skip the file creation section")
        try:
            print("SKIP FILE CREATE and the REQUIRED INFO HERE ")
            tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,usr_psswd)
            si = anturlar.SwitchInfo()
            sw_director_or_pizza = si.director()
            sw_type = si.switch_type()
            my_ip = si.ipaddress()
 
            anturlar.close_tel()
        except OSError:
        
            info_help_OSError()
            #### this will exit here
        
    else:
        
        if not pa.cmdprompt: #Only run if NOT at Command prompt????
            try:
                tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,usr_psswd)
            except OSError:
                info_help_OSError()
                #### this will exit here
                
            #sw_dict = cofra.get_info_from_the_switch("for_playback", 128)
            sw_dict = cofra.get_info_from_the_switch(pa.filename, 128)
            my_ip                = sw_dict["switch_ip"]
            my_cp_ip_list        = sw_dict["cp_ip_list"]
            sw_name              = sw_dict["switch_name"]
            sw_chass_name        = sw_dict["chassis_name"]
            sw_director_or_pizza = sw_dict["director"]
            sw_domains           = sw_dict["domain_list"]
            sw_ls_list           = sw_dict["ls_list"]
            sw_base_fid          = sw_dict["base_sw"]
            sw_xisl              = sw_dict["xisl_state"]
            sw_type              = sw_dict["switch_type"]
            sw_license           = sw_dict["license_list"]
            sw_vf_setting        = sw_dict["vf_setting"]
            sw_fcr_enabled       = sw_dict["fcr_enabled"]
            sw_port_list         = sw_dict["port_list"]
            sw_ex_port_list      = sw_dict["ex_ports"]
    
    
            print("\n"*20)
            print("SWITCH IP            : %s   " % my_ip)
            print("CP IP List           : %s   " % my_cp_ip_list)
            print("SWITCH NAME          : %s   " % sw_name)
            print("CHASSIS NAME         : %s   " % sw_chass_name)
            print("DIRECTOR             : %s   " % sw_director_or_pizza)
            print("SWITCH DOMAINS       : %s   " % sw_domains)
            print("LOGICAL SWITCH LIST  : %s   " % sw_ls_list)
            print("BASE FID             : %s   " % sw_base_fid)
            print("XISL STATE           : %s   " % sw_xisl)
            print("SWITCH TYPE          : %s   " % sw_type)
            print("LICENSE LIST         : %s   " % sw_license)
            print("VF SETTING           : %s   " % sw_vf_setting)
            print("FCR SETTING          : %s   " % sw_fcr_enabled)
            print("PORT LIST            : %s   " % sw_port_list)
            print("EX_PORT_LIST         : %s   " % sw_ex_port_list)
            print("@"*40)
            print("@"*40)
            print("CONSOLE INFO         : %s   " % cons_info)
            print("\n")
            print("POWER POLE INFO      : %s   " % power_pole_info)
            
            
    ###################################################################################################################
    ####
    ####  close telnet connection 
    ####
    ###################################################################################################################
            
            anturlar.close_tel()
        else:
            sw_type = pa.switchtype
            my_ip   = ipaddr_switch
            sw_director_or_pizza = False
            my_cp_ip_list = []
        #sys.exit()    
    ###################################################################################################################
    ###################################################################################################################
    ####
    #### if I am Director then get the CP0 and CP1 IP addresses
    ####    before connecting to the console
    #### 
    ###################################################################################################################
    ###################################################################################################################
        print("@"*40)
        print("switch is a director          %s  "    % sw_director_or_pizza)
        print("console_ip                    %s  "    %  console_ip)
        print("console port                  %s  "    %  console_port)
        print("user name is                  %s  "    %  user_name)
        print("password                      %s  "    % usr_pass)
        print("console_ip   backup           %s  "    % console_ip_bkup)
        print("console port backup           %s  "    % console_port_bkup)
        print("CP IP list (chassis CP0 CP1)  %s  "    % my_cp_ip_list)
        if sw_director_or_pizza:
            print("CP0                           %s  "    % my_cp_ip_list[1])
            print("CP1                           %s  "    % my_cp_ip_list[2])  
              
              
    #if pa.file_action == 0:
    #    complete_name = ("Switch_Info_%s_%s.txt" % (my_ip, pa.filename))
    #    print("Data for the switch is stored in logs directory as: %s " % complete_name)
    #    sys.exit()
        
        
    #sys.exit()   #stop here for getting the switch info only


    
###################################################################################################################
###################################################################################################################
####
####  if I am Director then connect to console 1 and find the cmdprompt
####     then connect to console 2 and find the cmdprompt
####
####     switch IP now needs to be the CP0 and CP1 values
####
    tn_list = []
    if sw_director_or_pizza:
        tn_cp0 = connect_console_enable_root(console_ip, user_name, usr_pass, console_port, 0)
        
        tn_cp1 = connect_console_enable_root(console_ip_bkup, user_name,usr_pass,console_port_bkup,0)
        #tn_list = []
        tn_list.append(tn_cp0)
        tn_list.append(tn_cp1)
        
        for tn in tn_list:
            cons_out = send_cmd("switchshow")
        
    
#######################################################################################################################
####
####  reboot and find the command prompt 
####
        cnt = 1
    
        if not pa.cmdprompt:
            for tn in tn_list:
                cons_out = stop_at_cmd_prompt(0)
                print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                print("FIND THE COMMAND PROMPT    \n")
                print(cons_out)
                print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                print("NOW SET THE ENV VARIABLES  ")
                print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            
            for tn in tn_list:
                cons_out = env_variables(sw_type,gateway_ip, 0)
                print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") 
                print(cons_out)
                
                load_kernel(sw_type, my_cp_ip_list[cnt], gateway_ip, pa.firmware)
                cnt += 1
        
    else:
    ###########################################################################
    #### im a pizza box
    ###########################################################################
         
        tn = connect_console_enable_root(console_ip, user_name, usr_pass, console_port, 0)
        tn_list.append(tn)
       
     
#######################################################################################################################
####
####  reboot and find the command prompt
####
        if not pa.cmdprompt:
            cons_out = stop_at_cmd_prompt(9)
            print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print("PIZZA BOX  FIND THE COMMAND PROMPT   \n")
            print(cons_out)
            print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print("PIZZA BOX  NOW SET THE ENV VARIABLES  ")
            print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            
        cons_out = env_variables(sw_type, gateway_ip, 9)
        print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print("\nLINE 1063")
        print(cons_out)
        load_kernel(sw_type, my_ip, gateway_ip, pa.firmware)
        #Need to check for BASH prompt here "bash-2.04#"
    
#######################################################################################################################
#######################################################################################################################
#### this step is the same for director or pizza box
####
####  turn each port off then turn each port on (otherwise the delay between did not power cycle the switch)
####bash-2.04#
#######################################################################################################################
    reg_list_bash = [b".*?bash-2\.04#"]
    cons_out = tn.expect(reg_list_bash,900)
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") 
    print("LOOKING FOR BASH PROMPT AFTER LOADING THE KERNEL")
    print(cons_out)
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("\nLINE 1176\n")


    try:
        for pp in range(0, len(power_pole_info), 2):
            print('POWERPOLE')
            print(power_pole_info[pp])
            print(power_pole_info[pp+1])
            pwr_cycle(power_pole_info[pp],power_pole_info[pp+1], "off",10)
            time.sleep(4)
            
        for pp in range(0, len(power_pole_info), 2):
            print('POWERPOLE')
            print(power_pole_info[pp])
            print(power_pole_info[pp+1])
            pwr_cycle(power_pole_info[pp],power_pole_info[pp+1], "on",10)
            time.sleep(4)
    except:
        if  '' == power_pole_info[0]:
            print("\n"*20)
            print("NO POWER POLE INFO FOUND ")
            print("HA "*10)
            print("you have to walk to power cycle the switch")
            print("I will wait ")
            liabhar.JustSleep(30)
        else:
            print("POWER TOWER INFO")
            print(power_pole_info[0])
            print(power_pole_info)
            liabhar.JustSleep(30)
            
#######################################################################################################################
#######################################################################################################################
####
#### 
    #### is there another way to tell if switch is ready ??
    #### instead of waiting
    ####  maybe looking at switch Domain and if it is uncomfirmed then switch is not ready
    ####
#######################################################################################################################
#######################################################################################################################
####
####
#######################################################################################################################

    print("\n"*6)
    print("@"*40)
    print("Close Console sessions and login via telnet")
    print("Sleep for a minute at line 1144")
    print("\n"*6)     
    #liabhar.count_down(300)
    #time.sleep(360)
    #cons_out = sw_set_pwd_timeout(usr_psswd,10)
    #print("@"*40)
    #print("TN   TN    TN")
    #print(tn_list)
    #print("@"*40)


    reg_list_after_reboot = [b"is in sync", b"initialization completed."]
    cons_out = tn.expect(reg_list_after_reboot,900)
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") 
    print("HERE WE ARE WAITING FOR THE SWITCH TO REBOOT SOMETIMES TOO LONG OTHERS NOT LONG ENOUGH")
    
    print(cons_out)
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("IF WE SEE BASH PROMPT HAS BEEN DETECTED WE CAN TAKE OUT THE WAIT 600")
    print("SEARCH FOR LOOKLOOK ")
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") 
    liabhar.count_down(60)
    
    for tn in tn_list:
        tn.close()
    #liabhar.JustSleep(600)
    #liabhar.count_down(600)
    
    ###################################################################################################################
    ###################################################################################################################
    ###################################################################################################################
    ###################################################################################################################
    ###################################################################################################################
    ###################################################################################################################
    ###################################################################################################################
    ###################################################################################################################
    ####
    ####
    ####  add the config from a file
    ####
    ####  login 
    try:
        tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,"password")
        
    #    if tn == "":
    #        tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,"fibranne")
    #
        
    except:
        sys.exit()
    #    tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,"fibranne")
    #
    
    
    cons_out = sw_set_pwd_timeout(usr_psswd, tn)
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") 
    print("tn is   %s  " % tn )
    #tn = anturlar.connect_tel_noparse(ipaddr_switch,user_name,usr_psswd)
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") 
    
    
    user_start()
    
    print("\n\nLICENSE ADD TO SWITCH \n\n")
    print(my_ip)
    
    ###################################################################################################################
    ####  
    ####  ask the user which file to use
    ####   prepopulate with the file from above
    ####    check the existience of the file
    ####    correct it or exit
    ####
    ###################################################################################################################
    print("USE USER INPUTED FILE NAME OR DEFAULT")
    sys.exit()
    #cc = cofra.SwitchUpdate("for_playback")
    cc = cofra.SwitchUpdate(pa.filename)
    
    cons_out = cc.playback_licenses()
    cons_out = cc.playback_ls()
    cons_out = cc.playback_switch_names()
    cons_out = cc.playback_switch_domains()
    cons_out = cc.playback_add_ports()
    cons_out = cc.playback_add_ports_ex()
    tn       = cc.reboot_reconnect()
    cons_out = anturlar.fos_cmd("switchshow")
    print(cons_out)
    cons_out = anturlar.fos_cmd("timeout 0")
    print(cons_out)
     
    anturlar.close_tel()
    #tn.write(b"exit\n")
    #tn.close()
     
    dt = liabhar.dateTimeStuff()
    date_is = dt.current()
    print(date_is)
    
if __name__ == '__main__':
    
    main()


#######################################################################################################################
#### END                                                                                                           ####
#######################################################################################################################

