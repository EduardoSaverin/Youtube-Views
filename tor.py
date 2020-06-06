import urllib.request as request
from subprocess import getoutput as shell
from time import sleep
import requests
from stem import Signal
from stem.control import Controller
import os

# I am using socks5h as the protocol, instead of socks5. The request documentation mentions
# that using socks5h will make sure that DNS resolution happens over the proxy instead
# of on the client side.
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}


class Tor(object):
    def __init__(self):
        super().__init__()

    def getIP(self):
        url = 'https://api.ipify.org/?format=text'
        session = requests.session()
        session.proxies = proxies
        f = session.get(url, timeout=5)
        ip = f.text
        return ip

    def getNewTorIP(self, recurrence=3):
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password=os.getenv("TOR_PASSWORD"))
            controller.signal(Signal.NEWNYM)
            self.getNewIP(recurrence)

    def checkTorIsUp(self):
        if shell('curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/ | cat | grep -m 1 Congratulations | xargs').startswith('Congratulations'):
            print("Tor is running")
            return True
        else:
            print('Tor restart failed')
            return False

    def stopTor(self):
        shell('service tor stop')
        self.alive = False

    def startTor(self):
        # Ignore error if it is already running
        shell('service tor start')
        sleep(5)

    def getNewIP(self, recurrence):
        if not self.alive:
            self.exit()

        try:
            ip = self.getIP()
            if all([not ip, recurrence]):
                print("Network unreachable! Trying Again by restarting network manager")
                retry = 2
                while(retry):
                    ip = self.getIP()
                    if ip:
                        break
                    else:
                        shell('service network-manager restart')
                        sleep(1)
                if not ip:
                    self.getNewTorIP(recurrence-1)
            # If IP still not available and recurrence has exhausted, then first check internet connection
            if all([not self.ip, not recurrence]):
                self.connection()
            if ip not in self.recentIPs:
                self.ip = ip
                self.recentIPs.append(ip)
            else:
                print("Same IP detected restarting tor")
                self.getNewTorIP()
        except Exception as e:
            print(e)
