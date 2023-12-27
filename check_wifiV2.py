import time
import pywifi
from pywifi import const

wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]

def check_wifi_security():
    iface.scan()
    time.sleep(2)
    networks = iface.scan_results()
    
    print("Wi-Fi Networks:")
    for network in networks:
        ssid = network.ssid
        signal_strength = network.signal
        security, security_desc = get_security(network)
        band = get_band(network)
        channel = get_channel(network)
        frequency = get_frequency(network)
        bssid = network.bssid
        capabilities = get_capabilities(network)
        crowded = is_crowded(network)
        
        print(f"SSID: {ssid}, Signal Strength: {signal_strength}, Security: {security} - {security_desc}, Band: {band}, Channel: {channel}, Frequency: {frequency}, BSSID: {bssid}, Capabilities: {capabilities}, Crowded: {crowded}")

def get_security(network):
    if network.akm[0] == pywifi.const.AKM_TYPE_WPA:
        return "WPA", "provides better security than WEP. Initially designed to address WEP's weaknesses" #i totally made those info texts myself.
    elif network.akm[0] == pywifi.const.AKM_TYPE_WPA2:
        return "WPA2", "improved version of WPA, offering stronger encryption"
    elif network.akm[0] == pywifi.const.AKM_TYPE_WPAPSK:
        return "WPA-PSK", "commonly used for personal/home networks"
    elif network.akm[0] == pywifi.const.AKM_TYPE_WPA2PSK:
        return "WPA2-PSK", "commonly used for personal/home networks, upgraded V of wpa-psk"
    elif hasattr(const, 'AKM_TYPE_WEP') and network.akm[0] == const.AKM_TYPE_WEP: #same problem as in V1:/
        return "WEP", "An older, less secure protocol. vulnerable to various attacks"
    else:
        return "Open", "No Security (Unencrypted)"

def get_band(network):
    if hasattr(network, 'frequency'):
        if network.frequency > 4900:
            return "5GHz"
        elif network.frequency > 2400:
            return "2.4GHz"
        else:
            return "Unknown"

def get_channel(network):
    if hasattr(network, 'channel'):
        return network.channel
    return "Unknown"

def get_frequency(network):
    if hasattr(network, 'frequency'):
        return network.frequency
    return "Unknown"

def get_capabilities(network):
    if hasattr(network, 'capabilities'):
        return network.capabilities
    return "Unknown"

def is_crowded(network):
    return network.signal < -70  # doesnt work  in al sences:(

while True:
    check_wifi_security()
    time.sleep(5)