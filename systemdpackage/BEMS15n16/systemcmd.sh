cp BEMS16.service /etc/systemd/system/ 
sudo chmod 644 /etc/systemd/system/BEMS16.service 
sudo systemctl daemon-reload 
sudo systemctl enable BEMS16.service 
sudo systemctl start BEMS16.service 
cp BEMS15.service /etc/systemd/system/ 
sudo chmod 644 /etc/systemd/system/BEMS15.service 
sudo systemctl daemon-reload 
sudo systemctl enable BEMS15.service 
sudo systemctl start BEMS15.service 
