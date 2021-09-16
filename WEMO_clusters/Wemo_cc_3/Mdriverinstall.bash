
vctl stop --tag MasterDriver

vctl remove --tag MasterDriver

python scripts/install-agent.py -s services/core/MasterDriverAgent -c services/core/MasterDriverAgent/master-driver.agent -t MasterDriver
vctl config store platform.driver registry_configs/csv_reg.csv ~/volttron/Config2/csv_reg.csv --csv 

#vctl config delete platform.driver devices/wemo_cc_3/Wp-57-L
#vctl config delete platform.driver devices/wemo_cc_3/Wp-40-L
		

vctl config store platform.driver devices/building540/wemo_cc_3/Wp-57-L ~/volttron/Config2/wemo_driver85.config
vctl config store platform.driver devices/building540/wemo_cc_3/Wp-40-L ~/volttron/Config2/wemo_driver52.config

vctl enable --tag MasterDriver
vctl start --tag MasterDriver
