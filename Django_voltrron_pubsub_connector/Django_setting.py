topic_prefixes_to_watch = ['']

# Seconds between hearbeat publishes
heartbeat_period = 10

# Volttron address and keys used to create agents
agent_kwargs = {
    # Volttron VIP address
    'address': 'tcp://192.168.128.233:22916',

    # Required keys for establishing an encrypted VIP connection
    'secretkey': '8XzwYwamx5gQj_owyV5v4Jr3BESnJVnEn7UyA1WnAyc',
    'publickey': '6SJtrBlJlB7HMPZ8wGel97gpqLcuraIJQ71yPf85iTE',
    'serverkey': 'QOZaCWxkhn2qFALNoPnvwBZNgUgnTSU0KjrOBJFsKTg',

    # Don't use the configuration store
    'enable_store': True,
}


