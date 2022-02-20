"""
Agent documentation goes here.
"""

__docformat__ = 'reStructuredText'
import datetime
from datetime import datetime
import time
import logging
import sys
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Agent, Core, RPC

_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"


def peakShaverAgent(config_path, **kwargs):
    """Parses the Agent configuration and returns an instance of
    the agent created using that configuration.

    :param config_path: Path to a configuration file.

    :type config_path: str
    :returns: Peakshaveragent
    :rtype: Peakshaveragent
    """
    try:
        config = utils.load_config(config_path)
    except StandardError:
        config = {}

    if not config:
        _log.info("Using Agent defaults for starting configuration.")

    setting1 = int(config.get('setting1', 1))
    setting2 = config.get('setting2', "some/random/topic")

    return Peakshaveragent(setting1,
                          setting2,
                          **kwargs)


class Peakshaveragent(Agent):
    """
    Document agent constructor here.
    """

    def __init__(self, setting1=1, setting2="some/random/topic",
                 **kwargs):
        super(Peakshaveragent, self).__init__(**kwargs)
        _log.debug("vip_identity: " + self.core.identity)

        self.setting1 = setting1
        self.setting2 = setting2

        self.default_config = {"setting1": setting1,
                               "setting2": setting2}
        self.total_consumption=-10
        self.Peakshaverthreashhold=1000000


        #Set a default configuration to ensure that self.configure is called immediately to setup
        #the agent.
        
        self.vip.config.set_default("config", self.default_config)
        #Hook self.configure up to changes to the configuration file "config".
        self.vip.config.subscribe(self.configure, actions=["NEW", "UPDATE"], pattern="config")
        self.core.periodic(5,self.PeakShaver)
                 


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
            setting2 = config["setting2"]
        except ValueError as e:
            _log.error("ERROR PROCESSING CONFIGURATION: {}".format(e))
            return

        for x in self.setting2:
            self._create_subscriptions(str(x))
            print(str(x))
            

    def _create_subscriptions(self, topic):
        #Unsubscribe from everything.
        self.vip.pubsub.unsubscribe("pubsub", None, None)

        self.vip.pubsub.subscribe(peer='pubsub',
                                  prefix=topic,
                                  callback=self._handle_publish,all_platforms=True)

    def _handle_publish(self, peer, sender, bus, topic, headers,
                                message):
        now = utils.format_timestamp(datetime.utcnow())
        utcnow = utils.get_aware_utc_now()
 
        header = {
        #    headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            "Date": utils.format_timestamp(utcnow),
            "TimeStamp":utils.format_timestamp(utcnow)
        }
        
        x=topic.find('prioritygroupconsumption')
        if x>0:
            self.total_consumption=message["Total_group_sum"]
            topics = "analysis/Centralcontrol/Control/Pshaveerror/all"
            self.peak_shaving_error=self.total_consumption-self.Peakshaverthreashhold
            Message={"Peak_shaving_error":self.peak_shaving_error}
            result = self.vip.pubsub.publish(peer='pubsub',topic=topics, headers=header,message= Message)          
            print("***********************got it******************",self.total_consumption,self.Peakshaverthreashhold,self.peak_shaving_error)
        x=topic.find('PeakShaver')
        if x>0:
            print("***********************got it******************Pshaver",message)
            self.Peakshaverthreashhold=message[0]["Threashhold"]
            #print("***********************got it******************",self.Peakshaverthreashhold)
        x=topic.find("PriorityControl")
        if x>0:
            print("***********************got it******************GAMS",message)
            #result=self.vip.rpc.call('lPCBAgentagent-0.1_1','direct_load_control', message[0:-1])
            self.Peakshaverthreashhold=message[-1]
            topics = "devices/Centralcontrol/Control/GAMS_command/all"
            Message={"building_status":message[0:-1] ,"Shedding_Threashold":self.Peakshaverthreashhold}
            result = self.vip.pubsub.publish(peer='pubsub',topic=topics, headers=header,message= Message)          
            topics = "analysis/Centralcontrol/Control/GAMS_command/all"
            result = self.vip.pubsub.publish(peer='pubsub',topic=topics, headers=header,message= Message)
            print("########################################################################Power Consumption for Building############################", self.Priority_Consumption,self.Priority_group_Consumption,self.total_consumption)

            #print("***********************got it******************",self.Peakshaverthreashhold)


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
    def PeakShaver(self):
        now = utils.format_timestamp(datetime.utcnow())
        utcnow = utils.get_aware_utc_now()
 
        header = {
        #    headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            "Date": utils.format_timestamp(utcnow),
            "TimeStamp":utils.format_timestamp(utcnow)
        }

        
        shedding=self.total_consumption-self.Peakshaverthreashhold
        print("nnothing to shed*************************",shedding)
        if shedding >0:
            
           topics='control/plc/shedding'
           result = self.vip.pubsub.publish(peer='pubsub',topic=topics,message=shedding)
           print("PShaver_Start shedding*************************",shedding,self.Peakshaverthreashhold)
           topics = "devices/Centralcontrol/Control/Peakshaver/all"
           Message={"shedding":shedding ,"increment":0}
           result = self.vip.pubsub.publish(peer='pubsub',topic=topics, headers=header,message= Message)          

        if shedding > -50000 and shedding < -500:
            
           topics='control/plc/increment'
           result = self.vip.pubsub.publish(peer='pubsub',topic=topics,message=abs(shedding))
           print("PShaver_Start increment*************************",abs(shedding),self.Peakshaverthreashhold)
           topics = "devices/Centralcontrol/Control/Peakshaver/all"
           Message={"building_status":0 ,"Shedding_Threashold":abs(shedding)}
           result = self.vip.pubsub.publish(peer='pubsub',topic=topics, headers=header,message= Message)          



        else:
            print("nothing to shed*************************",shedding,self.Peakshaverthreashhold)

    @Core.receiver("onstop")
    def onstop(self, sender, **kwargs):
        """
        This method is called when the Agent is about to shutdown, but before it disconnects from
        the message bus.
        """
        pass

    @RPC.export
    def priority_control(self, arg1, kwarg1=None, kwarg2=None):
        """
        RPC method

        May be called from another agent via self.core.rpc.call """
        print("***********************got it******************GAMS",message)
        result=self.vip.rpc.call('lPCBAgentagent-0.1_1','direct_load_control', message[0:-1])
        self.Peakshaverthreashhold=message[-1]
        #print("***********************got it******************",self.Peakshaverthreashhold)

        return 1

def main():
    """Main method called to start the agent."""
    utils.vip_main(peakShaverAgent, 
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
