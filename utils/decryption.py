from fsplit.filesplit import Filesplit
import glob
import os
import requests
from flask import request

URL = "http://pj007.pythonanywhere.com/"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def getNodes():
    hosts = requests.get(URL+'fetchHosts')
    print(hosts.json())
    hostList = []
    for i in hosts.json():
        #print(i['email'])
        #print(i['hosturl'])
        hosturl = i['hosturl']
        if 'ngrok' in hosturl:
            hostList.append(i['hosturl'])
    print(hostList)
    return hostList

def decrypt():
    nodes = getNodes()

def triggerRetrieval(email,node):
    nodes = getNodes()
    params = {'email':email, 'node': node}
    # api request to a API end point which sends the file back to this node.
    for i in range(len(nodes)):
        response_ = requests.get(nodes[i]+"fetchAllData",params=params)
        if response_.ok:
            print("Successfully saved")
            erasureDecode()
        else:
            print(response_.code)

def erasureDecode():
    albums = os.path.join(APP_ROOT,'albums/')
    if not os.path.isdir(albums):
        os.mkdir(albums)
    
    target = os.path.join(APP_ROOT, './../fetchedShards/')
    shardList = glob.glob(target+"/"+"*.fec")
    listofFiles = getListFiles()
    for filename in listofFiles:
        print("zunfec -o="+albums+filename+" "+target+filename+"*")
        os.system("zunfec -o="+albums+filename+" "+target+filename+"*")

def getListFiles():
    f = open("metadata.txt","r")
    content = f.read()
    coList = content.split("\n")
    return coList

triggerRetrieval("praji@gmail.com", "http://5129090bd80b.ngrok.io/")