"""
Agent documentation goes here.
"""

__docformat__ = 'reStructuredText'

import logging
import sys
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Agent, Core, RPC
import schedule
import time
from datetime import datetime
from pprint import pformat
from csv import DictReader, DictWriter
import os
import csv
import collections
import operator
from collections import defaultdict
from dateutil import parser, tz
from dateutil.relativedelta import relativedelta

_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"


def scheduletest(config_path, **kwargs):
    """Parses the Agent configuration and returns an instance of
    the agent created using that configuration.

    :param config_path: Path to a configuration file.

    :type config_path: str
    :returns: Scheduletest
    :rtype: Scheduletest
    """
    try:
        config = utils.load_config(config_path)
    except StandardError:
        config = {}

    if not config:
        _log.info("Using Agent defaults for starting configuration.")

    setting1 = int(config.get('setting1', 1))
    setting2 = config.get('setting2', "some/random/topic")

    return Scheduletest(setting1,
                          setting2,
                          **kwargs)


class Scheduletest(Agent):
    """
    Document agent constructor here.
    """

    def __init__(self, setting1=1, setting2="some/random/topic",
                 **kwargs):
        super(Scheduletest, self).__init__(**kwargs)
        _log.debug("vip_identity: " + self.core.identity)

        self.setting1 = setting1
        self.setting2 = setting2

        self.default_config = {"setting1": setting1,
                               "setting2": setting2}
        self.current_hour_schedule_to_WeMo={}
        self.WeMo_list=[]
        self.WeMo_Topics={}
        self.WeMo_cc={}
        self.prev_hour=0
        self.field_count=0
        self.time_offset=0
        self.time_delta=5

        csv_path='/home/sanka/CENTRAL_CONTROL_UNIT/WeMo_schedule2.csv'
        csv_path_WeMo_Config='/home/sanka/CENTRAL_CONTROL_UNIT/WeMo_Config.csv'

        time_now=datetime.now()
        self.time_delta=1
        self.time_offset=time_now.hour
        if self.time_offset>=60:
                self.time_offset=self.time_delta
        if os.path.isfile(csv_path):
            with open(csv_path, "r") as csv_device:
             reader = DictReader(csv_device)
             csv_device.seek(0,0)
            #iterate over the line of the csv
             self.H={}
             
             for point in reader:
                     ##Rading the lines for configuration parameters
                    csv_device.seek(0,0)
                    for point in reader:
                     ##Rading the lines for configuration parameters
                        
                        wemo=point.get("WeMo")
                        if wemo == '' or wemo == "WeMo":
                            pass
                        else:
                            self.WeMo_list.append(wemo)
             print(self.WeMo_list)
                 
             for hours in range(0,24):
                 WeMo=[]
                 csv_device.seek(0,0)
                 reader = DictReader(csv_device)
                 for point in reader:
                     ##Rading the lines for configuration parameters
                     if point.get(str(hours)) == '':
                        pass
                     else:
                        WeMo.append(point.get(str(hours)))
                 self.H[hours]=WeMo
        else:
        # Device hasn't been created, or the path to this device is incorrect
            raise RuntimeError("CSV device at {} does not exist".format(csv_path))

        if os.path.isfile(csv_path_WeMo_Config):
       	 with open(csv_path_WeMo_Config, "r") as csv_device:
	     pass
             reader2 = DictReader(csv_device)
	         
         #iterate over the line of the csv
         
             for point in reader2:
                     ##Rading the lines for configuration parameters
                     Name = point.get("Name")
                     Building = point.get("Building")
                     Cluster_Controller = point.get("cc")

                     #This is the topic that use for RPC call
                     Topic="acquisition/loads/"+"building"+Cluster_Controller+"/"+Name
                     if Name=='\t\t\t':
                         pass
                     else:
                         Name=Name+"_"+Cluster_Controller
                         self.WeMo_Topics[Name]=Topic
                         self.WeMo_cc[Name]=Cluster_Controller
                                                    
                     
        else:
            # Device hasn't been created, or the path to this device is incorrect
            raise RuntimeError("CSV device at {} does not exist".format(self.csv_path))
        #Set a default configuration to ensure that self.configure is called immediately to setup



        #Set a default configuration to ensure that self.configure is called immediately to setup
        #the agent.
        self.vip.config.set_default("config", self.default_config)
        #Hook self.configure up to changes to the configuration file "config".
        self.vip.config.subscribe(self.configure, actions=["NEW", "UPDATE"], pattern="config")
	schedule.every(1).minutes.do(self.dowork)
	self.core.periodic(2,self.mainworker)

    def configure(self, config_name, action, contents):
        """
        Called after the Agent has connected to the message bus. If a configuration exists at startup
        this will be called before onstart.

        Is called every time the configuration in the store changes.
        """
        config = self.default_config.copy()
        config.update(contents)

        _log.debug("Configuring Agent")

        try:
            setting1 = int(config["setting1"])
            setting2 = str(config["setting2"])
        except ValueError as e:
            _log.error("ERROR PROCESSING CONFIGURATION: {}".format(e))
            return

        self.setting1 = setting1
        self.setting2 = setting2

        self._create_subscriptions(self.setting2)

    def _create_subscriptions(self, topic):
        #Unsubscribe from everything.
        self.vip.pubsub.unsubscribe("pubsub", None, None)

        self.vip.pubsub.subscribe(peer='pubsub',
                                  prefix=topic,
                                  callback=self._handle_publish)

    def _handle_publish(self, peer, sender, bus, topic, headers,
                                message):
        pass

    @Core.receiver("onstart")
    def onstart(self, sender, **kwargs):
        """
        This is method is called once the Agent has successfully connected to the platform.
        This is a good place to setup subscriptions if they are not dynamic or
        do any other startup activities that require a connection to the message bus.
        Called after any configurations methods that are called at startup.

        Usually not needed if using the configuration store.
        """
        #Example publish to pubsub
        #self.vip.pubsub.publish('pubsub', "some/random/topic", message="HI!")

        #Exmaple RPC call
        #self.vip.rpc.call("some_agent", "some_method", arg1, arg2)
    def dowork(self):
	print("#################################################I am at work################################################",self.field_count)
	temp=[]
	time_now=datetime.now()
       
        self.field_count=self.field_count+1
        if self.field_count==24:
            self.field_count=0
        temp=list(self.H[self.field_count])
        
        
	for x in self.WeMo_list:
                 print('\y\n',x)
                 if x in temp:
                     self.current_hour_schedule_to_WeMo[x]=1
                 else:
                     self.current_hour_schedule_to_WeMo[x]=0
        print(x)
        temp=[]

        
        utcnow = utils.get_aware_utc_now()
        
        Header= {
    # python code to get this is
    # from datetime import datetime
    # from volttron.platform.messaging import headers as header_mod
    # from volttron.platform.agent import utils
    # now = utils.format_timestamp( datetime.utcnow())
    # {
    #     headers_mod.DATE: now,
    #     headers_mod.TIMESTAMP: now
    # }
         "Date": utils.format_timestamp(utcnow),
         "TimeStamp":utils.format_timestamp(utcnow)
        }

        #headers['time'] = utils.format_timestamp(utcnow)
       # Message={"Total_WeMo_Consumption": {"Readings": [utils.format_timestamp(utcnow),total],"Units": "Kw","tz": "UTC","data_type": "int"}}
        Message=self.current_hour_schedule_to_WeMo
        print("#######################################Publishig Wemo scheduleeeeeeeeeeeeee#########################")
        self.vip.pubsub.publish('pubsub',"Wemo_Schedule",headers=Header,message=Message)
       
        
        for x in self.current_hour_schedule_to_WeMo:
                    result=self.Send_Schedule_WeMO(x,self.current_hour_schedule_to_WeMo[x])
                   #result=5
                    if result==0 or result==11:
                        pass
                    else :
                        temp.append(x)
        for y in temp:
                    print("#######################################deleting requests to cluster controller for ##########################"+str(y))
                    del self.current_hour_schedule_to_WeMo[y]
                    print(self.current_hour_schedule_to_WeMo)


                    
    def Send_Schedule_WeMO(self,WeMo,Status):
        try:
            EP='WeMo_cc_'+self.WeMo_cc[WeMo]
            print("sending requests to cluster controller for "+EP)
            result=self.vip.rpc.call('platform.driver','set_point', self.WeMo_Topics[WeMo],'status',Status,external_platform=EP).get(timeout=20)
            #result=self.vip.rpc.call('platform.driver','get_point', self.WeMo_Topics[WeMo],'status',external_platform='WeMo_cc_1').get(timeout=60)
	    #print(result)
            if result['status']==11:
                print('Wemo is not responded')
                return 0
            else:
                #del self.WeMo_Scheduled_Status[WeMo]
                #print(self.WeMo_Scheduled_Status)
                return WeMo
        except:
            print("somthing happend")
            return 0
        return 1
        
    def mainworker(self):
	schedule.run_pending()

    @Core.receiver("onstop")
    def onstop(self, sender, **kwargs):
        """
        This method is called when the Agent is about to shutdown, but before it disconnects from
        the message bus.
        """
        pass

    @RPC.export
    def rpc_method(self, arg1, arg2, kwarg1=None, kwarg2=None):
        """
        RPC method

        May be called from another agent via self.core.rpc.call """
        return self.setting1 + arg1 - arg2

def main():
    """Main method called to start the agent."""
    utils.vip_main(scheduletest, 
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
