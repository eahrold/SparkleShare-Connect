#-*- coding: utf-8 -*-
#
#  sscprefs.py
#  SparkleShare Connect
#
#  Created by Eldon Ahrold on 4/18/13.
#  Copyright (c) 2013 aapps. All rights reserved.
#


#import os
#import sys
#import plistlib
import FoundationPlist
from Foundation import *
import SSCutils
from SSCutils import logThis

DEBUG = False
# our preferences "bundle_id"
BUNDLE_ID = 'com.aapps.ssconnect'

def getPref(pref_name):
    default_prefs = {
        'serverPort': '22',
        'serverRepo': '/SparkleShare/',
        'serverName': 'sparkle.local',
        'userName': '',
    }
    pref_value = CFPreferencesCopyAppValue(pref_name, BUNDLE_ID)
    if pref_value == None:
        pref_value = default_prefs.get(pref_name)
        # we're using a default value. We'll write it out to
        # /Library/Preferences/<BUNDLE_ID>.plist for admin
        # discoverability
        setPref(pref_name, pref_value)
    if isinstance(pref_value, NSDate):
        # convert NSDate/CFDates to strings
        pref_value = str(pref_value)
    if DEBUG:
        logThis('Setting %s to %s'%(pref_name,pref_value))
    return pref_value


def setPref(pref_name, pref_value):
    """Sets a preference, writing it to ~/Library/Preferences/aapps.plist."""
    
    try:
        CFPreferencesSetValue(
                              pref_name, pref_value, BUNDLE_ID,
                              kCFPreferencesCurrentUser, kCFPreferencesAnyHost)
    except Exception:
        pass

def setServerPrefs(self):
    setPref('LastServerUsed',self.server)
    setPref(self.server, {'userName':self.user,'serverRepo':self.repo,'serverPort':self.port,})
    CFPreferencesSynchronize(BUNDLE_ID,kCFPreferencesCurrentUser, kCFPreferencesAnyHost)