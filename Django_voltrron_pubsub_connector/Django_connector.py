from datetime import datetime
import os
import sys


import gevent
import logging
from gevent.core import callback
from gevent import Timeout

from volttron.platform.messaging import headers as headers_mod
from volttron.platform.vip.agent import Agent, PubSub, Core
from volttron.platform.agent import utils

# Log warnings and errors to make the node red log less chatty
utils.setup_logging(level=logging.WARNING)
_log = logging.getLogger(__name__)

# These are the options that can be set from the settings module.
from Django_setting import agent_kwargs

''' takes two arguments.  Firist is topic to publish under.  Second is message. '''
if  __name__ == '__main__':
    try:
        # If stdout is a pipe, re-open it line buffered
        if utils.isapipe(sys.stdout):
            # Hold a reference to the previous file object so it doesn't
            # get garbage collected and close the underlying descriptor.
            stdout = sys.stdout
            sys.stdout = os.fdopen(stdout.fileno(), 'w', 1)

        agent = Agent(identity='DjangoPublisher', **agent_kwargs)
        now = utils.format_timestamp(datetime.utcnow())
        utcnow = utils.get_aware_utc_now()
        header = {
        #    headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            "Date": utils.format_timestamp(utcnow),
            "TimeStamp":utils.format_timestamp(utcnow)
        }
        Message= {"Test1": 1,"Test2":2,"Test3":3}
        
        event = gevent.event.Event()
        task = gevent.spawn(agent.core.run, event)
        with gevent.Timeout(10):
            event.wait()

        try:
            result = agent.vip.pubsub.publish(peer='pubsub',topic= 'devices/BMS/test/all',headers=header, message=Message)
            result.get(timeout=10)
            print("dooooo")
        finally:
            task.kill()
    except KeyboardInterrupt:
        pass
