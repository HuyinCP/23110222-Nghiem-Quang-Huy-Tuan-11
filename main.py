import pygame
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from settings import Game
from algorithms_source.algorithm import *
from statics import *
from puzzleGrid import *
from puzzleApp import *

pygame.init()
game = Game()
FONT = pygame.font.SysFont("JetBrains Mono", 40)
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]


if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()