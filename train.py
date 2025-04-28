import tkinter as tk
from puzzleApp import PuzzleApp

def train():
    root = tk.Tk()
    app = PuzzleApp(root)
    app.train_models()  # Huấn luyện và lưu mô hình vào models.pkl
    root.destroy()

if __name__ == "__main__":
    train()