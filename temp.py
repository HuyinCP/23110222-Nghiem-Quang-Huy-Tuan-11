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

pygame.init()

game = Game()

FONT = pygame.font.SysFont("JetBrains Mono", 40)

GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

class PuzzleGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height))
        self.current_state = None
        self.prev_state = None
        self.animation_progress = 1.0
        self.swapped_positions = []

    def find_swapped_tiles(self, state1, state2):
        swapped = []
        for i in range(len(state1)):
            if state1[i] != state2[i]:
                swapped.append(i)
        return swapped

    def ease_in_out_cubic(self, t):
        t *= 2
        if t < 1:
            return 0.5 * t * t * t
        t -= 2
        return 0.5 * (t * t * t + 2)

    def get_direction(self, pos1, pos2):
        row1, col1 = pos1 // 3, pos1 % 3
        row2, col2 = pos2 // 3, pos2 % 3
        if row1 > row2:
            return "up"
        elif row1 < row2:
            return "down"
        elif col1 > col2:
            return "left"
        elif col1 < col2:
            return "right"
        return None

    def draw(self, state, prev_state=None, animation_progress=1.0):
        self.current_state = state
        self.prev_state = prev_state
        self.animation_progress = animation_progress
        self.swapped_positions = self.find_swapped_tiles(prev_state, state) if prev_state else []
        tile_positions = {}
        tile_scales = {}
        tile_alphas = {}

        for i in range(game.GRID_SIZE):
            for j in range(game.GRID_SIZE):
                tile = state[i * 3 + j]
                tile_positions[i * 3 + j] = (game.GRID_X + j * game.TILE_SIZE, game.GRID_Y + i * game.TILE_SIZE)
                tile_scales[i * 3 + j] = 1.0
                tile_alphas[i * 3 + j] = 255

        if prev_state and animation_progress < 1.0 and self.swapped_positions:
            pos1, pos2 = self.swapped_positions
            direction = self.get_direction(pos1, pos2)
            row1, col1 = pos1 // 3, pos1 % 3
            row2, col2 = pos2 // 3, pos2 % 3
            start_x1, start_y1 = game.GRID_X + col2 * game.TILE_SIZE, game.GRID_Y + row2 * game.TILE_SIZE
            end_x1, end_y1 = game.GRID_X + col1 * game.TILE_SIZE, game.GRID_Y + row1 * game.TILE_SIZE
            start_x2, start_y2 = game.GRID_X + col1 * game.TILE_SIZE, game.GRID_Y + row1 * game.TILE_SIZE
            end_x2, end_y2 = game.GRID_X + col2 * game.TILE_SIZE, game.GRID_Y + row2 * game.TILE_SIZE
            eased_progress = self.ease_in_out_cubic(animation_progress)
            scale = 1.0 + 0.2 * (1 - abs(2 * eased_progress - 1))
            alpha = 255 * (1 - 0.3 * (1 - abs(2 * eased_progress - 1)))

            if direction in ["up", "down"]:
                tile_positions[pos1] = (start_x1, start_y1 + (end_y1 - start_y1) * eased_progress)
                tile_positions[pos2] = (start_x2, start_y2 + (end_y2 - start_y2) * eased_progress)
            elif direction in ["left", "right"]:
                tile_positions[pos1] = (start_x1 + (end_x1 - start_x1) * eased_progress, start_y1)
                tile_positions[pos2] = (start_x2 + (end_x2 - start_x2) * eased_progress, start_y2)

            tile_scales[pos1] = scale
            tile_scales[pos2] = scale
            tile_alphas[pos1] = alpha
            tile_alphas[pos2] = alpha

        self.surface.fill((245, 245, 245))  # Light gray background

        for i in range(game.GRID_SIZE):
            for j in range(game.GRID_SIZE):
                tile = state[i * 3 + j]
                if tile != 0:
                    pos_idx = i * 3 + j
                    x, y = tile_positions[pos_idx]
                    scale = tile_scales[pos_idx]
                    alpha = tile_alphas[pos_idx]
                    is_correct = (tile == GOAL_STATE[pos_idx])
                    color = (200, 255, 200) if is_correct else (255, 100, 100) if pos_idx in self.swapped_positions else (180, 180, 180)

                    if pos_idx in self.swapped_positions and animation_progress < 1.0:
                        shadow_surface = pygame.Surface((game.TILE_SIZE, game.TILE_SIZE), pygame.SRCALPHA)
                        shadow_surface.fill((0, 0, 0, 50))
                        shadow_rect = shadow_surface.get_rect(center=(x + game.TILE_SIZE / 2 + 5, y + game.TILE_SIZE / 2 + 5))
                        self.surface.blit(shadow_surface, shadow_rect)

                    tile_surface = pygame.Surface((game.TILE_SIZE - 2, game.TILE_SIZE - 2), pygame.SRCALPHA)
                    pygame.draw.rect(tile_surface, color, (0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2), border_radius=5)
                    tile_surface.set_alpha(int(alpha))
                    scaled_size = (int((game.TILE_SIZE - 2) * scale), int((game.TILE_SIZE - 2) * scale))
                    scaled_tile = pygame.transform.scale(tile_surface, scaled_size)
                    tile_rect = scaled_tile.get_rect(center=(x + game.TILE_SIZE / 2, y + game.TILE_SIZE / 2))
                    self.surface.blit(scaled_tile, tile_rect)

                    text = FONT.render(str(tile), True, (50, 50, 50))
                    text_rect = text.get_rect(center=(x + game.TILE_SIZE / 2, y + game.TILE_SIZE / 2))
                    self.surface.blit(text, text_rect)

    def get_surface(self):
        return self.surface

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

        num_metrics = len(self.selected_metrics)
        if num_metrics == 0:
            return

        fig, axes = plt.subplots(num_metrics, 1, figsize=(6, 2 * num_metrics), sharex=True)
        if num_metrics == 1:
            axes = [axes]

        x = np.arange(len(algorithms))
        width = 0.2

        for idx, metric in enumerate(self.selected_metrics):
            if metric == "Steps":
                axes[idx].bar(x, steps, width, label="Steps", color="#4a90e2")
                axes[idx].set_ylabel("Steps")
            elif metric == "Cost":
                axes[idx].bar(x, costs, width, label="Cost", color="#50c878")
                axes[idx].set_ylabel("Cost")
            elif metric == "Time":
                axes[idx].bar(x, times, width, label="Time (s)", color="#f5a623")
                axes[idx].set_ylabel("Time (s)")
            elif metric == "Space":
                axes[idx].bar(x, spaces, width, label="Space", color="#e74c3c")
                axes[idx].set_ylabel("Space")
            axes[idx].legend()

        axes[0].set_title("Algorithm Performance Comparison", fontsize=12, pad=10)
        axes[-1].set_xlabel("Algorithms", fontsize=10)
        axes[-1].set_xticks(x)
        axes[-1].set_xticklabels(algorithms, rotation=45, ha="right", fontsize=8)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.root.geometry(f"{game.WIDTH + 200}x{game.HEIGHT + 400}")  # Tăng kích thước cửa sổ
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
            ("BFS", self.run_bfs), ("DFS", self.run_dfs), ("IDS", self.run_ids), ("UCS", self.run_ucs),
            ("A*", self.run_astar), ("IDA*", self.run_idastar), ("Hill Climb", self.run_hillclimbing),
            ("Reset", self.reset), ("SimuAnnealing", self.run_simulated_annealing),
            ("BeamSearch", self.run_beam_search), ("AND-OR", self.run_andor_search), ("Compare", self.compare_algorithms)
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

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()