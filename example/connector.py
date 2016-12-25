from time import sleep
import pybrood


client = pybrood.client_instance
game = pybrood.game


def reconnect():
    while not client.connect():
        sleep(1)


def connection_checker():
    client.update()
    if not client.isConnected():
        print('Reconnecting...')
        reconnect()


# TODO: Re-instantiate AI for every game


class BaseAI:
    def prepare(self):
        pass

    def frame(self):
        raise NotImplementedError

    def run(self):
        print('Connecting...')
        reconnect()
        while True:
            print('Waiting to enter match...')
            while not game.isInGame():
                connection_checker()
            print('Starting match!')
            self.prepare()
            while game.isInGame():
                self.frame()
                connection_checker()
            print('Game ended')


class TestAI(BaseAI):
    def prepare(self):
        force = game.getForce(0)
        print(force)
        print(force.getID())
        print(force.getName())

        units = game.getAllUnits()
        for u in units:
            print('Unit', u.getID(), u.getType().getName(), u.getPosition(), u.getTilePosition())

        game.print('suka')

    def frame(self):
        sleep(0.05)


if __name__ == '__main__':
    TestAI().run()
