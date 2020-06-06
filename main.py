from browser import Browser
from tor import Tor
from sys import exit
from threading import Thread
from argparse import ArgumentParser
from os import path


class Views(Browser, Tor):
    def __init__(self, urllist, visits):
        self.urls = urllist
        self.visits = visits
        self.recentIPs = []
        self.alive = True
        self.views = {}
        self.bots = 5
        self.ip = None
        if self.urls == [] or self.urls is None:
            exit("Please provide valid number of urls")

        if self.visits is None or self.visits <= 0:
            exit("Please provide positive number of visits")

        for url in urllist:
            self.views[url] = 0

    def exit(self):
        self.alive = False
        self.stopTor()

    def connection(self):
        try:
            browser = self.createBrowser()
            browser.open('https://example.com', timeout=2.5)
            browser.close()
        except:
            print('[Error] Unable to access the internet')
            self.exit()

    def visit(self, url):
        try:
            if self.watch(url):
                print('Video Watch Success')
                views = self.views[url]
                self.views[url] = views + 1
            else:
                print('Video Watch Failed')

        except Exception as e:
            print(e)
        finally:
            self.bots -= 1

    def display(self, url):
        print('')
        print('  +------ Youtube Views ------+')
        print(f'  [-] Url: {url}')
        print(f'  [-] Proxy IP: {self.ip}')
        print(f'  [-] Visits: {self.views[url]}')

    def run(self):
        # In Python 3 dict.keys() returns an iterable but not indexable object.
        urls = list(self.views.keys())
        index = len(urls)
        while all([len(self.views), self.alive, index]):
            index -= 1
            self.startTor()
            self.getNewTorIP()
            print(f"New IP {self.ip}")
            if not self.ip:
                continue
            url = urls[index]
            print(f"Running for url {url}")
            if self.views[url] >= self.visits:
                del self.views[url]
                continue
            bots = []
            for _ in range(self.bots):
                thread = Thread(target=self.visit, args=[url])
                bots.append(thread)
                thread.start()
            for bot in bots:
                bot.join()
            self.display(urls[index])


if __name__ == '__main__':
    args = ArgumentParser()
    args.add_argument(
        'visits', help='The amount of visits ex: 300', type=int)
    args.add_argument('urls', help='Youtube videos url list',
                      nargs="+")
    args = args.parse_args()

    youtube_views = Views(args.urls, args.visits)

    # does tor exists?
    if not path.exists('/usr/sbin/tor'):
        try:
            print('Tor not installed on machine. Please install Tor First')
        finally:
            exit('Exiting ...')

    youtube_views.run()
