# receivers placed on the walls
class Receiver:
    def __init__(self, id="recID", x=0, y=0):
        self.id = id
        self.x = x
        self.y = y

    def printUnit(self):
        print("id={}    pos=({},{})".format(self.id, self.x, self.y))