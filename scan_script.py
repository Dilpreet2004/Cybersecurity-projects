import nmap
import pandas as pd
import time
from alive_progress import alive_bar

def nmap_scan():
    sc = nmap.PortScanner()

    print("Welcome to this simple Nmap Scanning Tool !!")
    print("---------------------------------------------")

    ip_addr = input("Please enter the IP Address to scan: ")

    print("The entered IP Address is: ", ip_addr)

    resp = input("""\nPlease Enter the type of scan you wish to perform: 
                            1. SYN Scan
                            2. UDP Scan
                            3. Comprehensive Scan\n>""")

    print("You have selected: ", resp)

    resp_dict = {'1':['-sS -v -sV','tcp'],'2':['-sU -v -sV','udp'],'3':['-sS -v -p- -O -sC','tcp']}

    if resp not in resp_dict.keys():
        print("Please enter a valid Option")
    else:
        print("Nmap version: ", sc.nmap_version())
        print("Scanning Target:", ip_addr)
        print("Please wait, scanning in progress...")
        with alive_bar(stats='') as bar:
            sc.scan(ip_addr, "1-65535", resp_dict[resp][0])
            proto = resp_dict[resp][1]
            bar()

        # Check if the specified host is in the scan results.
        if sc.all_hosts() and ip_addr in sc.all_hosts():
            host_state = sc[ip_addr].state()
            if host_state == 'up':
                print("\nHost is up, below are the scan results: ")
                # Use .get() to safely access the protocol information
                if sc[ip_addr].get(proto):
                    ports_data = []
                    for port, info in sc[ip_addr][proto].items():
                        ports_data.append((port, info['name'], info['state']))
                    df = pd.DataFrame(ports_data, columns=['Port', 'Name', 'State'])
                    print(df)

                        
                else:
                    print(f"No {proto.upper()} ports found for this host.")
            else:
                print(f"Host is {host_state}.")
        else:
            print("\nHost is down or could not be scanned.")

if __name__ == "__main__":
    nmap_scan()