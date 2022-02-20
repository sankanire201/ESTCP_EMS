cp BEMS2.service /etc/systemd/system/ 
sudo chmod 644 /etc/systemd/system/BEMS2.service 
sudo systemctl daemon-reload 
sudo systemctl enable BEMS2.service 
sudo systemctl start BEMS2.service 
cp BEMS1.service /etc/systemd/system/ 
sudo chmod 644 /etc/systemd/system/BEMS1.service 
sudo systemctl daemon-reload 
sudo systemctl enable BEMS1.service 
sudo systemctl start BEMS1.service 
