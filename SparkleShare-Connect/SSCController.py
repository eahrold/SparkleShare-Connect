#-*- coding: utf-8 -*-
#
#  SSCController.py
#  SparkleShare Connect
#
#  Created by Eldon Ahrold on 4/17/13.
#  Copyright (c) 2013 aapps. All rights reserved.
#

import os,traceback
import objc

from Foundation import *
from AppKit import *
from Cocoa import *

from SSCServer import *
from SSCutils import *

import SSCprefs
import time

DEBUG = SSCprefs.getPref('debug')

class SSCController(NSObject):
    window = objc.IBOutlet()
    
    ssprogress = objc.IBOutlet()
    ssprogbar = objc.IBOutlet()
    
    connectButton = objc.IBOutlet()
    useMCX = objc.IBOutlet()

    userName = objc.IBOutlet()
    passWord = objc.IBOutlet()

    serverName = objc.IBOutlet()
    serverPort = objc.IBOutlet()
    serverRepo = objc.IBOutlet()
    projectName = objc.IBOutlet()
    
    mcxserver=''
        
    def startRun(self):
        if self.window:
            self.window.center()


    def awakeFromNib(self):
        prog2 = "hello"
        self.ssprogbar.setUsesThreadedAnimation_(True)

        if not SSCprefs.getPref('managedServer'):
            NSApp.delegate().useMCX.setHidden_(True)

        servername = SSCprefs.getPref('LastServerUsed')
        if servername != None:
            ssprefs = SSCprefs.getPref(servername)
            self.serverName.setStringValue_(servername)
            NSApp.delegate().useMCX.setState_(False)

        else:
            ssprefs = SSCprefs.getPref('managedServer')
            NSApp.delegate().useMCX.setState_(True)
       
        tryToSetIBOutlet(self.serverPort.setStringValue_,ssprefs,'serverPort')
        tryToSetIBOutlet(self.serverRepo.setStringValue_,ssprefs,'serverRepo')
        tryToSetIBOutlet(self.userName.setStringValue_,ssprefs,'userName')
        tryToSetIBOutlet(self.projectName.setStringValue_,ssprefs,'userName')

        if NSApp.delegate().useMCX.state():
            self.mcxserver=self.serverName.stringValue()
            
    @objc.IBAction
    def connect_(self,sender):
        server=SSCserver(self)
        try:
            enableInput(False)
            server.checkFields()
            server.rsaPubCheck()
            server.serverCheck()
            server.checkAuthKey()
            if not server.gitRepoCheck():
                server.gitRepoInit()
                server.gitSetRepoAttributes()
                server.gitSetRepoPerm()
            else:
                bailOut("That Repo Exists")
        
        
        except Exception, msg:
            if DEBUG == True:
                print str(msg)
                traceback.print_exc()
            else:
                print str(msg)
        finally:
            print "good bye"
            resetIf()


    @objc.IBAction
    def editServername_(self,sender):
        servername = self.serverName.stringValue()
        if not self.mcxserver == _servername:
            NSApp.delegate().useMCX.setState_(False)
        try:
            ssprefs = SSCprefs.getPref(_servername)
            if not _ssprefs == None:            
                tryToSetIBOutlet(self.serverPort.setStringValue_,ssprefs,'serverPort')
                tryToSetIBOutlet(self.serverRepo.setStringValue_,ssprefs,'serverRepo')
                tryToSetIBOutlet(self.userName.setStringValue_,ssprefs,'userName')
        except:
            print "no pref for that server"

    @objc.IBAction
    def checkUseMCX_(self,sender):
        if sender.state():
            ssprefs = SSCprefs.getPref('managedServer')
            tryToSetIBOutlet(self.serverPort.setStringValue_,ssprefs,'serverPort')
            tryToSetIBOutlet(self.serverRepo.setStringValue_,ssprefs,'serverRepo')
            tryToSetIBOutlet(self.serverName.setStringValue_,ssprefs,'serverName')
            self.mcxserver=self.serverName.stringValue()
        