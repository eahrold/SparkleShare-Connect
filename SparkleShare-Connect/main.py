#-*- coding: utf-8 -*-
#
#  main.py
#  SparkleShare Connect
#
#  Created by Eldon Ahrold on 4/17/13.
#  Copyright aapps 2013. All rights reserved.
#

#import modules required by application
import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib
import SSCAppDelegate
import SSCController

# pass control to AppKit
AppHelper.runEventLoop()
