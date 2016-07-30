from time import sleep
import pybrood


def reconnect():
    while not pybrood.client.connect():
        sleep(1)


def connection_checker():
    pybrood.client.update()
    if not pybrood.client.is_connected():
        print('Reconnecting...')
        reconnect()


def debug_code():
    force = pybrood.game.get_force(0)
    print(force)
    print(force.id)
    print(force.name)
    pybrood.Force()


def main():
    print('Connecting...')
    reconnect()
    while True:
        print('Waiting to enter match...')
        while not pybrood.game.is_in_game():
            connection_checker()
        print('Starting match!')

        debug_code()

        while pybrood.game.is_in_game():
            # ...
            connection_checker()
        print('Game ended')


if __name__ == '__main__':
    main()
