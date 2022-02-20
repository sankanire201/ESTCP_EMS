cp BEMS10.service /etc/systemd/system/ 
sudo chmod 644 /etc/systemd/system/BEMS10.service 
sudo systemctl daemon-reload 
sudo systemctl enable BEMS10.service 
sudo systemctl start BEMS10.service 
cp BEMS9.service /etc/systemd/system/ 
sudo chmod 644 /etc/systemd/system/BEMS9.service 
sudo systemctl daemon-reload 
sudo systemctl enable BEMS9.service 
sudo systemctl start BEMS9.service 
