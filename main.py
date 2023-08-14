from Simulation import Simulation
from Game import Game
import random
import statistics


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    simulation = False

    if simulation:
        random.seed(1912)
        numSimulations = 1
        instance = 1
        turns = []

        while instance <= numSimulations:
            simulation = Simulation()
            simulation.simulate()
            turns.append(simulation.instance)
            instance += 1
            print(f'instance: {instance}, turns: {simulation.instance}')

        print(str(turns))
        print(f'Mean: {statistics.mean(turns)}')
        print(f'Variance: {statistics.variance(turns)}')

    if not simulation:
        game = Game()
        game.play()



