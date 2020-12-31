import _thread

import advertiser
import deployer
import machine


def _advertise_thread(advertise_ip, advertise_port, advertise_interval, deployer_port):
    unique_id = machine.unique_id()
    advertiser.run(
        advertise_ip, advertise_port, advertise_interval, unique_id, deployer_port
    )


def _deploy_thread(deployer_port):
    if deployer.run(deployer_port):
        machine.reset()


def bootstrap(configuration):
    import connector
    connector.connect(configuration["CONNECTIONS"])
    _thread.start_new_thread(_deploy_thread, (configuration["DEPLOYER_PORT"],))
    _thread.start_new_thread(
        _advertise_thread,
        (
            configuration["ADVERTISE_IP"],
            configuration["ADVERTISE_PORT"],
            configuration["ADVERTISE_INTERVAL"],
            configuration["DEPLOYER_PORT"]
        )
    )


def bootstrap_in_thread(configuration):
    _thread.start_new_thread(bootstrap, (configuration,))
