#!/usr/bin/python3
'''
Solarwinds IPAM Import Script
_AUTHOR: Jake Bergeron <Jakeb@plixer.com>
_DATE: 8/15/2018
_VERSION: 1.1
'''
# Needed Modules
import requests
import getpass
import requests
import json

def _json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial


class SwisClient:
    def __init__(self, hostname, username, password, verify=False):
        self.url = "https://{}:17778/SolarWinds/InformationService/v3/Json/".\
                format(hostname)
        self.credentials = (username, password)
        self.verify = verify

    def query(self, query, **params):
        return self._req(
                "POST",
                "Query",
                {'query': query, 'parameters': params}).json()

    def invoke(self, entity, verb, *args):
        return self._req(
                "POST",
                "Invoke/{}/{}".format(entity, verb), args).json()

    def create(self, entity, **properties):
        return self._req(
                "POST",
                "Create/" + entity, properties).json()

    def read(self, uri):
        return self._req("GET", uri).json()

    def update(self, uri, **properties):
        self._req("POST", uri, properties)

    def delete(self, uri):
        self._req("DELETE", uri)

    def _req(self, method, frag, data=None):
        resp = requests.request(method, self.url + frag,
                                data=json.dumps(data, default=_json_serial),
                                verify=self.verify,
                                auth=self.credentials,
                                headers={'Content-Type': 'application/json'})
		
        # try to extract reason from response when request returns error
        if 400 <= resp.status_code < 600:
            try:
                resp.reason = json.loads(resp.text)['Message'];
            except:
                pass;
			 
        resp.raise_for_status()
        return resp

def GetGroups():
    server = input("Server IP: ")
    username = input("Username: ")
    password = getpass.getpass()
    verify = False
    if not verify:
        from requests.packages.urllib3.exceptions import InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    # Connect to the NPM server
    print("Connecting to %s as User - %s" % (server,username))
    try:
        swis = SwisClient(server,username,password)
    except BaseException as err:
        print(err)
    try:
        aliases = swis.invoke('Metadata.Entity', 'GetAliases', 'SELECT B.Caption FROM Orion.Nodes B')
        print(aliases)
    except BaseException as err:
        print(err)
GetGroups()