class Game:
    """All the settings for the game in here kaka"""
    def __init__(self):
        self.WIDTH = 950
        self.HEIGHT = 350
        RES = (self.WIDTH, self.HEIGHT)
        self.GRID_SIZE = 3
        self.TILE_SIZE = 100
        self.GRID_X, self.GRID_Y = 20, 20
        self.FPS = 60
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.RED = (255, 0, 0)  #swap color


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]