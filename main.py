import pygame
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

from settings import Game
from algorithm import *

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

class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.root.geometry(f"{game.WIDTH}x{game.HEIGHT + 200}")
        self.root.configure(bg="#e0e7ff")  # Light blue background

        # Gradient canvas background
        self.canvas = tk.Canvas(self.root, width=game.WIDTH, height=game.HEIGHT + 200, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_rectangle(0, 0, game.WIDTH, game.HEIGHT + 200, fill="#e0e7ff", outline="")
        self.canvas.create_rectangle(0, 0, game.WIDTH, 200, fill="#c7d2fe", outline="")

        # Initial state
        self.initial_state = [2, 3, 6, 1, 0, 5, 4, 7, 8]
        self.result = None
        self.step = 0
        self.last_step_time = time.time()
        self.animation_progress = 1.0
        self.animation_duration = 0.15

        # Main frame with shadow
        self.main_frame = tk.Frame(self.canvas, bg="white", bd=0, relief="flat")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=game.WIDTH-40, height=game.HEIGHT+160)
        self.canvas.create_rectangle(20, 20, game.WIDTH-20, game.HEIGHT+180, fill="", outline="#d1d5db", width=2)
        self.canvas.create_rectangle(25, 25, game.WIDTH-25, game.HEIGHT+185, fill="", outline="#e5e7eb", width=1)

        # Left frame for the puzzle grid
        self.grid_frame = tk.Frame(self.main_frame, bg="white")
        self.grid_frame.pack(side=tk.LEFT, padx=20, pady=20)
        self.grid_width = game.GRID_X * 2 + game.GRID_SIZE * game.TILE_SIZE
        self.grid_height = game.GRID_Y * 2 + game.GRID_SIZE * game.TILE_SIZE
        self.puzzle_grid = PuzzleGrid(self.grid_width, self.grid_height)
        self.grid_label = tk.Label(self.grid_frame, bg="white", bd=0)
        self.grid_label.pack()

        # Right frame for controls
        self.control_frame = tk.Frame(self.main_frame, bg="white")
        self.control_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill="y")

        # Input frame
        self.input_frame = tk.Frame(self.control_frame, bg="white")
        self.input_frame.pack(pady=(20, 10), fill="x")
        self.input_label = tk.Label(self.input_frame, text="Initial State (0-8)", font=("JetBrains Mono", 12, "bold"), bg="white", fg="#4b5563")
        self.input_label.pack(anchor="w", pady=(0, 5))

        self.input_grid = []
        for i in range(3):
            row = []
            frame_row = tk.Frame(self.input_frame, bg="white")
            frame_row.pack(fill="x")
            for j in range(3):
                entry = ttk.Entry(frame_row, width=5, font=("JetBrains Mono", 12), justify="center", style="Custom.TEntry")
                entry.insert(0, str(self.initial_state[i * 3 + j]))
                entry.pack(side=tk.LEFT, padx=3, pady=3)
                row.append(entry)
            self.input_grid.append(row)

        # Button frame
        self.button_frame = tk.Frame(self.control_frame, bg="white")
        self.button_frame.pack(pady=15)
        style = ttk.Style()
        style.configure("Custom.TButton", font=("JetBrains Mono", 10, "bold"), padding=8, background="#60a5fa", foreground="black")
        style.map("Custom.TButton", background=[('active', '#3b82f6')], foreground=[('active', 'black')])

        self.bfs_button = ttk.Button(self.button_frame, text="BFS", command=self.run_bfs, style="Custom.TButton")
        self.bfs_button.grid(row=0, column=0, padx=5, pady=3)
        self.dfs_button = ttk.Button(self.button_frame, text="DFS", command=self.run_dfs, style="Custom.TButton")
        self.dfs_button.grid(row=0, column=1, padx=5, pady=3)
        self.ids_button = ttk.Button(self.button_frame, text="IDS", command=self.run_ids, style="Custom.TButton")
        self.ids_button.grid(row=0, column=2, padx=5, pady=3)
        self.ucs_button = ttk.Button(self.button_frame, text="UCS", command=self.run_ucs, style="Custom.TButton")
        self.ucs_button.grid(row=0, column=3, padx=5, pady=3)
        self.astar_button = ttk.Button(self.button_frame, text="A*", command=self.run_astar, style="Custom.TButton")
        self.astar_button.grid(row=1, column=0, padx=5, pady=3)
        self.idastar_button = ttk.Button(self.button_frame, text="IDA*", command=self.run_idastar, style="Custom.TButton")
        self.idastar_button.grid(row=1, column=1, padx=5, pady=3)
        self.hillclimbing_button = ttk.Button(self.button_frame, text="Hill Climb", command=self.run_hillclimbing, style="Custom.TButton")
        self.hillclimbing_button.grid(row=1, column=2, padx=5, pady=3)
        self.reset_button = ttk.Button(self.button_frame, text="Reset", command=self.reset, style="Custom.TButton")
        self.reset_button.grid(row=1, column=3, padx=5, pady=3)

        # Status label
        self.status_label = tk.Label(self.control_frame, text="NGHIEM QUANG HUY - 23110222", font=("JetBrains Mono", 14, "bold"), bg="white", fg="#1f2937")
        self.status_label.pack(pady=15)

        # Table frame for metrics
        self.table_frame = tk.Frame(self.control_frame, bg="#f9fafb", bd=1, relief="solid")
        self.table_frame.pack(pady=10, fill="x")
        style.configure("Custom.Treeview", font=("JetBrains Mono", 10), rowheight=25)
        style.configure("Custom.Treeview.Heading", font=("JetBrains Mono", 10, "bold"), background="#e5e7eb", foreground="#374151")
        self.tree = ttk.Treeview(self.table_frame, columns=("Algorithm", "Steps", "Cost", "Time", "Space"), show="headings", height=1, style="Custom.Treeview")
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

        # Custom entry style
        style.configure("Custom.TEntry", fieldbackground="#f3f4f6", borderwidth=0, padding=5)
        style.map("Custom.TEntry", fieldbackground=[('focus', '#e5e7eb')])

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
                        return
                    nums.append(int(value))

            if len(set(nums)) != 9:
                messagebox.showerror("Error", "Numbers must be unique (0-8)!")
                return

            if len(nums) != 9 or not is_solvable(tuple(nums)):
                messagebox.showerror("Error", "Invalid or unsolvable puzzle!")
                return

            self.initial_state = nums
            self.result = algorithm(tuple(self.initial_state))
            self.step = 0
            self.last_step_time = time.time()
            self.animation_progress = 0.0

            if not self.result:
                messagebox.showerror("Error", "No solution found!")
                return

            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=(
                algo_name,
                self.result["steps"],
                self.result["cost"],
                f"{self.result['time']:.4f}",
                self.result["space"]
            ))

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input or error: {str(e)}")

    def run_bfs(self):
        self.run_algorithm(bfs, "BFS")

    def run_dfs(self):
        self.run_algorithm(dfs, "DFS")

    def run_ids(self):
        self.run_algorithm(ids, "IDS")

    def run_ucs(self):
        self.run_algorithm(ucs, "UCS")

    def run_astar(self):
        self.run_algorithm(a_star, "A*")

    def run_idastar(self):
        self.run_algorithm(ida_star, "IDA*")

    def run_hillclimbing(self):
        self.run_algorithm(hill_climbing, "Hill Climb")

    def reset(self):
        self.initial_state = [2, 3, 6, 1, 0, 5, 4, 7, 8]
        for i in range(3):
            for j in range(3):
                self.input_grid[i][j].delete(0, tk.END)
                self.input_grid[i][j].insert(0, str(self.initial_state[i * 3 + j]))
        self.result = None
        self.step = 0
        self.animation_progress = 1.0
        self.tree.delete(*self.tree.get_children())
        self.status_label.config(text="Enter 9 numbers (0-8)")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()