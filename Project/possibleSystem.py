
class possibleSystem(object):

    def __init__(self, cost, reliability, edge_list):
        self.cost = cost
        self.reliability = reliability
        self.edge_list = edge_list

    def getCost(self):
        return self.cost

    def getReliability(self):
        return self.reliability