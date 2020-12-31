CONFIGURATION = {
    "CONNECTIONS": {
        "ssid": "password",
    },
    "ADVERTISE_IP": '239.1.1.1',
    "ADVERTISE_PORT": 35550,
    "ADVERTISE_INTERVAL": 10,
    "DEPLOYER_PORT": 35551,
}

from bootstrap import bootstrap_in_thread

bootstrap_in_thread(CONFIGURATION)
