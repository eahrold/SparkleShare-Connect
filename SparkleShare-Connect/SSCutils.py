#-*- coding: utf-8 -*-
#
#  SSCutils.py
#  SparkleShare Connect
#
#  Created by Eldon Ahrold on 4/17/13.
#  Copyright (c) 2013 aapps. All rights reserved.
#

import os
import sys
from socket import *
from AppKit import *
import glob
from Foundation import *
from time import sleep
import xml.etree.ElementTree as xml
import shutil



RESOURCE_DIRECTORY = NSBundle.mainBundle().resourcePath()

##############################################################
####  Sanity Check Class
####

class SanityCheck:
    """checks for empty values in required fields"""
    def checkFields(self):
        allFields=[self.user,self.server,self.repo,self.port]
        for field in allFields:
            if field == "":
                bailOut("Please fill out all fields")
        return True
    
    def serverCheck(self):
        """port scan to see wether the port on the server is open"""
        progUp("Checking server and port")
        server_ip = gethostbyname(self.server)
        port=int(float(self.port))
        timeout = 5
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((server_ip, port))
        
        if(result == 0) :
            return True
        else:
            logThis(os.strerror(result))
            bailOut("Check the server and port")
        sock.close()
    
    
    def rsaPubCheck(self):
        """dose a search for the sparkleshare rsa key in the users home directory
            and if it finds it set's the SSServer object's property to the key"""
        progUp('checking for SparkleShare RSA Key.')
        ss_dir='.config/sparkleshare/'
        ss_pub_key_name='*.key.pub'
        try:
            key_file = glob.glob(os.path.join(self.user_home,ss_dir, ss_pub_key_name))[0]
            if os.path.isfile(key_file):
                self.pubkey = open(key_file).read()
                return True
            else:
                raise
        except:
            bailOut('The Key\'s Not there!')






##############################################################
####  Utility Functions
####

def bailOut(msg):
    NSApp.delegate().ssprogress.setStringValue_(msg)
    resetIf()
    raise Exception,msg

def enableInput(bool):
    NSApp.delegate().userName.setEnabled_(bool)
    NSApp.delegate().passWord.setEnabled_(bool)
    NSApp.delegate().connectButton.setEnabled_(bool)

def resetIf():
    enableInput(True)
    #self.ssprogbar.setHidden_(YES)
    progBar(-100)

def tryToSetIBOutlet(outlet,dictionary,value):
    try:
        outlet(dictionary[value])
    except KeyError as name:
        pass



##############################################################
####  Logging/Status Functions
####

def logThis(msg):
    print (msg)

def progUp(msg):
    sleep(0.3)
    NSApp.delegate().ssprogress.setStringValue_(u'%s' % msg)
    progBar(10)
    print (msg)

def progBar(x):
    NSApp.delegate().ssprogbar.incrementBy_(x)



##############################################################
####  SparkleShare Specific Functions
####
def ssRelaunch():
    ss_path=os.path.join("Applications","SparkleShare.app","Contents","MacOS","SparkleShare")
    ss_process=subprocess.Popen("ps -ax| grep [S]parkleShare.app",
                       shell=True,stdin=subprocess.PIPE,
                       stdout=subprocess.PIPE).communicate()[0]
    if ss_process:
        subprocess.Popen(["kill",ss_process.split()[0]])
        time.sleep(3)
    

def openInvite():
    pass

def makePlugin(self):
    logThis("adding that repo to sshare")
    ss_root = xml.Element("sparkleshare")
    plugin = xml.SubElement(ss_root, "plugin")
    info = xml.SubElement(plugin, "info")

    name = xml.SubElement(info, "name")
    name.text = self.project
    ##
    description = xml.SubElement(info,"description")
    description.text = self.server
    ##
    icon = xml.SubElement(info,"icon")
    icon.text = "own-server.png"


    address = xml.SubElement(plugin, "address")

    a_value = xml.SubElement(address, "value")
    a_value.text = (u'ssh://%s@%s' % (self.user,self.server))
    xml.SubElement(address, "example")


    path = xml.SubElement(plugin, "path")

    p_value = xml.SubElement(path, "value")
    p_value.text = self.project_path
    xml.SubElement(path, "example")

    # wrap it in an ElementTree instance, and save as XML
    ss_xml = xml.ElementTree(ss_root)
    plugin_file=(os.path.join(self.user_home,".config","sparkleshare","plugins",self.project+".xml"))
    print plugin_file
    ss_xml.write(plugin_file)


def makeInvite(self):
    logThis("mading an invite link to the project")
    ss_root = xml.Element("sparkleshare")

    invite = xml.SubElement(ss_root, "invite")

    address = xml.SubElement(invite, "address")
    address.text = (u'ssh://%s@%s:%s' % (self.user,self.server,self.port))
    
    remote_path = xml.SubElement(invite, "remote_path")
    remote_path.text = self.project_path
    
    
    if not self.fingerprint :
        self.fingerprint = self.runSSH(["ssh-keygen -lf /etc/ssh_host_rsa_key.pub | cut -b 6-52"]).strip()
    
    fingerprint = xml.SubElement(invite, "fingerprint")
    fingerprint.text = self.fingerprint
    
    ss_xml = xml.ElementTree(ss_root)
    invite_file=(os.path.join(self.user_home,"SparkleShare","repo.xml"))
    ss_xml.write(invite_file)

    sleep(1)
    count = 0

    while os.path.isfile(invite_file) and count < 3:
        print(u"pass %s at adding invite didn't work trying again" % count)
        tmp_file="/tmp/repo.xml"
        shutil.move(invite_file,tmp_file)
        sleep(1)
        shutil.move(tmp_file,invite_file)
        count = count + 1

