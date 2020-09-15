#!/usr/bin/env python

########################################################################################################
#
# Copyright (c) 2020 Nutanix Inc. All rights reserved.
# 
# Script Name: get_leader.py
# v1.0 Date: 14-Sep-2020
#
# Summary:
#   This script provides a simple interface to fetch Acropolis OS service leaders in a Nutnaix cluster.
#   This script should be run in a Controller VM in the cluster.
#
# Usage: At CVM prompt, run the script as follows:
#   $ /home/nutanix/serviceability/bin/get_leader.py <service_name>
#   Examples:
#     $ /home/nutanix/serviceability/bin/get_leader.py lcm
#     $ /home/nutanix/serviceability/bin/get_leader.py lcm arithmos
#     $ /home/nutanix/serviceability/bin/get_leader.py lcm arithmos 'health server'
#     $ /home/nutanix/serviceability/bin/get_leader.py all
#
#   To print usage, simply run the script without any arguments.
#
# Author: Azeez Nuruddin (azeez.nuruddin@nutanix.com)
# 
# Files:
#   - get_leader.py...........(script)
#   - get_leader.json.........(data file)
#
# Script Workflow:
#   1. Read and load from JSON, defined AOS services and commands.
#   2. Read and validate service names in arguments.
#   3. Fetch Acropolis service leader from the Controller VM.
#   4. Parse output and print CVM leader IP address for these services.
#   5. Exit.
#
# Examples:
#   nutanix@NTNX-19FM6H130137-A-CVM:10.63.18.96:~/azeezn$ ./get_leader.py ngt
#   ngt : 10.63.18.99
#   nutanix@NTNX-19FM6H130137-A-CVM:10.63.18.96:~/azeezn$
#   nutanix@NTNX-19FM6H130137-A-CVM:10.63.18.96:~/azeezn$ ./get_leader.py lcm arithmos "health server"
#   arithmos : 10.63.18.96
#   health server : 10.63.18.97
#   cm : 10.63.18.97
#   nutanix@NTNX-19FM6H130137-A-CVM:10.63.18.96:~/azeezn$
#   nutanix@NTNX-19FM6H130137-A-CVM:10.63.18.96:~/azeezn$ ./get_leader.py all
#   acropolis : 10.63.18.99
#   alert manager : 10.63.18.99
#   aplos : 10.63.18.96
#   aplos engine : 10.63.18.96
#   aplos stats publisher : <leader not found>
#   aplos vm scanner : <leader not found>
#   aplos webhook : <leader not found>
#   arithmos : 10.63.18.96
#   arithmoscollector : 10.63.18.98
#   cassandra : 10.63.18.99
#   cassandra monitor : 10.63.18.99
#   catalog : 10.63.18.99
#   cerebro : 10.63.18.99
#   ...
#   ...
#   prism monitor : 10.63.18.96
#   snmp : 10.63.18.99
#   snmp manager : 10.63.18.99
#   uhura : 10.63.18.99
#   zeuscollector : 10.63.18.96
#   zookeeper : 10.63.18.98
#   ookeeper monitor : 10.63.18.98
#   nutanix@NTNX-19FM6H130137-A-CVM:10.63.18.96:~/azeezn$
#
# Disclaimer:
#   This code is intended as a standalone example.  Subject to licensing restrictions defined on nutanix.dev, 
# this script can be downloaded, copied and/or modified in any way you see fit. Please be aware that all public 
# code samples provided by Nutanix are unofficial in nature, are provided as examples only, are unsupported and 
# will need to be heavily scrutinized and potentially modified before they can be used in a production environment. 
# All such code samples are provided on an as-is basis, and Nutanix expressly disclaims all warranties, express or 
# implied.
########################################################################################################

# Import modules
import json
import re
import subprocess
import sys

# Define JSON file
# The JSON file contains AOS services and the CVM commands to retrieve their leaders
jsonFile = './get_leader.json'

# Check args and pop out the script file name
def check_args(args):
    # Pop out script filename from args list
    args.pop(0)
    return args

# Fetch leader for a given service
def get_leader(service):
    # Get the command to run to fetch service leader
    runCmd = serviceObj['services'][service]['command']
    try:
        # Fetch the service leader
        cmdOut = run_command(runCmd)
    except:
        print('Failed to get leader for ' + service)
        cmdOut = ''
    return cmdOut

# Fetch leaders for requested services (in args list)
def get_leaders(args):
    for service in args:
        # Initialize leader key in services dictionary
        serviceObj['services'][service]['leader'] = '<leader not found>'
        # Parse the command output to retrieve the leader IP
        cmdOut = get_leader(service)
        if cmdOut:
            if just_ip(cmdOut):
                serviceObj['services'][service]['leader'] = cmdOut.strip()
                continue
            for line in cmdOut.splitlines():
                if service.split(' ', 1)[0] in line.lower():
                    leaderIp = re.findall(r'(?:\d{1,3}\.)+(?:\d{1,3})', line)[0]
                    serviceObj['services'][service]['leader'] = leaderIp
                    break
    return

# Read JSON and build a global services and commands dictionary
def get_services():
    global serviceObj
    serviceObj = read_json(jsonFile)

# Check if a string is an IP-address-only string, with or without a port number attached to it
def just_ip(someString):
    # String definition leveraged from: https://www.geeksforgeeks.org/python-program-to-validate-an-ip-address/
    ip_re = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)[:0-9]*$'''
    return re.match(ip_re, someString)

# Print CVM leader IP for each requested service (in args list)
def print_leaders(args):
    for service in args:
        print(service + ' : ' + serviceObj['services'][service]['leader'])
    return

# Print script usage with an example
def print_usage(errStr=None):
    if errStr:
        print(errStr)
    print('Command usage: get_leader <arg1> <arg2> ...')
    print('\t- args are leader service names')
    return

# Read JSON file and return the dict object
def read_json(jsonFile):
    try:
        with open(jsonFile, 'r') as jFile:
            data=jFile.read()
        obj = json.loads(data)
    except Exception as e:
        print('ERROR: failed to read ' + jsonFile + '.')
        print(e)
        return
    return obj

# Execute the AOS CLI for service leader
def run_command(cmd):
    return subprocess.check_output(cmd, stdin=None, stderr=subprocess.STDOUT, shell=True, universal_newlines=False)

# Validate service names in args list
def validate_args(args):
    # Get services from the services dictionary read from JSON
    try:
        serviceList = serviceObj['services'].keys()
    except:
        print('ERROR: Services not defined.')
        return
    # Check if service names in argument list are valid. Compare with services in service list
    newArgs = []
    # If user requested leaders for all services, then create list of all services
    # Else validate service names in args list
    if 'all' in [x.lower() for x in args]:
        for service in serviceList:
            newArgs.append(service.lower())
    else:
        for arg in args:
            if arg.lower() not in [x.lower() for x in serviceList]:
                print('Invalid argument: \'' + arg + '\' is not an AOS service.')
            else:
                newArgs.append(arg.lower())
    newArgs.sort()
    return newArgs

# Main function call
def main(args):
    # Check script arguments
    args = check_args(args)
    # If argument list is invalid (empty), then print usage and exit. Else, proceed
    if not args:
        print_usage()
        return 0
    # Build a global services and commands dictionary
    get_services()
    # Validate args with services dictionary
    args = validate_args(args)
    if not args:
        return 0
    # For the reqeusted services, fetch the leaders
    get_leaders(args)
    # Print the service leaders
    print_leaders(args)
    return 1

# Script begin
if __name__ == "__main__":
    main(sys.argv)
    sys.exit(0)
