cp BEMS12.service /etc/systemd/system/ 
sudo chmod 644 /etc/systemd/system/BEMS12.service 
sudo systemctl daemon-reload 
sudo systemctl enable BEMS12.service 
sudo systemctl start BEMS12.service 
cp BEMS11.service /etc/systemd/system/ 
sudo chmod 644 /etc/systemd/system/BEMS11.service 
sudo systemctl daemon-reload 
sudo systemctl enable BEMS11.service 
sudo systemctl start BEMS11.service 
