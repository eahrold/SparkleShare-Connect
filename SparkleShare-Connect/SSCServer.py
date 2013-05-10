#-*- coding: utf-8 -*-
#
#  SSCServer.py
#  SparkleShare Connect
#
#  Created by Eldon Ahrold on 5/3/13.
#  Copyright (c) 2013 aapps. All rights reserved.
#

#import os
#import sys

#!/usr/bin/env python

import os
from AppKit import *
from SSCssh import SSHCommands
from SSCutils import SanityCheck
from SSCprefs import getPref

class SSCserver(SSHCommands,SanityCheck):
    pubkey= ''
    user_home=os.getenv("HOME")

    def __init__(self,s):
        self.server=s.serverName.stringValue()
        self.port=s.serverPort.stringValue()
        self.repo=s.serverRepo.stringValue()
        self.project=s.projectName.stringValue()
        self.project_path=os.path.join(self.repo,self.project)
        self.user=s.userName.stringValue()
        self.passwd=s.passWord.stringValue()
        try:
            sscpref =  getPref(self.server)
            self.fingerprint=sscpref['serverFingerprint']
        except:
            self.fingerprint=""
