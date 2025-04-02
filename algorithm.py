import heapq
from collections import deque
import random
import time
import sys

# Import settings
from settings import Game, GOAL_STATE, MOVES

# Create an instance of Game to access settings
game = Game()

# Puzzle-solving functions
def is_solvable(state):
    inversions = 0
    state_list = [x for x in state if x != 0]
    for i in range(len(state_list)):
        for j in range(i + 1, len(state_list)):
            if state_list[i] > state_list[j]:
                inversions += 1
    return inversions % 2 == 0

def get_blank_position(state):
    return state.index(0)

def is_valid(pos):
    return 0 <= pos[0] < 3 and 0 <= pos[1] < 3

def move_tile(state, old_pos, new_pos):
    state_list = list(state)
    i, j = old_pos[0] * 3 + old_pos[1], new_pos[0] * 3 + new_pos[1]
    state_list[i], state_list[j] = state_list[j], state_list[i]
    return tuple(state_list)

def get_neighbors(state):
    blank_idx = get_blank_position(state)
    blank_pos = (blank_idx // 3, blank_idx % 3)
    neighbors = []
    for move in MOVES:
        new_pos = (blank_pos[0] + move[0], blank_pos[1] + move[1])
        if is_valid(new_pos):
            neighbors.append(move_tile(state, blank_pos, new_pos))
    return neighbors

def manhattan_distance(state):
    total = 0
    for i, tile in enumerate(state):
        if tile != 0:
            target_row, target_col = (tile - 1) // 3, (tile - 1) % 3
            current_row, current_col = i // 3, i % 3
            total += abs(target_row - current_row) + abs(target_col - current_col)
    return total

def bfs(start):
    start_time = time.time()
    visited = set()
    queue = deque([(start, [start])])
    max_space_bytes = 0
    while queue:
        state, path = queue.popleft()
        if state == GOAL_STATE:
            end_time = time.time()
            return {
                "path": path,
                "steps": len(path) - 1,
                "cost": len(path) - 1,
                "time": end_time - start_time,
                "space": max_space_bytes
            }
        if state not in visited:
            visited.add(state)
            for neighbor in get_neighbors(state):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
        # Tính dung lượng bộ nhớ thực tế
        queue_size = sum(sys.getsizeof(item) for item in queue)
        visited_size = sum(sys.getsizeof(item) for item in visited)
        path_size = sum(sys.getsizeof(item) for item in path)
        current_space = queue_size + visited_size + path_size
        max_space_bytes = max(max_space_bytes, current_space)
    return None

def dfs(start, depth_limit=float('inf')):
    start_time = time.time()
    visited = set()
    stack = [(start, [start], 0)]
    max_space = 0
    while stack:
        state, path, depth = stack.pop()
        if state == GOAL_STATE:
            end_time = time.time()
            return {
                "path": path,
                "steps": len(path) - 1,
                "cost": len(path) - 1,
                "time": end_time - start_time,
                "space": max_space
            }
        if state not in visited and depth < depth_limit:
            visited.add(state)
            for neighbor in get_neighbors(state):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor], depth + 1))
        max_space = max(max_space, len(stack) + len(visited))
    return None

def ids(start):
    start_time = time.time()
    depth = 0
    max_space = 0
    while True:
        visited = set()
        stack = [(start, [start], 0)]
        while stack:
            state, path, d = stack.pop()
            if state == GOAL_STATE:
                end_time = time.time()
                return {
                    "path": path,
                    "steps": len(path) - 1,
                    "cost": len(path) - 1,
                    "time": end_time - start_time,
                    "space": max_space
                }
            if state not in visited and d < depth:
                visited.add(state)
                for neighbor in get_neighbors(state):
                    if neighbor not in visited:
                        stack.append((neighbor, path + [neighbor], d + 1))
            max_space = max(max_space, len(stack) + len(visited))
        depth += 1

def ucs(start):
    start_time = time.time()
    visited = set()
    queue = [(0, start, [start])]  # (cost, state, path)
    heapq.heapify(queue)
    max_space = 0
    while queue:
        cost, state, path = heapq.heappop(queue)
        if state == GOAL_STATE:
            end_time = time.time()
            return {
                "path": path,
                "steps": len(path) - 1,
                "cost": cost,
                "time": end_time - start_time,
                "space": max_space
            }
        if state not in visited:
            visited.add(state)
            for neighbor in get_neighbors(state):
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + 1, neighbor, path + [neighbor]))
        max_space = max(max_space, len(queue) + len(visited))
    return None

