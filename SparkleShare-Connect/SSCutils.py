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
    pass

def openInvite():
    pass

def makePlugin():
    logThis("adding that repo to sshare")

def makeInvite(userRepo):
    logThis("mading an invite link to the project")




