#!/usr/bin/python3
'''
Solarwinds IPAM Import Script
_AUTHOR: Jake Bergeron <Jakeb@plixer.com>
_DATE: 8/15/2018
_VERSION: 1.0
'''
# Needed Modules
import requests
from orionsdk import SwisClient
import os 
import configparser
import getpass

# Create a configuration INI
config = configparser.ConfigParser()
try:
    config.read('.Solarwinds.ini')
    npm_server = config.get('solarwinds', 'npm_server')
    username = config.get('solarwinds', 'username')
    password = config.get('solarwinds', 'password')
except BaseException:
    npm_server = input("What is the IP address of the NPM Server: ")
    username = input("What is the username for authentication: ")
    password = getpass.getpass("What is the password (Will not echo): ")
    config.add_section('solarwinds')
    config.set('solarwinds', 'npm_server', npm_server)
    config.set('solarwinds', 'username', username)
    config.set('solarwinds', 'password', password)
    with open('.Solarwinds.ini', 'w') as configfile:
        config.write(configfile)
try: # Remove the old ipgroup import file to help elimiate duplicates
    os.remove('/home/plixer/scrutinizer/files/ipgroup_import.csv')
    GetGroups()
except BaseException:
    def GetGroups():
        verify = False
        if not verify:
            from requests.packages.urllib3.exceptions import InsecureRequestWarning
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        # Connect to the NPM server
        swis = SwisClient(npm_server, username, password)
        # Using the SWIS module query the display name from SW IPAM module
        print("Querying Solarwinds...:")
        results = swis.query(
            "SELECT DisplayName, Address, CIDR from IPAM.Subnet")
        # Iterate through the groups and format them for Scrutinizer
        for row in results['results']:
            networks = []
            if row['Address'] is None:
                continue
            else:
                name = row['DisplayName']
                network = str(row['Address'] + '/' + str(row['CIDR']))
                networks = name, network
            writeFile(networks)
        os.system(
            '/home/plixer/scrutinizer/bin/scrut_util.exe --import ipgroups --reset')

    def writeFile(networks): # write to a new import file
        import csv
        with open('/home/plixer/scrutinizer/files/ipgroup_import.csv', 'a+') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(networks)
GetGroups()
