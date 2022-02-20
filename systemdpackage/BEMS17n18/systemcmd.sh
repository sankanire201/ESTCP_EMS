cp BEMS18.service /etc/systemd/system/ 
sudo chmod 644 /etc/systemd/system/BEMS18.service 
sudo systemctl daemon-reload 
sudo systemctl enable BEMS18.service 
sudo systemctl start BEMS18.service 
cp BEMS17.service /etc/systemd/system/ 
sudo chmod 644 /etc/systemd/system/BEMS17.service 
sudo systemctl daemon-reload 
sudo systemctl enable BEMS17.service 
sudo systemctl start BEMS17.service 
