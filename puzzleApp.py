import pygame
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
from sklearn.ensemble import RandomForestRegressor
import pickle

from settings import Game
from algorithms_source.algorithm import *
from statics import *
from puzzleGrid import *

pygame.init()
game = Game()
FONT = pygame.font.SysFont("JetBrains Mono", 40)
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nghiêm Quang Huy OI 2025")
        self.root.geometry(f"{game.WIDTH + 200}x{game.HEIGHT + 400}")
        self.root.configure(bg="#f0f4f8")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.canvas = tk.Canvas(
            self.root, 
            width=game.WIDTH + 200, 
            height=game.HEIGHT + 400, 
            highlightthickness=0, 
            bg="#f0f4f8"
        )
        self.canvas.pack(
            fill="both", 
            expand=True
        )
        self.canvas.create_rectangle(0, 0, game.WIDTH + 200, game.HEIGHT + 400, fill="#e6ecf0", outline="")
        self.canvas.create_rectangle(0, 0, game.WIDTH + 200, 250, fill="#d3e0ea", outline="")

        self.initial_state = [1, 2, 3, 4, 5, 6, 0, 7, 8]
        self.result = None
        self.step = 0
        self.last_step_time = time.time()
        self.animation_progress = 1.0
        self.animation_duration = 0.15
        self.comparison_results = []

        # Tải mô hình dự đoán
        self.models = self.load_or_initialize_models()

        self.main_frame = tk.Frame(self.canvas, bg="#ffffff", bd=2, relief="raised")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=game.WIDTH + 160, height=game.HEIGHT + 360)
        self.canvas.create_rectangle(20, 20, game.WIDTH + 180, game.HEIGHT + 380, fill="", outline="#b0c4de", width=2)

        self.grid_frame = tk.Frame(self.main_frame, bg="#ffffff", bd=2, relief="groove")
        self.grid_frame.pack(side=tk.LEFT, padx=20, pady=20)
        self.grid_width = game.GRID_X * 2 + game.GRID_SIZE * game.TILE_SIZE
        self.grid_height = game.GRID_Y * 2 + game.GRID_SIZE * game.TILE_SIZE
        self.puzzle_grid = PuzzleGrid(self.grid_width, self.grid_height)
        self.grid_label = tk.Label(self.grid_frame, bg="#ffffff", bd=0)
        self.grid_label.pack(padx=10, pady=10)

        self.control_frame = tk.Frame(self.main_frame, bg="#ffffff", bd=2, relief="groove")
        self.control_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill="y", expand=True)

        self.header_label = tk.Label(self.control_frame, text="Will win OI 2025 🦅", font=("JetBrains Mono", 18, "bold"),
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
            #Uniform cost search
            ("BFS", self.run_bfs), 
            ("DFS", self.run_dfs), 
            ("IDS", self.run_ids), 
            ("UCS", self.run_ucs),

            #Inform cost search
            ("A* manhattan", self.run_a_star_manhattan), 
            ("A* linear conflict", self.run_a_start_linear_conflict),
            ("IDA*", self.run_idastar), 
            ("Greedy FS", self.run_greedy_FS), 

            ("Hill Climb", self.run_hillclimbing),
            ("Reset", self.reset), 
            ("SimuAnnealing", self.run_simulated_annealing),
            ("AND-OR", self.run_andor_search), 
            ("BeamSearch", self.run_beam_search), 
            ("Compare", self.compare_algorithms),
            ("Belief", self.run_partialy_observable_search),
            ("Roll", self.roll_random_state),
            ("Predict", self.predict_fastest_algorithm)
            
        ]

        for i, (text, cmd) in enumerate(buttons):
            btn = ttk.Button(self.button_frame, text=text, command=cmd, style="Custom.TButton")
            btn.grid(row=i // 5, column=i % 5, padx=5, pady=5, sticky="ew")

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

    def calculate_features(self, state):
        manhattan_distance = 0
        for i, num in enumerate(state):
            if num == 0:
                continue
            target_x, target_y = (num - 1) // 3, (num - 1) % 3
            current_x, current_y = i // 3, i % 3
            manhattan_distance += abs(target_x - current_x) + abs(target_y - current_y)
        
        misplaced_tiles = sum(1 for i, num in enumerate(state) if num != 0 and num != GOAL_STATE[i])
        
        inversions = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] != 0 and state[j] != 0 and state[i] > state[j]:
                    inversions += 1
        print([manhattan_distance, misplaced_tiles, inversions])
        return [manhattan_distance, misplaced_tiles, inversions]

    def load_or_initialize_models(self):
        try:
            with open("models.pkl", "rb") as f:
                models = pickle.load(f)
        except FileNotFoundError:
            models = {
                algo: RandomForestRegressor(n_estimators=100, random_state=42)
                for algo in ["BFS", "IDS", "UCS", "A*", "IDA*", "Hill Climb", 
                            "SimuAnnealing", "BeamSearch", "AND-OR"]
            }
        return models

    def train_models(self):
        algorithms = [
            (bfs, "BFS"), (ids, "IDS"), (ucs, "UCS"),
            (a_star_manhattan, "A*"), (ida_star_manhattan, "IDA*"), (hill_climbing, "Hill Climb"),
            (simulated_annealing, "SimuAnnealing"), (beam_search, "BeamSearch"),
            (and_or_search, "AND-OR")
        ]
        n_samples = 10  # Số lượng mẫu
        X = []
        y = {algo: [] for _, algo in algorithms}
        MAX_TIME = 1000.0  # Giá trị thời gian lớn thay cho float('inf')

        self.status_label.config(text="Training models...")
        self.root.update()

        for sample_idx in range(n_samples):
            state = self.generate_random_state()
            features = self.calculate_features(state)
            X.append(features)
            print(f"Sample {sample_idx + 1}/{n_samples} - Features: {features}")  # Debug features

            for algo_func, algo_name in algorithms:
                result = algo_func(tuple(state))
                time_taken = result["time"] if result and result["time"] < float('inf') else MAX_TIME
                y[algo_name].append(time_taken)
                print(f"Algorithm: {algo_name}, Time: {time_taken}")  # Debug labels

        models = {}
        for algo_name in y:
            print(f"Training model for {algo_name} with labels: {y[algo_name]}")  # Debug labels for each algorithm
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X, y[algo_name])
            models[algo_name] = model

        with open("models.pkl", "wb") as f:
            pickle.dump(models, f)

        self.status_label.config(text="Model training complete")
        return models

    def predict_fastest_algorithm(self):
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

            features = self.calculate_features(nums)
            predictions = {}
            for algo, model in self.models.items():
                try:
                    predicted_time = model.predict([features])[0]
                    predictions[algo] = predicted_time
                except:
                    predictions[algo] = float('inf')

            fastest_algo = min(predictions, key=predictions.get)
            fastest_time = predictions[fastest_algo]

            self.status_label.config(text=f"Predicted fastest: {fastest_algo} ({fastest_time:.4f}s)")
            messagebox.showinfo("Prediction", f"Fastest algorithm: {fastest_algo} ({fastest_time:.4f}s)")

        except Exception as e:
            messagebox.showerror("Error", f"Prediction error: {str(e)}")
            self.status_label.config(text="Algorithm Details Table")

    def generate_random_state(self):
        while True:
            state = list(range(9))
            random.shuffle(state)
            if is_solvable(tuple(state)):
                return state

    def roll_random_state(self):
        self.initial_state = self.generate_random_state()
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
        self.status_label.config(text="New random state generated")

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
            self.status_label.config(text=f"Running {algo_name}... pls wait")
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
                f"{result["time"]:.4f}",
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

    def run_a_star_manhattan(self):
        result = self.run_algorithm(a_star_manhattan, "A* manhattan")
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
        result = self.run_algorithm(ida_star_manhattan, "IDA* manhattan")
        if result:
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=(
                result["algorithm"],
                result["steps"],
                result["cost"],
                f"{result['time']:.4f}",
                result["space"]
            ))

    def run_greedy_FS(self):
        result = self.run_algorithm(greedy_FS, "Greedy FS")
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

    def run_a_start_linear_conflict(self):
        result = self.run_algorithm(a_start_linear_conflict, "A* linear conflict")
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

    def run_partialy_observable_search(self):
        result = self.run_algorithm(belief, "BELIFE")
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

        avg_steps = sum(result["steps"] for result in self.comparison_results) / len(self.comparison_results)
        problem_complexity = "simple" if avg_steps <= 5 else "moderate" if avg_steps <= 15 else "complex"

        conclusion = "Conclusion:\n"
        conclusion += f"- Problem Complexity: {problem_complexity.capitalize()} (average {avg_steps:.1f} steps).\n"
        conclusion += f"- For shortest path: {', '.join(optimal_algorithms)} achieved optimal steps ({optimal_steps}).\n"
        if problem_complexity == "simple":
            conclusion += "  BFS, UCS, A*, IDA*, IDS are reliable for simple puzzles.\n"
        else:
            conclusion += "  A*, IDA*, AND-OR are better for complex puzzles due to heuristic guidance.\n"
        conclusion += f"- For memory efficiency: {', '.join(space_efficient_algorithms)} used least space ({min_space}).\n"
        if min_space <= 5:
            conclusion += "  IDA*, AND-OR, Hill Climb, Simulated Annealing are ideal for low-memory scenarios.\n"
        conclusion += f"- For speed: {', '.join(time_efficient_algorithms)} were fastest ({min_time:.4f}s).\n"
        if problem_complexity == "simple":
            conclusion += "  Hill Climb, Simulated Annealing, Beam Search are fast for simple puzzles.\n"
        else:
            conclusion += "  A*, IDA*, AND-OR are faster for complex puzzles with heuristic optimization.\n"
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
                (a_star_mahatan, "A*"),
                (ida_star, "IDA*"),
                (hill_climbing, "Hill Climb"),
                (simulated_annealing, "SimuAnnealing"),
                (a_start_linear_conflict, "A* linear conflict"),  # Add the missing comma here
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
    
    def on_close(self):
        """Handle cleanup before closing the application."""
        try:
            self.root.after_cancel(self.update)  # Cancel any scheduled updates
        except Exception:
            pass
        self.root.destroy()