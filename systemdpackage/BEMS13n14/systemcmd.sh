cp BEMS14.service /etc/systemd/system/ 
sudo chmod 644 /etc/systemd/system/BEMS14.service 
sudo systemctl daemon-reload 
sudo systemctl enable BEMS14.service 
sudo systemctl start BEMS14.service 
cp BEMS13.service /etc/systemd/system/ 
sudo chmod 644 /etc/systemd/system/BEMS13.service 
sudo systemctl daemon-reload 
sudo systemctl enable BEMS13.service 
sudo systemctl start BEMS13.service 
