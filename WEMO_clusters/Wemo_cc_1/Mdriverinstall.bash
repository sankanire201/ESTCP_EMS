
vctl stop --tag MasterDriver

vctl remove --tag MasterDriver

python scripts/install-agent.py -s services/core/MasterDriverAgent -c services/core/MasterDriverAgent/master-driver.agent -t MasterDriver
vctl config store platform.driver registry_configs/csv_reg.csv ~/volttron/Config2/csv_reg.csv --csv 

#vctl config delete platform.driver devices/wemo/w1
#vctl config delete platform.driver devices/wemo/w2
#vctl config delete platform.driver devices/wemo/w3
#vctl config delete platform.driver devices/wemo/w4
#vctl config delete platform.driver devices/wemo/w5
#vctl config delete platform.driver devices/wemo/w6
#vctl config delete platform.driver devices/wemo/w7
#vctl config delete platform.driver devices/wemo/w8
#vctl config delete platform.driver devices/wemo/w9
#vctl config delete platform.driver devices/wemo/w10
vctl config delete platform.driver devices/building540/wemo/w1		

vctl config store platform.driver devices/building540/wemo/w1 ~/volttron/Config2/wemo_driver2.config
vctl config store platform.driver devices/building540/wemo/w2 ~/volttron/Config2/wemo_driver12.config
vctl config store platform.driver devices/building540/wemo/w3 ~/volttron/Config2/wemo_driver8.config
vctl config store platform.driver devices/building540/wemo/w4 ~/volttron/Config2/wemo_driver7.config
vctl config store platform.driver devices/building540/wemo/w5 ~/volttron/Config2/wemo_driver9.config
vctl config store platform.driver devices/building540/wemo/w6 ~/volttron/Config2/wemo_driver13.config
vctl config store platform.driver devices/building540/wemo/w7 ~/volttron/Config2/wemo_driver18.config
vctl config store platform.driver devices/building540/wemo/w8 ~/volttron/Config2/wemo_driver15.config
vctl config store platform.driver devices/building540/wemo/w9 ~/volttron/Config2/wemo_driver5.config
vctl config store platform.driver devices/building540/wemo/w10 ~/volttron/Config2/wemo_driver11.config
vctl config store platform.driver devices/building540/wemo/w11 ~/volttron/Config2/wemo_driver93.config

vctl start --tag MasterDriver
