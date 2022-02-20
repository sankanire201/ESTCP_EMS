cp BEMS4.service /etc/systemd/system/ 
sudo chmod 644 /etc/systemd/system/BEMS4.service 
sudo systemctl daemon-reload 
sudo systemctl enable BEMS4.service 
sudo systemctl start BEMS4.service 
cp BEMS3.service /etc/systemd/system/ 
sudo chmod 644 /etc/systemd/system/BEMS3.service 
sudo systemctl daemon-reload 
sudo systemctl enable BEMS3.service 
sudo systemctl start BEMS3.service 
