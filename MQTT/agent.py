"""
Agent documentation goes here.
"""

__docformat__ = 'reStructuredText'

import logging
import sys
import os
import datetime
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Agent, Core, RPC
from paho.mqtt.client import MQTTv311, MQTTv31
import paho.mqtt.publish as publish
import paho.mqtt.client as paho
from paho.mqtt.subscribe import callback
from csv import DictReader, DictWriter
import csv
import collections
_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"



def mqttagent(config_path, **kwargs):
    """Parses the Agent configuration and returns an instance of
    the agent created using that configuration.

    :param config_path: Path to a configuration file.

    :type config_path: str
    :returns: Mqttagent
    :rtype: Mqttagent
    """
    try:
        config = utils.load_config(config_path)
    except StandardError:
        config = {}

    if not config:
        _log.info("Using Agent defaults for starting configuration.")

    setting1 = int(config.get('setting1', 1))
    setting2 = config.get('setting2', "some/random/topic")

    return Mqttagent(setting1,
                          setting2,
                          **kwargs)


def listen(client, userdata, message):
    global message1
    message1=message
    if message.topic=="devices/wemo_c/shed":
        pass
   	 
def connect(client, userdata, flags,rc):
    _log.debug("#######################MQTT client is connected###################")  

class Mqttagent(Agent):
    """
    Document agent constructor here.
    """

    def __init__(self, setting1=1, setting2="some/random/topic",
                 **kwargs):
        super(Mqttagent, self).__init__(**kwargs)
        _log.debug("vip_identity: " + self.core.identity)

        self.setting1 = setting1
        self.setting2 = setting2

        self.default_config = {"setting1": setting1,
                               "setting2": setting2}
        self.client1= paho.Client("MQQT_VOLTTRON_BRIDGE")
        self.client1.on_connect=connect
        self.client1.on_message=listen
        self.client1.connect("192.168.10.52",1886)
        self.client1.subscribe("devices/wemo_c/#")
        self.client1.publish("devices/wemo_c/w000",11)
        self.client1.loop_start()

        self.Read_Topics={}

        self.csv_path='/home/sanka/CENTRAL_CONTROL_UNIT/Read_Topic.csv'

        if os.path.isfile(self.csv_path):
       	 with open(self.csv_path, "r") as csv_device:
	     pass
             reader = DictReader(csv_device)
	         
         #iterate over the line of the csv
         
             for point in reader:
                     ##Rading the lines for configuration parameters
                     Topic = point.get("Topic")
                     
                     if Topic=='\t\t\t':
                         pass
                     else:
                         self.Read_Topics[Topic]=0
        else:
            # Device hasn't been created, or the path to this device is incorrect
            raise RuntimeError("CSV device at {} does not exist".format(self.csv_path))


        #Set a default configuration to ensure that self.configure is called immediately to setup
        #the agent.
        self.vip.config.set_default("config", self.default_config)
        #Hook self.configure up to changes to the configuration file "config".
        self.vip.config.subscribe(self.configure, actions=["NEW", "UPDATE"], pattern="config")
        self.core.periodic(10,self.Main_Worker)

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

        self.setting1 = setting1
        self.setting2 = setting2
        
        for x in self.setting2:
            self._create_subscriptions(str(x))

    def _create_subscriptions(self, topic):
        #Unsubscribe from everything.
        self.vip.pubsub.unsubscribe("pubsub", None, None)

        self.vip.pubsub.subscribe(peer='pubsub',
                                  prefix=topic,
                                  callback=self._handle_publish)
        #self.vip.pubsub.subscribe(peer='pubsub',
         #                         prefix='devices/Building540/Bay_area/solaredge86/all',
          #                        callback=self._handle_publish)
        #self.vip.pubsub.subscribe(peer='pubsub',
           #                       prefix='devices/Building540/Bay_area/solaredge87/all',
            #                      callback=self._handle_publish)

    def _handle_publish(self, peer, sender, bus, topic, headers,
                                message):
	x=topic.split('devices')
	new_topic='devices/acquisition'+x[1]
        self.client1.publish(new_topic,str(message))
        print(str(new_topic)+"######################Subscribe######################"+str(message))
        

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
    def Main_Worker(self):
        print("Main Worker is Working")
        #self.Read()
        self.Publish()
        self.Control()
        
    def Read(self):
        #THis function read the sql dtat base and the MQTT signals
        
        self.Read_sql()
        
    def Read_sql(self):
        for topic in self.Read_Topics:
            result=self.Read_Topic(topic)
            print(str(topic)+" : " +str(result))
        
    def Read_Topic(self,topic):
        end = str(datetime.datetime.utcnow()) 
        start = str(datetime.datetime.utcnow()+datetime.timedelta(minutes=-1))
        try:
            result=self.vip.rpc.call( 'platform.historian','query',topic,start,end, None, None,0,None,'LAST_TO_FIRST').get(timeout=30)
            return result.get('values',None)[0][1]
        except :
            print('***************read error ***************************')
            return "error"
    
    def Publish(self):
        self.Publish_to_MQTT()
        self.Publish_to_Volttron()
        self.Publish_to_Sql()
        
    def Publish_to_MQTT(self):
        pass
    
    def Publish_to_Volttron(self):
        pass
    
    def Publish_to_Sql(self):
        pass
    
    def Control(self):
        pass
    

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
    utils.vip_main(mqttagent, 
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
