
import os
import shutil
k=0
for k in range(1,10):
    path = os.path.join("./", "BEMS"+str(2*k-1)+"n"+str(2*k))
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path,0o666,)
    f2 = open("BEMS"+str(2*k-1)+"n"+str(2*k)+"\systemcmd.sh", "a")
    f2.truncate(0)
 
    for j in range (0,2):
    
        f = open("BEMS"+str(2*k-1)+"n"+str(2*k)+"\BEMS"+str(2*k-j)+".service", "a")
        f.truncate(0)
        f.write("[Unit] \n")
        f.write("Description=BEMS"+str(k)+" Platform Service \n")
        f.write("After=systemd-networkd-wait-online.service \nWants=systemd-networkd-wait-online.service\n \n")


        f.write("[Service] \n")
        f.write("Type=simple \n")

        #Change this to the user that VOLTTRON will run as.
        f.write("User=pi \n")
        #Group=volttron

        #Uncomment and change this to specify a different VOLTTRON_HOME
        f.write("Environment=\"VOLTTRON_HOME=/home/pi/.BEMS_"+str(2*k-j)+"\"\n")

        #Change these to settings to reflect the install location of VOLTTRON
        f.write("WorkingDirectory=/home/pi/volttron \n")
        f.write("ExecStart=/home/pi/volttron/env/bin/volttron -vv \n")
        f.write("ExecStop=/home/pi/volttron/env/bin/volttron-ctl shutdown --platform \n \n")

        f.write("[Install] \n")
        f.write("WantedBy=multi-user.target \n")

        f.close()
        
        f2.write("cp BEMS"+str(2*k-j)+".service " "/etc/systemd/system/ \n")
        f2.write("sudo chmod 644 /etc/systemd/system/BEMS"+str(2*k-j)+".service \n")
        f2.write("sudo systemctl daemon-reload \n")
        f2.write("sudo systemctl enable BEMS"+str(2*k-j)+".service \n")
        f2.write("sudo systemctl start BEMS"+str(2*k-j)+".service \n")
        
    f2.close()
        
        
























        
        
