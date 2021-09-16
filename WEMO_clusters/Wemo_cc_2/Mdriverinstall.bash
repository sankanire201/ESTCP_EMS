
vctl stop --tag MasterDriver

vctl remove --tag MasterDriver

python scripts/install-agent.py -s services/core/MasterDriverAgent -c services/core/MasterDriverAgent/master-driver.agent -t MasterDriver
vctl config store platform.driver registry_configs/csv_reg.csv ~/volttron/Config2/csv_reg.csv --csv 

#vctl config delete platform.driver devices/wemo_cc_2/Wp-60-L
#vctl config delete platform.driver devices/wemo_cc_2/Wp-61-L
#vctl config delete platform.driver devices/wemo_cc_2/Wp-62-L
#vctl config delete platform.driver devices/wemo_cc_2/Wp-63-L
#vctl config delete platform.driver devices/wemo_cc_2/Wp-52-L
#vctl config delete platform.driver devices/wemo_cc_2/Wp-53-L
#vctl config delete platform.driver devices/wemo_cc_2/Wp-54-L
#vctl config delete platform.driver devices/wemo_cc_2/Wp-55-L
#vctl config delete platform.driver devices/wemo_cc_2/Wp-59-L
#vctl config delete platform.driver devices/wemo_cc_2/Wp-58-L
		

vctl config store platform.driver devices/building540/wemo_cc_2/Wp-60-L ~/volttron/Config2/wemo_driver58.config
vctl config store platform.driver devices/building540/wemo_cc_2/Wp-61-L ~/volttron/Config2/wemo_driver106.config
vctl config store platform.driver devices/building540/wemo_cc_2/Wp-62-L ~/volttron/Config2/wemo_driver104.config
vctl config store platform.driver devices/building540/wemo_cc_2/Wp-63-L ~/volttron/Config2/wemo_driver139.config
vctl config store platform.driver devices/building540/wemo_cc_2/Wp-52-L ~/volttron/Config2/wemo_driver122.config
vctl config store platform.driver devices/building540/wemo_cc_2/Wp-53-L ~/volttron/Config2/wemo_driver74.config
vctl config store platform.driver devices/building540/wemo_cc_2/Wp-54-L ~/volttron/Config2/wemo_driver51.config
vctl config store platform.driver devices/building540/wemo_cc_2/Wp-55-L ~/volttron/Config2/wemo_driver141.config
vctl config store platform.driver devices/building540/wemo_cc_2/Wp-59-L ~/volttron/Config2/wemo_driver80.config
vctl config store platform.driver devices/building540/wemo_cc_2/Wp-58-L ~/volttron/Config2/wemo_driver137.config

vctl start --tag MasterDriver
