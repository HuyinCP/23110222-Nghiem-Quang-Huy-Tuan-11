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

# pygame.init()
# game = Game()
FONT = pygame.font.SysFont("JetBrains Mono", 40)
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]


class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.root.geometry(f"{game.WIDTH +200}x{game.HEIGHT + 400}")  # Tăng kích thước cửa sổ
        self.root.configure(bg="#f0f4f8")
        self.root.resizable(False, False)  # Không cho phép thay đổi kích thước
        self.root.overrideredirect(False)  # Tắt chế độ toàn màn hình

        # Gradient background
        self.canvas = tk.Canvas(self.root, width=game.WIDTH + 200, height=game.HEIGHT + 400, highlightthickness=0, bg="#f0f4f8")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_rectangle(0, 0, game.WIDTH + 200, game.HEIGHT + 400,
                                    fill="#e6ecf0", outline="")
        self.canvas.create_rectangle(0, 0, game.WIDTH + 200, 250,
                                    fill="#d3e0ea", outline="")

        self.initial_state = [1, 2, 3, 4, 5, 6, 0, 7, 8]
        self.result = None
        self.step = 0
        self.last_step_time = time.time()
        self.animation_progress = 1.0
        self.animation_duration = 0.15
        self.comparison_results = []

        self.main_frame = tk.Frame(self.canvas, bg="#ffffff", bd=2, relief="raised")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=game.WIDTH + 160, height=game.HEIGHT + 360)
        self.canvas.create_rectangle(20, 20, game.WIDTH + 180, game.HEIGHT + 380,
                                    fill="", outline="#b0c4de", width=2)

        self.grid_frame = tk.Frame(self.main_frame, bg="#ffffff", bd=2, relief="groove")
        self.grid_frame.pack(side=tk.LEFT, padx=20, pady=20)
        self.grid_width = game.GRID_X * 2 + game.GRID_SIZE * game.TILE_SIZE
        self.grid_height = game.GRID_Y * 2 + game.GRID_SIZE * game.TILE_SIZE
        self.puzzle_grid = PuzzleGrid(self.grid_width, self.grid_height)
        self.grid_label = tk.Label(self.grid_frame, bg="#ffffff", bd=0)
        self.grid_label.pack(padx=10, pady=10)

        self.control_frame = tk.Frame(self.main_frame, bg="#ffffff", bd=2, relief="groove")
        self.control_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill="y", expand=True)

        self.header_label = tk.Label(self.control_frame, text="8-Puzzle Solver", font=("JetBrains Mono", 18, "bold"),
                                   bg="#d3e0ea", fg="#2c3e50", pady=10)
        self.header_label.pack(fill="x")

        self.input_frame = tk.Frame(self.control_frame, bg="#ffffff")
        self.input_frame.pack(pady=(10, 5), padx=10, fill="x")
        self.input_label = tk.Label(self.input_frame, text="Initial State (0-8)", font=("JetBrains Mono", 12, "bold"),
                                  bg="#ffffff", fg="#34495e")
        self.input_label.pack(anchor="w", pady=(0, 5))

        self.input_grid = []
        for i in range(3):
            row = []
            frame_row = tk.Frame(self.input_frame, bg="#ffffff")
            frame_row.pack(fill="x")
            for j in range(3):
                entry = ttk.Entry(frame_row, width=5, font=("JetBrains Mono", 12), justify="center", style="Custom.TEntry")
                entry.insert(0, str(self.initial_state[i * 3 + j]))
                entry.pack(side=tk.LEFT, padx=5, pady=5)
                row.append(entry)
            self.input_grid.append(row)

        self.chart_selection_frame = tk.Frame(self.control_frame, bg="#ffffff")
        self.chart_selection_frame.pack(pady=(5, 5), padx=10, fill="x")
        self.chart_label = tk.Label(self.chart_selection_frame, text="Select Charts to Display",
                                  font=("JetBrains Mono", 12, "bold"), bg="#ffffff", fg="#34495e")
        self.chart_label.pack(anchor="w", pady=(0, 5))

        self.chart_vars = {
            "Steps": tk.BooleanVar(value=True),
            "Cost": tk.BooleanVar(value=True),
            "Time": tk.BooleanVar(value=True),
            "Space": tk.BooleanVar(value=True)
        }
        for metric, var in self.chart_vars.items():
            chk = ttk.Checkbutton(self.chart_selection_frame, text=metric, variable=var, style="Custom.TCheckbutton")
            chk.pack(anchor="w", padx=5, pady=2)

        self.button_frame = tk.Frame(self.control_frame, bg="#ffffff")
        self.button_frame.pack(pady=10, padx=10)
        style = ttk.Style()
        style.configure("Custom.TButton", font=("JetBrains Mono", 10, "bold"), padding=8,
                       background="#4a90e2", foreground="black")
        style.map("Custom.TButton",
                 background=[('active', '#357abd')],
                 foreground=[('active', 'red')])

        buttons = [
            ("BFS", self.run_bfs), 
            ("DFS", self.run_dfs), 
            ("IDS", self.run_ids), 
            ("UCS", self.run_ucs),
            ("A*", self.run_astar), 
            ("IDA*", self.run_idastar), 
            ("Hill Climb", self.run_hillclimbing),
            ("Reset", self.reset), 
            ("SimuAnnealing", self.run_simulated_annealing),
            ("BeamSearch", self.run_beam_search), 
            ("AND-OR", self.run_andor_search), 
            ("Compare", self.compare_algorithms)
        ]

        for i, (text, cmd) in enumerate(buttons):
            btn = ttk.Button(self.button_frame, text=text, command=cmd, style="Custom.TButton")
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5, sticky="ew")

        self.status_label = tk.Label(self.control_frame, text="NGHIEM QUANG HUY - 23110222",
                                   font=("JetBrains Mono", 12, "italic"), bg="#ffffff", fg="#7f8c8d")
        self.status_label.pack(pady=10)

        self.table_frame = tk.Frame(self.control_frame, bg="#ecf0f1", bd=2, relief="sunken")
        self.table_frame.pack(pady=10, padx=10, fill="x")
        style.configure("Custom.Treeview", font=("JetBrains Mono", 10), rowheight=25,
                       background="3498db", fieldbackground="#ecf0f1")
        style.configure("Custom.Treeview.Heading", font=("JetBrains Mono", 10, "bold"),
                       background="#3498db", foreground="black")
        self.tree = ttk.Treeview(self.table_frame, columns=("Algorithm", "Steps", "Cost", "Time", "Space"),
                               show="headings", height=10, style="Custom.Treeview")
        self.tree.heading("Algorithm", text="Algorithm")
        self.tree.heading("Steps", text="Steps")
        self.tree.heading("Cost", text="Cost")
        self.tree.heading("Time", text="Time (s)")
        self.tree.heading("Space", text="Space")
        self.tree.column("Algorithm", width=100, anchor="center")
        self.tree.column("Steps", width=60, anchor="center")
        self.tree.column("Cost", width=60, anchor="center")
        self.tree.column("Time", width=80, anchor="center")
        self.tree.column("Space", width=80, anchor="center")
        self.tree.pack(fill="x", padx=5, pady=5)

        # Conclusion frame
        self.conclusion_frame = tk.Frame(self.control_frame, bg="#ffffff", bd=2, relief="groove")
        self.conclusion_frame.pack(pady=10, padx=10, fill="x")
        self.conclusion_label = tk.Label(
            self.conclusion_frame,
            text="Conclusion: Select an algorithm and click Compare to see the evaluation.",
            font=("JetBrains Mono", 10, "italic"),
            bg="#ffffff",
            fg="#7f8c8d",
            wraplength=350,
            justify="left"
        )
        self.conclusion_label.pack(anchor="w", padx=5, pady=5)

        style.configure("Custom.TEntry", fieldbackground="#ecf0f1", borderwidth=1, padding=5,
                       foreground="#2c3e50")
        style.map("Custom.TEntry", fieldbackground=[('focus', '#d5e8f1')])
        style.configure("Custom.TCheckbutton", background="#ffffff", foreground="#34495e",
                       font=("JetBrains Mono", 10))
        style.map("Custom.TCheckbutton", background=[('active', 'red')])

        self.update()

    def update(self):
        if self.result and self.step < len(self.result["path"]):
            current_time = time.time()
            elapsed = current_time - self.last_step_time
            self.animation_progress = min(elapsed / self.animation_duration, 1.0)
            self.puzzle_grid.draw(self.result["path"][self.step], 
                                self.result["path"][self.step - 1] if self.step > 0 else None, 
                                self.animation_progress)
            self.status_label.config(text=f"Step {self.step}/{len(self.result['path'])-1}")
            if self.animation_progress >= 1.0 and self.step < len(self.result["path"]) - 1:
                self.step += 1
                self.last_step_time = current_time
                self.animation_progress = 0.0
        else:
            self.puzzle_grid.draw(tuple(self.initial_state))
            self.status_label.config(text="Algorithm Details Table")

        pygame_image = pygame.image.tostring(self.puzzle_grid.get_surface(), "RGB")
        pil_image = Image.frombytes("RGB", (self.grid_width, self.grid_height), pygame_image)
        tk_image = ImageTk.PhotoImage(pil_image)
        self.grid_label.configure(image=tk_image)
        self.grid_label.image = tk_image
        self.root.after(16, self.update)

    def run_algorithm(self, algorithm, algo_name):
        try:
            nums = []
            for i in range(3):
                for j in range(3):
                    value = self.input_grid[i][j].get()
                    if not value.isdigit() or int(value) < 0 or int(value) > 8:
                        messagebox.showerror("Error", "Each cell must contain a number between 0 and 8!")
                        return None
                    nums.append(int(value))

            if len(set(nums)) != 9:
                messagebox.showerror("Error", "Numbers must be unique (0-8)!")
                return None

            if len(nums) != 9 or not is_solvable(tuple(nums)):
                messagebox.showerror("Error", "Invalid or unsolvable puzzle!")
                return None

            self.initial_state = nums
            self.status_label.config(text=f"Running {algo_name}...")
            self.root.update()
            result = algorithm(tuple(self.initial_state))
            self.status_label.config(text="Algorithm Details Table")

            if not result:
                messagebox.showerror("Error", f"No solution found for {algo_name}!")
                return None

            self.result = result
            self.step = 0
            self.last_step_time = time.time()
            self.animation_progress = 0.0

            return {
                "algorithm": algo_name,
                "steps": result["steps"],
                "cost": result["cost"],
                "time": result["time"],
                "space": result["space"]
            }

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input or error in {algo_name}: {str(e)}")
            return None

    def run_bfs(self):
        result = self.run_algorithm(bfs, "BFS")
        if result:
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=(
                result["algorithm"],
                result["steps"],
                result["cost"],
                f"{result['time']:.4f}",
                result["space"]
            ))

    def run_dfs(self):
        result = self.run_algorithm(dfs, "DFS")
        if result:
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=(
                result["algorithm"],
                result["steps"],
                result["cost"],
                f"{result['time']:.4f}",
                result["space"]
            ))

    def run_ids(self):
        result = self.run_algorithm(ids, "IDS")
        if result:
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=(
                result["algorithm"],
                result["steps"],
                result["cost"],
                f"{result['time']:.4f}",
                result["space"]
            ))

    def run_ucs(self):
        result = self.run_algorithm(ucs, "UCS")
        if result:
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=(
                result["algorithm"],
                result["steps"],
                result["cost"],
                f"{result['time']:.4f}",
                result["space"]
            ))

    def run_astar(self):
        result = self.run_algorithm(a_star, "A*")
        if result:
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=(
                result["algorithm"],
                result["steps"],
                result["cost"],
                f"{result['time']:.4f}",
                result["space"]
            ))

    def run_idastar(self):
        result = self.run_algorithm(ida_star, "IDA*")
        if result:
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=(
                result["algorithm"],
                result["steps"],
                result["cost"],
                f"{result['time']:.4f}",
                result["space"]
            ))

    def run_hillclimbing(self):
        result = self.run_algorithm(hill_climbing, "Hill Climb")
        if result:
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=(
                result["algorithm"],
                result["steps"],
                result["cost"],
                f"{result['time']:.4f}",
                result["space"]
            ))

    def run_simulated_annealing(self):
        result = self.run_algorithm(simulated_annealing, "SimuAnnealing")
        if result:
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=(
                result["algorithm"],
                result["steps"],
                result["cost"],
                f"{result['time']:.4f}",
                result["space"]
            ))

    def run_beam_search(self):
        result = self.run_algorithm(beam_search, "BeamSearch")
        if result:
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=(
                result["algorithm"],
                result["steps"],
                result["cost"],
                f"{result['time']:.4f}",
                result["space"]
            ))

    def run_andor_search(self):
        result = self.run_algorithm(and_or_search, "AND-OR")
        if result:
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=(
                result["algorithm"],
                result["steps"],
                result["cost"],
                f"{result['time']:.4f}",
                result["space"]
            ))

    def generate_conclusion(self):
        if not self.comparison_results:
            return "Conclusion: No results to evaluate. Run Compare to see the evaluation."

        # Find best algorithms based on metrics
        optimal_steps = min(result["steps"] for result in self.comparison_results)
        min_space = min(result["space"] for result in self.comparison_results)
        min_time = min(result["time"] for result in self.comparison_results)

        optimal_algorithms = [
            result["algorithm"] for result in self.comparison_results
            if result["steps"] == optimal_steps
        ]
        space_efficient_algorithms = [
            result["algorithm"] for result in self.comparison_results
            if result["space"] == min_space
        ]
        time_efficient_algorithms = [
            result["algorithm"] for result in self.comparison_results
            if result["time"] == min_time
        ]

        # General analysis based on steps (indicating problem complexity)
        avg_steps = sum(result["steps"] for result in self.comparison_results) / len(self.comparison_results)
        problem_complexity = "simple" if avg_steps <= 5 else "moderate" if avg_steps <= 15 else "complex"

        conclusion = "Conclusion:\n"
        conclusion += f"- Problem Complexity: {problem_complexity.capitalize()} (average {avg_steps:.1f} steps).\n"

        # Optimal path (Steps/Cost)
        conclusion += f"- For shortest path: {', '.join(optimal_algorithms)} achieved optimal steps ({optimal_steps}).\n"
        if problem_complexity == "simple":
            conclusion += "  BFS, UCS, A*, IDA*, IDS are reliable for simple puzzles.\n"
        else:
            conclusion += "  A*, IDA*, AND-OR are better for complex puzzles due to heuristic guidance.\n"

        # Space efficiency
        conclusion += f"- For memory efficiency: {', '.join(space_efficient_algorithms)} used least space ({min_space}).\n"
        if min_space <= 5:
            conclusion += "  IDA*, AND-OR, Hill Climb, Simulated Annealing are ideal for low-memory scenarios.\n"

        # Time efficiency
        conclusion += f"- For speed: {', '.join(time_efficient_algorithms)} were fastest ({min_time:.4f}s).\n"
        if problem_complexity == "simple":
            conclusion += "  Hill Climb, Simulated Annealing, Beam Search are fast for simple puzzles.\n"
        else:
            conclusion += "  A*, IDA*, AND-OR are faster for complex puzzles with heuristic optimization.\n"

        # Overall recommendation
        if problem_complexity == "simple":
            conclusion += "- Recommendation: Use BFS or A* for guaranteed optimal path, or Hill Climb for speed.\n"
        elif problem_complexity == "moderate":
            conclusion += "- Recommendation: Use A* or IDA* for a balance of speed and optimality.\n"
        else:
            conclusion += "- Recommendation: Use IDA* or AND-OR for complex puzzles with limited memory.\n"

        return conclusion

    def compare_algorithms(self):
        try:
            nums = []
            for i in range(3):
                for j in range(3):
                    value = self.input_grid[i][j].get()
                    if not value.isdigit() or int(value) < 0 or int(value) > 8:
                        messagebox.showerror("Error", "Each cell must contain a number between 0 and 8!")
                        return
                    nums.append(int(value))

            if len(set(nums)) != 9:
                messagebox.showerror("Error", "Numbers must be unique (0-8)!")
                return

            if len(nums) != 9 or not is_solvable(tuple(nums)):
                messagebox.showerror("Error", "Invalid or unsolvable puzzle!")
                return

            self.initial_state = nums
            self.comparison_results = []
            algorithms = [
                (bfs, "BFS"),
                (dfs, "DFS"),
                (ids, "IDS"),
                (ucs, "UCS"),
                (a_star, "A*"),
                (ida_star, "IDA*"),
                (hill_climbing, "Hill Climb"),
                (simulated_annealing, "SimuAnnealing"),
                (beam_search, "BeamSearch"),
                (and_or_search, "AND-OR")
            ]

            self.status_label.config(text="Comparing algorithms...")
            self.root.update()

            for algo, name in algorithms:
                result = self.run_algorithm(algo, name)
                if result:
                    self.comparison_results.append(result)

            self.status_label.config(text="Algorithm Comparison Complete")
            self.tree.delete(*self.tree.get_children())
            for result in self.comparison_results:
                self.tree.insert("", "end", values=(
                    result["algorithm"],
                    result["steps"],
                    result["cost"],
                    f"{result['time']:.4f}",
                    result["space"]
                ))

            # Update conclusion
            conclusion_text = self.generate_conclusion()
            self.conclusion_label.config(text=conclusion_text)

            selected_metrics = [metric for metric, var in self.chart_vars.items() if var.get()]
            if not selected_metrics:
                messagebox.showwarning("Warning", "Please select at least one metric to display the chart!")
                return

            ChartWindow(self.comparison_results, selected_metrics)

        except Exception as e:
            messagebox.showerror("Error", f"Error during comparison: {str(e)}")
            self.status_label.config(text="Algorithm Details Table")

    def reset(self):
        self.initial_state = [1, 2, 3, 4, 5, 6, 0, 7, 8]
        for i in range(3):
            for j in range(3):
                self.input_grid[i][j].delete(0, tk.END)
                self.input_grid[i][j].insert(0, str(self.initial_state[i * 3 + j]))
        self.result = None
        self.step = 0
        self.animation_progress = 1.0
        self.comparison_results = []
        self.tree.delete(*self.tree.get_children())
        self.conclusion_label.config(text="Conclusion: Select an algorithm and click Compare to see the evaluation.")
        self.status_label.config(text="Enter 9 numbers (0-8)")