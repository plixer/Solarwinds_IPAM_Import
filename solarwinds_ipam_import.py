#!/usr/bin/python3
'''
Solarwinds IPAM Import Script
_AUTHOR: Jake Bergeron <Jakeb@plixer.com>
_DATE: 8/15/2018
_VERSION: 1.1
'''
# Needed Modules
import requests
from orionsdk import SwisClient
import os
import configparser
import getpass
import socket

# Grab hostname of machine to encode the password

entropy = socket.gethostname()

def writeFile(networks):  # write to a new import file
    import csv
    with open('/home/plixer/scrutinizer/files/ipgroup_import.csv', 'a+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(networks)

def encode(key, string):  # Simple password encoding https://stackoverflow.com/questions/2490334
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string


def decode(key, string):  # Simple password decode https://stackoverflow.com/questions/2490334
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string


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
    password = encode(str(entropy), getpass.getpass(
        "What is the password (Will not echo): "))
    config.add_section('solarwinds')
    config.set('solarwinds', 'npm_server', npm_server)
    config.set('solarwinds', 'username', username)
    config.set('solarwinds', 'password', password)
    with open('.Solarwinds.ini', 'w') as configfile:
        config.write(configfile)
try:  # Remove the old ipgroup import file to help elimiate duplicates
    os.remove('/home/plixer/scrutinizer/files/ipgroup_import.csv')
    GetGroups()
except BaseException:
    def GetGroups():
        verify = False
        if not verify:
            from requests.packages.urllib3.exceptions import InsecureRequestWarning
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        # Connect to the NPM server
        swis = SwisClient(npm_server, username, decode(str(entropy), password))
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

GetGroups()
