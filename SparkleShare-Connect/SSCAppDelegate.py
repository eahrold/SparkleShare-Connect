#-*- coding: utf-8 -*-
#
#  SparkleShare_ConnectAppDelegate.py
#  SparkleShare Connect
#
#  Created by Eldon Ahrold on 4/17/13.
#  Copyright aapps 2013. All rights reserved.
#

from Foundation import *
from AppKit import *
from Cocoa import *
import SSCController
import SSCutils


class SSCAppDelegate(NSObject):
    ssprogress = objc.IBOutlet()
    ssprogbar = objc.IBOutlet()
    
    userName = objc.IBOutlet()
    passWord = objc.IBOutlet()
    serverName = objc.IBOutlet()
    sharedRepo = objc.IBOutlet()
    
    connectButton = objc.IBOutlet()
    window = objc.IBOutlet()
    useMCX = objc.IBOutlet()


    def applicationWillFinishLaunching_(self, sender):
        NSMenu.setMenuBarVisible_(YES)
    
    def applicationDidFinishLaunching_(self, sender):
        return None

    def applicationShouldTerminateAfterLastWindowClosed_(self, sender):
        return YES
