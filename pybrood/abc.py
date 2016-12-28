from time import sleep
from . import inner


client = inner.client_instance
game = inner.game


def reconnect():
    while not client.connect():
        sleep(1)


def connection_checker():
    client.update()
    if not client.isConnected():
        print('Reconnecting...')
        reconnect()


class BaseAI:
    def prepare(self):
        pass

    def frame(self):
        raise NotImplementedError

    def finished(self):
        pass


def run(cls: BaseAI, once=False):
    print('Connecting...')
    reconnect()
    while True:
        print('Waiting to enter match...')
        while not game.isInGame():
            connection_checker()
        print('Starting match!')
        ai = cls()
        ai.prepare()
        while game.isInGame():
            ai.frame()
            connection_checker()
        ai.finished()
        print('Game ended')
        if once:
            break
