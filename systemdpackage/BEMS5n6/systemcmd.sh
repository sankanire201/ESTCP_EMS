cp BEMS6.service /etc/systemd/system/ 
sudo chmod 644 /etc/systemd/system/BEMS6.service 
sudo systemctl daemon-reload 
sudo systemctl enable BEMS6.service 
sudo systemctl start BEMS6.service 
cp BEMS5.service /etc/systemd/system/ 
sudo chmod 644 /etc/systemd/system/BEMS5.service 
sudo systemctl daemon-reload 
sudo systemctl enable BEMS5.service 
sudo systemctl start BEMS5.service 
