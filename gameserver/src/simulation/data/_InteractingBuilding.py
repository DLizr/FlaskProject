from src.simulation.data._Building import Building


class InteractingBuilding(Building):

    def update(self):
        raise NotImplementedError
    