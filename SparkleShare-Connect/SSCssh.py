#!/usr/bin/env python
import subprocess
import pexpect
import os
from AppKit import *
from SSCutils import progUp,bailOut
RESOURCE_DIRECTORY = NSBundle.mainBundle().resourcePath()

class GitCommands:
    """ these are a set of predefined git commmands that get SSHed to the server
        it is intended to be merely a way to easily ammend methodology based on 
        sparkleshare development and were taken from from https://github.com/hbons/Dazzle"""
    
    def gitRepoCheck(self):
        progUp('checking for repo on server')
        self.cmds=[]
        self.cmds.append('test -f %s/HEAD' % (self.project_path))
        return self.runSSH()

    def gitRepoInit(self):
        progUp('initializing git repo')
        self.cmds=[]
        self.cmds.append('git init --quiet --bare %s' % (self.project_path))
        self.cmds.append('git config --file %s/config receive.denyNonFastForwards true' %(self.project_path))
        return self.runSSH()
    
    def gitSetRepoPerm(self):
        progUp('setting repo permissions')
        self.cmds=[]
        if NSApp.delegate().sharedRepo.state():
            self.cmds.append('git config --file %s/config core.sharedRepository true'% (self.project_path))
            self.cmds.append('chmod -R o-rwx %s'% (self.project_path))
            self.cmds.append('chmod -R g+rwx %s'% (self.project_path))
        else:
            self.cmds.append('git config --file %s/config core.sharedRepository true'% (self.project_path))
            self.cmds.append('chmod -R o-rwx %s'% (self.project_path))
            self.cmds.append('chmod -R g+rwx %s'% (self.project_path))
        return self.runSSH()

    def gitSetRepoAttributes(self):
        progUp('sending repo attribute file')
        attributefile=os.path.join(RESOURCE_DIRECTORY,'attributes')
        filedestination=os.path.join(self.project_path,'info')
        if self.runSCP(attributefile,filedestination):
            return True


class KeyCommands:
    
    def checkAuthKey(self):
        progUp('Testing ssh public key')
        try:
            sendKey="[ ! -d ~/.ssh ] && mkdir -p ~/.ssh;echo \'"+self.pubkey+"\' >> ~/.ssh/authorized_keys"
            sendHello='echo hello world'
            result = self.sshSpawn(sendHello)
            if result == 'Password Needed':
                progUp('Sending Host Key to server')
                self.sshSpawn(sendKey)
                self.sshSpawn(sendHello)
            elif result == 'Auth Key Worked':
                progUp('You already have a key for the server')
            else:
                raise Exception
        except Exception:
            bailOut(result)


    def sshSpawn(self,sshcmd):
        """set up reusable terms for pexpect"""
        expect_newfingerprint = 'Are you sure you want to continue connectin'
        expect_logout= 'logout'
        expect_password= '[Pp]assword:'
        expect_prompt= '[#\$]'
        expect_permission= 'Permission denied'
        
        """ start the pexpect spawn""" 
        ssh = pexpect.spawn('ssh -l %s -p %s %s '%(self.user,self.port,self.server),timeout=5)
        i = ssh.expect([expect_permission,pexpect.TIMEOUT,expect_newfingerprint,expect_password,expect_prompt])
        if i == 0: return 'Server Permission denied'
        if i == 1: return 'Server Timeout'
        if i == 2: # Finger Print Check
            self.fingerprint=(ssh.before.split()[-1]).split('.')[0]
            if self.confirmFingerprint():
                ssh.sendline('yes')
                i=ssh.expect([expect_password,expect_prompt])
                if i == 0:
                    ssh.sendline(self.passwd)
                    i=ssh.expect([expect_password,expect_prompt])
                    if i == 0:
                        return 'Check name and password'
                    elif i == 1:
                        ssh.sendline(sshcmd)
                        ssh.expect(expect_prompt)
                        ssh.sendline(ssh_logout)
                        return 'Password Needed'
                elif i == 1:
                    return 'Auth Key Worked'
                else:
                    return 'Something went wrong.'
            else:
                ssh.sendline('no')
                return 'Wrong Server Fingerprint'
        if i == 3: # Send Password at prompt
            ssh.sendline(self.passwd)
            i=ssh.expect([expect_password,expect_prompt])
            if i == 0:
                return 'Check name and password'
            elif i == 1:
                ssh.sendline(sshcmd)
                ssh.expect(expect_prompt)
                ssh.sendline(expect_logout)
                return 'Password Needed'
            else:
                return 'Something went wrong?'
        if i == 4:
            ssh.sendline(expect_logout)
            return 'Auth Key Worked'
        return 'OK?'
    
    
    
class SSHCommands(GitCommands,KeyCommands):
    """this is how ssh is implemented, currently subprocess makes the most sense"""
    def __init__(self):
        self.cmds=[]
        self.fingerprint = None
    
    def runSSH(self):
        for cmd in self.cmds:
            print(u'doing %s'%cmd)
            sshcmd=['ssh','-l',self.user,'-p',self.port,self.server,cmd]
            p=subprocess.Popen(sshcmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            p.communicate()[0]
            if p.returncode == 0:
               pass
            else:
                return False
        return True

    def runSCP(self,file,remloc):
        #_sshcmd='scp -P %s -q "%s" %s@%s:"%s/"' % (self.port,file,self.user,self.server,remloc)
        sshcmd=['scp','-P', self.port,file,(u'%s@%s:%s' % (self.user,self.server,remloc))]
        p=subprocess.Popen(sshcmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        p.communicate()[0]
        if p.returncode == 0:
            return True
        else:
            return False

    def confirmFingerprint(self):
        mcxfp = None
        if NSApp.delegate().useMCX.state():
            mcxfp = getPref('managedServer')['serverFingerprint']
        if not mcxfp == None:
            if self.fingerprint == mcxfp:
                return True
            else:
                return False
        else:
            fingerPrint_alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(u"RSA key fingerprint for %s" % self.server,"Correct","Wrong!",objc.nil,u"%s" % self.fingerprint)
            
            if fingerPrint_alert.runModal():
                return True
            else:
                return False

   