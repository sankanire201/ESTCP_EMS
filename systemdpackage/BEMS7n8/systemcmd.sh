cp BEMS8.service /etc/systemd/system/ 
sudo chmod 644 /etc/systemd/system/BEMS8.service 
sudo systemctl daemon-reload 
sudo systemctl enable BEMS8.service 
sudo systemctl start BEMS8.service 
cp BEMS7.service /etc/systemd/system/ 
sudo chmod 644 /etc/systemd/system/BEMS7.service 
sudo systemctl daemon-reload 
sudo systemctl enable BEMS7.service 
sudo systemctl start BEMS7.service 
