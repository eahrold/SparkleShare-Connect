####Sparkle-Server-Connect is a GUI to help non-tech end users set up a sparkle share repo.  It assumes a few things 

1. Your users already have a user name and password for the server and can access it via ssh.
2. You have a share point on the server that authenticated users can write to.  The default is /SparkleShare/.

    `sudo ln -s /path/to/your/storage /SparkleShare/`

4. You've installed git on your server and it's in a path that would be in a default users ENV path.  I like /usr/bin/git.



####what the GUI does

1. reads any preferences set by the user or via MCX
2. using the supplied information tries to first authenticate via SparkleShare rsa-key.  
3. if that fails it will authenticate to the server using the supplied password.
4. then re-tests the key auth, which should now work
5. then via ssh creates a git repo ( using settings similar to hbons/Dazzle.sh )
6. then makes a sparkle share plugin with the settings.


####If deploying MCX you can specify these keys  ( or use example com.aapps.ssconnect.plist)
The deployed file should be installed in /Library/Managed Preferences/

serverName  =  FQDN

serverPort  =  22

serverRepo  =  /path/to/ss/server/dir/

serverFinger =  RSA Fingerprint

invitePath = /SparkleShare/invites/  <-- if left blank this will default to serverRepo/invites/


####To get the Auto-Invites working properly
make a directory on your server called "invites" that has write acces to your sparkleshare group.
this defaults inside of your /SparkleShare/ repo.
Also make sure your www user has access to the directory. 

then add an alias to that directory in your https_website.conf file
here's what it is on apache
	Alias "/invites/" "/SparkleShare/invites/"