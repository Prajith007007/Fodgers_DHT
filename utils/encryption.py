import glob
import os
import requests
import json

from flask import request

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

URL = "http://pj007.pythonanywhere.com/"
os.system("touch metadata.txt")
# This Method creates shards in a directory which can be later used for processing
def createShards(file,email):
    trueWriteName=writeMeta(file.name,email)
    target = os.path.join(APP_ROOT,'shards/')
    if not os.path.isdir(target):
        os.mkdir(target)
    
    
    nodes = getNodes()

    #print("zfec -d="+target+" "+"-p"+" "+email+"_1_"+" "+file.name)
    m=str(len(nodes))
    n=str(len(nodes))
    os.system("zfec -d="+target+" "+"-p"+" "+trueWriteName+" -m "+"2"+" -k "+"2"+" "+file.name)
    shardList = glob.glob(target+"/"+"*.fec")
    print(shardList)
    processShards(target, shardList, email)


def processShards(folder,shards,email):
    
    nodes = getNodes()
    print(nodes)
    
    for i in range(len(shards)):
        sendShard(nodes[0],shards[i],email)

def sendShard(node,file,email):
    file = open(file)
    files = {'user_image': open(file.name, 'rb')}

    # flash("File Uploaded", "success")
    #url=node+'imageUpdate'
    #print(url)
    data={
        'email':email
    }
    #data.append({'email':email})
    test_response = requests.post(node+'imageUpdate', files=files,data=data)
    if test_response.ok:
        print("Shard uploaded successfully to "+str(node))
    else:
        print("Upload failed"+test_response.response)



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

def getLengthFromMeta():
    counter=0
    f = open("metadata.txt","r")
    content = f.read()
    coList = content.split("\n")
    for i in coList:
        counter+=1
    return "_"+str(counter)+"_"

def writeMeta(filename,email):
    writeName = filename.split(".")
    trueWriteName = email+getLengthFromMeta()+"."+writeName[1]
    f = open("metadata.txt","a")
    f.write(trueWriteName+"\n")
    f.close()
    return trueWriteName

file = open('/home/pkesavap/Pictures/photos/DSCN0937.JPG','rb')
print(file.name)


getNodes()
createShards(file, "praji@gmail.com")
#sendShard("http://127.0.0.1:3000/",file)
#processShards(file,"prajithprasad112")
