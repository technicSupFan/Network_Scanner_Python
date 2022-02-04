#-*-coding:utf8;-*-
#qpy:3
#qpy:console

import threading
import os
import socket
from datetime import datetime
import sys
import subprocess as sub
from subprocess import PIPE, run
from subprocess import check_output

class bcolors:
    GREEN_IP = '\033[92m'
    ENDC = '\033[0m'
    WARNING_PORT = '\033[33m'
    END = '\033[0m'
    WARNING_PORT_PORT = '\033[36m'
    END2 = '\033[0m'
    hostdevice = '\033[44m'
    active_device = '\033[41m'
    clara = '\33[101m'
    mario = '\33[93m'
    
command = ['ip', 'route'] 
result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
final = result.returncode, result.stdout, result.stderr
hk = final[1]
hkj = hk.strip().split(" ")[-1]
print("\nYour IP-Address at the moment: "+ bcolors.GREEN_IP + hkj + bcolors.ENDC + "\n")

def tcp_scan(network_ip):
    pass
    

def check_for_firewall_ping_block(router):
    print(bcolors.clara + "[*] Checking if ping isn't blocked by firewall"+bcolors.END)
    check_one = os.system("ping -c 2 -W 2 " + router + " >/dev/null 2>&1") 
    if check_one == 0:
        print(bcolors.GREEN_IP + "\n[√] seems to be good" + bcolors.END)
        print(bcolors.WARNING_PORT_PORT + "\n[*] starting last check (pinging google) ..." + bcolors.END)
        check_two = os.system("ping -c 2 -W 2 google.com >/dev/null 2>&1")
        if check_two == 0:
            print(bcolors.GREEN_IP + "\n[√] Success!!! Ping is allowed at current network" + bcolors.END)
            print("\n[*] continue scanning network\n")
            return True
    else:
        print(bcolors.active_device + "\nMaybe the wrong Gateway ..." + bcolors.END)
        print(bcolors.GREEN_IP + "\nTrying to ping Google ...")
        check_two = os.system("ping -c 2 -W 2 google.com >/dev/null 2>&1")
        if check_two == 0:
            print(bcolors.GREEN_IP + "\n[√] Success!!! Ping is allowed at current network" + bcolors.END)
            print("\n[*] continue scanning network\n")
            return True
        else:
            print(bcolors.active_device + "\n[!] WARNING! Ping scan won't work on this network! Do you want to use TCP Scan?" + bcolors.END)
            tcp_ask = input("Do you want to use TCP Scan? (Y/N)")
            if tcp_ask == "Y":
                tcp_scan(router)
            else:
                sys.exit()
def ports_matching(port_nummer):
    with open("service-names-port-numbers.csv", "r") as file:
      a = 0
      ports = {}
      for i in file:
          i_sp = i.strip().split(",")
          a = a + 1
          if a > 10000:
              break
          else:
              #print(i_sp[0] + "    " + i_sp[1])
              #ports[str(i_sp[0])] = str(i_sp[])
              try:
                  if i_sp[0] == None:
                      continue
                  else:
                      if i_sp[3] == "Unassigned":
                          continue
                      else:
                          if i_sp[1] in ports:
                              continue
                          else:
                              ports[i_sp[1]] = i_sp[0]
              except:
                  pass
      return ports[str(port_nummer)]
def pscan(hostname):
    target = hostname
    targetIP = socket.gethostbyname(target)

    tstart = datetime.now()

    
    ports = []
    try:
        for p in range(1, 1200):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            res = sock.connect_ex((targetIP, p))
            if res == 0:
                try:
                    #portz = ports_matching(p)
                    ports.append(p)
                    #print("open port   " + bcolors.WARNING_PORT_PORT + str(p) + bcolors.END2 + "  --->  " +portz)
                except:
                    print("open port  " + bcolors.WARNING_PORT_PORT + str(p) + bcolors.END2)
            sock.close()
        
    except Exception:
        print("There was an Error.")
        sys.exit()

    tend = datetime.now()
    diff = tend - tstart
    for i in ports:
        try:
            portz = ports_matching(i)
            print("open port   " + bcolors.WARNING_PORT_PORT + str(i) + bcolors.END2 + "    --->  " + portz)
        except:
            print("open port   " + bcolors.WARNING_PORT_PORT + str(i) + bcolors.END2)
    print(bcolors.WARNING_PORT + "\nScan completed in " + str(diff) + bcolors.ENDC)
def scan(targ):
    temp = targ
    t=threading.Thread(target=pscan, args=(temp,)) 
    t.start()


def check_ping(hostname): 
    response = os.system("ping -c 1 -W 1 " + hostname+" >/dev/null 2>&1") 
    if response == 0:
        print("Active Devices(IP): " + bcolors.hostdevice + hostname + bcolors.ENDC + "\nName of the device: " + bcolors.active_device + socket.getfqdn(hostname) + bcolors.ENDC + "\n")
        pingstatus = True 
    else:
        pingstatus = False 
    return pingstatus 
def ipscan(): 
    output_ip = []
    print(bcolors.mario + "Do you wanna get the IP address automatically?(Y/N)" + bcolors.ENDC)
    kla = input()
    if kla == "Y":
        hjks = hkj.strip().split(".")
        auto_ip = str(hjks[0] + "." + hjks[1] + "." + hjks[2] + ".")
        for i in range(0,256): 
            host = auto_ip + str(i)
            output_ip.append(host)
    else:
        thehost = input("Enter your IP range (e.g. 192.168.178.) : ")
        for i in range(0,256):
            host = thehost + str(i)
            output_ip.append(host)
    return output_ip
    
    
command = ['ip', 'neigh'] 
result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
final = result.returncode, result.stdout, result.stderr
router_ip = final[1].split(" ")[0]
mac_of_router = final[1].split(" ")[4]
print("Default gateway router:")
print("---> "+str(router_ip))
print("---> "+str(mac_of_router))
print()
check_for_firewall_ping_block(router_ip)
hosts = ipscan()
num_hosts = len(hosts)
for k in range(num_hosts): 
    temp = hosts[k]
    t=threading.Thread(target=check_ping, args=(temp,)) 
    t.start()
print("Do you wanna scan again? (Y/N)")
g = input()
if g == "Y":
    for k in range(num_hosts):
        temp = hosts[k]
        t=threading.Thread(target=check_ping, args=(temp,)) 
        t.start()
 
        
jale = 1
while jale > 0:
    qes = input("Do you wanna scan a device with a port scan? (Y/N): ")
    if qes == "Y":
       iiptar = input("Enter your target device IP: ")
       scan(iiptar)
       jale = 0
    else:
        sys.exit()