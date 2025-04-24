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
from puzzleGrid import *

pygame.init()

game = Game()

FONT = pygame.font.SysFont("JetBrains Mono", 40)

GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

class ChartWindow:
    def __init__(self, comparison_results, selected_metrics):
        self.chart_window = tk.Toplevel()
        self.chart_window.title("Algorithm Comparison Charts")
        self.chart_window.geometry("600x600")
        self.chart_window.configure(bg="#f0f4f8")  # Màu nền nhẹ nhàng

        self.comparison_results = comparison_results
        self.selected_metrics = selected_metrics

        self.plot_comparison_chart()

    def plot_comparison_chart(self):
        if not self.comparison_results:
            return

        algorithms = [result["algorithm"] for result in self.comparison_results]
        steps = [result["steps"] for result in self.comparison_results]
        costs = [result["cost"] for result in self.comparison_results]
        times = [result["time"] for result in self.comparison_results]
        spaces = [result["space"] for result in self.comparison_results]

        # Chuẩn hóa dữ liệu để tỷ lệ tương đối
        def normalize(data):
            max_val = max(data)
            return [val / max_val if max_val != 0 else 0 for val in data]

        steps = normalize(steps)
        costs = normalize(costs)
        times = normalize(times)
        spaces = normalize(spaces)

        num_metrics = len(self.selected_metrics)
        if num_metrics == 0:
            return

        fig, ax = plt.subplots(figsize=(8, 6))

        x = np.arange(len(algorithms))

        # Line plot for each metric
        colors = {"Steps": "#4a90e2", "Cost": "#50c878", "Time": "#f5a623", "Space": "#e74c3c"}
        markers = {"Steps": "o", "Cost": "s", "Time": "D", "Space": "^"}
        for metric in self.selected_metrics:
            if metric == "Steps":
                ax.plot(x, steps, label="Steps (Normalized)", color=colors["Steps"], marker=markers["Steps"], linewidth=2)
            elif metric == "Cost":
                ax.plot(x, costs, label="Cost (Normalized)", color=colors["Cost"], marker=markers["Cost"], linewidth=2)
            elif metric == "Time":
                ax.plot(x, times, label="Time (s) (Normalized)", color=colors["Time"], marker=markers["Time"], linewidth=2)
            elif metric == "Space":
                ax.plot(x, spaces, label="Space (Normalized)", color=colors["Space"], marker=markers["Space"], linewidth=2)

        ax.set_title("Algorithm Performance Comparison (Normalized)", fontsize=14, pad=15)
        ax.set_xlabel("Algorithms", fontsize=12)
        ax.set_ylabel("Normalized Metrics", fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(algorithms, rotation=45, ha="right", fontsize=10)
        ax.legend(title="Metrics", fontsize=10)

        plt.grid(visible=True, linestyle="--", alpha=0.6)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)