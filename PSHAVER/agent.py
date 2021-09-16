"""
Agent documentation goes here.
"""

__docformat__ = 'reStructuredText'

import logging
import sys
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Agent, Core, RPC

_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"


def pSHAVER(config_path, **kwargs):
    """Parses the Agent configuration and returns an instance of
    the agent created using that configuration.

    :param config_path: Path to a configuration file.

    :type config_path: str
    :returns: Pshaver
    :rtype: Pshaver
    """
    try:
        config = utils.load_config(config_path)
    except StandardError:
        config = {}

    if not config:
        _log.info("Using Agent defaults for starting configuration.")

    setting1 = int(config.get('setting1', 1))
    setting2 = config.get('setting2', "some/random/topic")

    return Pshaver(setting1,
                          setting2,
                          **kwargs)


class Pshaver(Agent):
    """
    Document agent constructor here.
    """

    def __init__(self, setting1=1, setting2="some/random/topic",
                 **kwargs):
        super(Pshaver, self).__init__(**kwargs)
        _log.debug("vip_identity: " + self.core.identity)

        self.setting1 = setting1
        self.setting2 = setting2

        self.default_config = {"setting1": setting1,
                               "setting2": setting2}
        self.loads_consumption={}
        self.total_consumption=0
        self.wind_power={}
        self.solar_power={}
        self.battery_power={}
        self.total_wind_power_generation=0
        self.total_solar_power_generation=0
        self.total_battery_storage=0
        self.total_available_generated_power=0


        #Set a default configuration to ensure that self.configure is called immediately to setup
        #the agent.
        self.vip.config.set_default("config", self.default_config)
        #Hook self.configure up to changes to the configuration file "config".
        self.vip.config.subscribe(self.configure, actions=["NEW", "UPDATE"], pattern="config")
        self.vip.config.subscribe(self.configure, actions=["NEW", "UPDATE"], pattern="config")

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
            print(str(x))
           

    def _create_subscriptions(self, topic):
        #Unsubscribe from everything.
        self.vip.pubsub.unsubscribe("pubsub", None, None)
        result=0
        result = topic.find('generation')
        
        if result >0:
            self.vip.pubsub.subscribe(peer='pubsub',
                              prefix=topic,
                              callback=self._handle_publish_generation)
            #print("#############found generation#################",str(topic))
        else:
            pass
        result=0
        result = topic.find('loads')
        if result >0:
            self.vip.pubsub.subscribe(peer='pubsub',
                              prefix=topic,
                              callback=self._handle_publish_loads)
            print("#############found loads#################",str(topic))
        else:
            pass
        result=0
        result = topic.find('storage')
        if result >0:
            self.vip.pubsub.subscribe(peer='pubsub',
                              prefix=topic,
                              callback=self._handle_publish_storage)
            #print("#############found storage#################",str(topic))
        else:
            pass


    def _handle_publish_generation(self, peer, sender, bus, topic, headers,
                                message):
        x=topic.find('wind')
        if x>0:
            wind_tag=topic.split("/")
            self.wind_power[wind_tag[-2]]=int((message[0])['inverter_output_power'])
            values_wind=self.wind_power.values()
            self.total_wind_power_generation=sum(values_wind)
        else:
            pass
        x=topic.find('solar')
        if x>0:
            solar_tag=topic.split("/")
            self.solar_power[solar_tag[-2]]=int((message[0])['AC_Power'])
            values_sloar=self.solar_power.values()
            self.total_solar_power_generation=sum(values_sloar)
           # print("###################################publish solar##################",str( self.solar_power[solar_tag[-2]]))
        else:
            pass
        self.total_available_generated_power=self.total_wind_power_generation+self.total_solar_power_generation
       
    
    def _handle_publish_loads(self, peer, sender, bus, topic, headers,
                                message):
        load_tag=topic.split("/")
        self.loads_consumption[load_tag[-2]]=int((message[0])['power'])/1000
        values=self.loads_consumption.values()
        self.total_consumption=sum(values)
       # print(str(load_tag[-2]),"###################################Power##################",str(total_consumption))
        
        
    def _handle_publish_storage(self, peer, sender, bus, topic, headers,
                            message):
        pass
       # print("###################################publish storage##################",str(topic))

   
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
        
        self.core.periodic(180,self.Main_Worker)
        #Exmaple RPC call
        #self.vip.rpc.call("some_agent", "some_method", arg1, arg2)
    def Main_Worker(self):
        self.threshhold=3000
        #print("##########################################################################toooo much",self.threshhold,self.total_consumption)
        if self.total_consumption>self.threshhold:
            print("##########################################################################toooo much",self.threshhold,self.total_consumption)
            self.vip.pubsub.publish('pubsub',"control/plc/shedding",message=int(total_consumption-self.threshhold))

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
    utils.vip_main(pSHAVER, 
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
