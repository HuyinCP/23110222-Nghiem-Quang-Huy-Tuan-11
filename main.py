import pygame
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from settings import Game
from algorithms_source.algorithm import *
from statics import *
from puzzleGrid import *
from puzzleApp import *

pygame.init()

game = Game()
FONT = pygame.font.SysFont("JetBrains Mono", 40)
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

def main():
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()