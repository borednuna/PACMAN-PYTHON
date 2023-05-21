from abc import ABC, abstractmethod

# abstract parent class for ghosts
class Ghost(ABC):
    # constructor
    def __init__(self, x_coord, y_coord, target, direct, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = x_coord + 22
        self.center_y = y_coord + 22
        self.target = target
        self.speed = 2
        self.direction = direct
        self.id = id
        self.is_dead = False
        self.is_in_box = True
        self.is_frightened = False
        self.is_eaten = False
        self.turns = [False, False, False, False]

    @abstractmethod
    def draw(self):
        pass

    def move(self):
        pass
