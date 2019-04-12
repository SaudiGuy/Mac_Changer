#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Put the interface name to change its Mac Address")
    parser.add_option("-m", "--mac", dest="new_mac", help="Put the new MAC Address for EX. 00:11:22:33:44:55")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] please specify an interface use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] please specify a new MAC address use --help for more info.")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing your mac address for " + interface )
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_result:
        return mac_address_result.group(0)
    else:
        print("[-] Could not read Mac Address")



options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Your Current Mac = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] Mac address was successfully changed to " + current_mac)
else:
    print("[-] Mac Address did NOT change")