def a_star(start):
    start_time = time.time()
    visited = set()
    queue = [(manhattan_distance(start), 0, start, [start])]  # (f_score, g_score, state, path)
    heapq.heapify(queue)
    max_space = 0
    while queue:
        f_score, g_score, state, path = heapq.heappop(queue)
        if state == GOAL_STATE:
            end_time = time.time()
            return {
                "path": path,
                "steps": len(path) - 1,
                "cost": g_score,
                "time": end_time - start_time,
                "space": max_space
            }
        if state not in visited:
            visited.add(state)
            for neighbor in get_neighbors(state):
                if neighbor not in visited:
                    new_g = g_score + 1
                    new_f = new_g + manhattan_distance(neighbor)
                    heapq.heappush(queue, (new_f, new_g, neighbor, path + [neighbor]))
        max_space = max(max_space, len(queue) + len(visited))
    return None

def ida_star(start):
    start_time = time.time()
    max_space = 0
    def search(state, g_score, path, threshold, visited):
        nonlocal max_space
        h_score = manhattan_distance(state)
        f_score = g_score + h_score
        if f_score > threshold:
            return None, f_score
        if state == GOAL_STATE:
            return path, f_score
        min_exceeded = float('inf')
        for neighbor in get_neighbors(state):
            if neighbor not in path:
                visited.add(neighbor)
                result, new_f = search(neighbor, g_score + 1, path + [neighbor], threshold, visited)
                if result is not None:
                    return result, new_f
                min_exceeded = min(min_exceeded, new_f)
        max_space = max(max_space, len(visited))
        return None, min_exceeded

    threshold = manhattan_distance(start)
    path = [start]
    while True:
        visited = set(path)
        result, new_threshold = search(start, 0, path, threshold, visited)
        if result is not None:
            end_time = time.time()
            return {
                "path": result,
                "steps": len(result) - 1,
                "cost": len(result) - 1,
                "time": end_time - start_time,
                "space": max_space
            }
        if new_threshold == float('inf'):
            return None
        threshold = new_threshold

def hill_climbing(start):
    start_time = time.time()
    def generate_random_state():
        state = list(GOAL_STATE)
        while True:
            random.shuffle(state)
            if is_solvable(tuple(state)):
                return tuple(state)

    max_iterations = 1000
    max_restarts = 10
    best_path = None
    best_heuristic = float('inf')
    max_space = 0

    current_state = start
    current_path = [start]

    for restart in range(max_restarts):
        iterations = 0
        stuck = False

        while iterations < max_iterations:
            if current_state == GOAL_STATE:
                end_time = time.time()
                return {
                    "path": current_path,
                    "steps": len(current_path) - 1,
                    "cost": len(current_path) - 1,
                    "time": end_time - start_time,
                    "space": max_space
                }

            neighbors = get_neighbors(current_state)
            current_heuristic = manhattan_distance(current_state)
            best_neighbor = None
            best_neighbor_heuristic = current_heuristic

            for neighbor in neighbors:
                neighbor_heuristic = manhattan_distance(neighbor)
                if neighbor_heuristic < best_neighbor_heuristic:
                    best_neighbor = neighbor
                    best_neighbor_heuristic = neighbor_heuristic

            if best_neighbor is None or best_neighbor_heuristic >= current_heuristic:
                stuck = True
                break

            current_state = best_neighbor
            current_path.append(current_state)
            iterations += 1
            max_space = max(max_space, len(current_path) + len(neighbors))

        if best_neighbor_heuristic < best_heuristic:
            best_heuristic = best_neighbor_heuristic
            best_path = current_path.copy()

        if stuck:
            current_state = generate_random_state()
            current_path = [current_state]

    end_time = time.time()
    return {
        "path": best_path,
        "steps": len(best_path) - 1 if best_path else 0,
        "cost": len(best_path) - 1 if best_path else 0,
        "time": end_time - start_time,
        "space": max_space
    } if best_path else None