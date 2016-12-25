from time import sleep
from pybrood import BaseAI, run, game, Color


class HelloAI(BaseAI):
    def prepare(self):
        force = game.getForce(0)
        print(force)
        print(force.getID())
        print(force.getName())

        units = game.getAllUnits()
        for u in units:
            print('Unit', u.getID(), u.getType().getName(), u.getPosition(), u.getTilePosition())

        game.print('Hello world!')

        print(Color(255, 0, 0).getName())

    def frame(self):
        sleep(0.05)


if __name__ == '__main__':
    run(HelloAI)
