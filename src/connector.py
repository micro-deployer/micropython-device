def _connect(interface, ssid, password, timeout_ms):
    import time
    import machine

    interface.connect(ssid, password)
    t0 = time.ticks_ms()
    while not interface.isconnected():
        if time.ticks_diff(time.ticks_ms(), t0) > timeout_ms:
            raise Exception('Timeout')
        machine.idle()
    return


def _connect_somewhere(connections):
    import sys
    import network

    sta_if = network.WLAN(network.STA_IF)

    sta_if.active(True)

    wifi_networks = sta_if.scan()
    wifi_ssids = {ssid.decode() for ssid, *_ in wifi_networks}
    print('WiFi found:', wifi_ssids)

    for ssid, password in connections.items():
        if ssid in wifi_ssids:
            print('Connecting:', ssid)
            try:
                _connect(sta_if, ssid, password, 10000)
            except Exception as exc:
                sys.print_exception(exc)
                print('Connecting error:', ssid)
                continue

            print('Connecting sucessful:', ssid)
            return sta_if

    sta_if.active(False)
    raise Exception("Can't connect")


def connect(connections):
    interface = _connect_somewhere(connections)
    ssid = interface.config('essid')
    mac_addr = interface.config('mac')
    ifconfig = interface.ifconfig()
    print('Connected to WiFi', ssid, 'MAC', mac_addr, "ifconfig", ifconfig)
