import time
from collections import deque
import heapq
import random
import math

# Goal state for the 8-puzzle
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def is_solvable(state):
    """Check if the puzzle is solvable based on inversion count."""
    inversions = 0
    state = [x for x in state if x != 0]
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] > state[j]:
                inversions += 1
    return inversions % 2 == 0

def get_neighbors(state):
    """Return possible next states by moving the blank tile (0)."""
    neighbors = []
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    zero_idx = state.index(0)
    row, col = zero_idx // 3, zero_idx % 3

    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_idx = new_row * 3 + new_col
            new_state = list(state)
            new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
            neighbors.append(tuple(new_state))
    return neighbors

def manhattan_distance(state):
    """Calculate Manhattan distance heuristic for the state."""
    distance = 0
    for i, tile in enumerate(state):
        if tile != 0:
            goal_row, goal_col = (tile - 1) // 3, (tile - 1) % 3
            curr_row, curr_col = i // 3, i % 3
            distance += abs(goal_row - curr_row) + abs(goal_col - curr_col)
    return distance

def and_or_search(start_state, max_depth=30, time_limit=5.0):
    """Optimized AND-OR Search with heuristic-guided pruning and iterative deepening."""
    start_time = time.time()
    visited = set()
    max_space = 0
    best_solution = None
    best_f_score = float('inf')

    def or_search(state, path, g_cost, depth, bound):
        """
        Perform an OR search to find a solution path in a state space using heuristic guidance.
        This function explores a state space using a combination of depth-first search and 
        heuristic-based pruning. It calculates the f-cost (g-cost + h-cost) for each state 
        and prunes paths that exceed the given bound or depth limit. The function prioritizes 
        promising moves by sorting neighbors based on their heuristic values.
        Args:
            state: The current state in the search space.
            path: A list representing the path taken to reach the current state.
            g_cost: The cost incurred to reach the current state.
            depth: The current depth in the search tree.
            bound: The maximum allowable f-cost for pruning.
        Returns:
            A tuple containing:
                - A dictionary with the solution path and its cost, or None if no solution is found.
                - The minimum f-cost encountered during the search.
        """
        """OR node: Choose a move with heuristic guidance."""
        nonlocal max_space, best_solution, best_f_score, start_time

        # Check time limit
        if time.time() - start_time > time_limit:
            return None, float('inf')

        # Calculate f = g + h (cost + heuristic)
        h_cost = manhattan_distance(state)
        f_cost = g_cost + h_cost

        # Prune if f_cost exceeds bound or depth limit
        if f_cost > bound or depth > max_depth:
            return None, f_cost

        if state == GOAL_STATE:
            return {"path": path, "cost": g_cost}, f_cost

        if state in visited:
            return None, float('inf')

        visited.add(state)
        max_space = max(max_space, len(visited))

        # Sort neighbors by f = g + h to prioritize promising moves
        neighbors = [(manhattan_distance(next_state), next_state) for next_state in get_neighbors(state)]
        neighbors.sort()  # Sort by heuristic value
        solutions = []
        min_f = float('inf')

        # AND node: Explore all promising neighbors
        for _, next_state in neighbors:
            if next_state not in visited:
                result, new_f = or_search(next_state, path + [next_state], g_cost + 1, depth + 1, bound)
                if result:
                    solutions.append(result)
                    if result["cost"] < best_f_score:
                        best_f_score = result["cost"]
                        best_solution = result
                        # Early termination if optimal solution found
                        if best_f_score <= h_cost:
                            visited.remove(state)
                            return best_solution, best_f_score
                min_f = min(min_f, new_f)

        visited.remove(state)  # Backtrack to save memory
        if solutions:
            best_result = min(solutions, key=lambda x: x["cost"])
            return best_result, best_result["cost"]
        return None, min_f

    if not is_solvable(start_state):
        return None

    # Iterative deepening with f-cost bound
    bound = manhattan_distance(start_state)
    while True:
        if time.time() - start_time > time_limit:
            break
        result, new_bound = or_search(start_state, [start_state], 0, 0, bound)
        if result:
            result["steps"] = len(result["path"]) - 1
            result["time"] = time.time() - start_time
            result["space"] = max_space
            return result
        if new_bound == float('inf'):
            break
        bound = new_bound * 1.5  # Increase bound more aggressively

    # Return best solution found within limits
    if best_solution:
        best_solution["steps"] = len(best_solution["path"]) - 1
        best_solution["time"] = time.time() - start_time
        best_solution["space"] = max_space
        return best_solution
    return None

def bfs(start_state):
    start_time = time.time()
    queue = deque([(start_state, [start_state])])
    visited = {start_state}
    max_space = 1

    while queue:
        state, path = queue.popleft()
        if state == GOAL_STATE:
            return {
                "path": path,
                "steps": len(path) - 1,
                "cost": len(path) - 1,
                "time": time.time() - start_time,
                "space": max_space
            }
        for next_state in get_neighbors(state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [next_state]))
                max_space = max(max_space, len(queue) + len(visited))
    return None

def dfs(start_state, time_limit=10000.0):
    start_time = time.time()
    stack = [(start_state, [start_state], 0)]  # (state, path, depth)
    visited = {start_state}
    max_space = 1

    while stack:
        if time.time() - start_time > time_limit:
            print("DFS: Time limit exceeded!")
            return None

        state, path, depth = stack.pop()

        if state == GOAL_STATE:
            return {
                "path": path,
                "steps": len(path) - 1,
                "cost": len(path) - 1,
                "time": time.time() - start_time,
                "space": max_space
            }

        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor], depth + 1))
                max_space = max(max_space, len(stack) + len(visited))

    print("DFS: No solution found within constraints!")
    return None

def ids(start_state):
    start_time = time.time()
    max_space = 0

    def dls(state, path, depth, visited):
        nonlocal max_space
        if state == GOAL_STATE:
            return path
        if depth == 0:
            return None
        for next_state in get_neighbors(state):
            if next_state not in visited:
                visited.add(next_state)
                max_space = max(max_space, len(visited))
                result = dls(next_state, path + [next_state], depth - 1, visited)
                if result:
                    return result
        return None

    depth = 0
    while True:
        visited = {start_state}
        result = dls(start_state, [start_state], depth, visited)
        if result:
            return {
                "path": result,
                "steps": len(result) - 1,
                "cost": len(result) - 1,
                "time": time.time() - start_time,
                "space": max_space
            }
        depth += 1
        if depth > 50:
            return None


# def belief(start_state):

def ucs(start_state):
    start_time = time.time()
    queue = [(0, start_state, [start_state])]
    visited = {start_state}
    max_space = 1

    while queue:
        cost, state, path = heapq.heappop(queue)
        if state == GOAL_STATE:
            return {
                "path": path,
                "steps": len(path) - 1,
                "cost": cost,
                "time": time.time() - start_time,
                "space": max_space
            }
        for next_state in get_neighbors(state):
            if next_state not in visited:
                visited.add(next_state)
                heapq.heappush(queue, (cost + 1, next_state, path + [next_state]))
                max_space = max(max_space, len(queue) + len(visited))
    return None

def a_star(start_state):
    start_time = time.time()
    queue = [(0 + manhattan_distance(start_state), 0, start_state, [start_state])]
    visited = {start_state}
    max_space = 1

    while queue:
        _, cost, state, path = heapq.heappop(queue)
        if state == GOAL_STATE:
            return {
                "path": path,
                "steps": len(path) - 1,
                "cost": cost,
                "time": time.time() - start_time,
                "space": max_space
            }
        for next_state in get_neighbors(state):
            if next_state not in visited:
                visited.add(next_state)
                new_cost = cost + 1
                heapq.heappush(queue, (new_cost + manhattan_distance(next_state), new_cost, next_state, path + [next_state]))
                max_space = max(max_space, len(queue) + len(visited))
    return None

def ida_star(start_state):
    start_time = time.time()
    max_space = 0

    def search(state, g, bound, path, visited):
        nonlocal max_space
        f = g + manhattan_distance(state)
        if f > bound:
            return f, None
        if state == GOAL_STATE:
            return f, path
        min_bound = float('inf')
        for next_state in get_neighbors(state):
            if next_state not in visited:
                visited.add(next_state)
                max_space = max(max_space, len(visited))
                new_f, result = search(next_state, g + 1, bound, path + [next_state], visited)
                visited.remove(next_state)
                if result:
                    return new_f, result
                min_bound = min(min_bound, new_f)
        return min_bound, None

    bound = manhattan_distance(start_state)
    visited = {start_state}
    while True:
        new_bound, result = search(start_state, 0, bound, [start_state], visited)
        if result:
            return {
                "path": result,
                "steps": len(result) - 1,
                "cost": len(result) - 1,
                "time": time.time() - start_time,
                "space": max_space
            }
        if new_bound == float('inf'):
            return None
        bound = new_bound

def hill_climbing(start_state):
    start_time = time.time()
    current_state = start_state
    path = [current_state]
    visited = {current_state}
    max_space = 1

    while current_state != GOAL_STATE:
        neighbors = get_neighbors(current_state)
        next_state = min(neighbors, key=manhattan_distance, default=None)
        if not next_state or manhattan_distance(next_state) >= manhattan_distance(current_state):
            return None
        current_state = next_state
        path.append(current_state)
        visited.add(current_state)
        max_space = max(max_space, len(visited))
    return {
        "path": path,
        "steps": len(path) - 1,
        "cost": len(path) - 1,
        "time": time.time() - start_time,
        "space": max_space
    }

def simulated_annealing(start_state):
    start_time = time.time()
    current_state = start_state
    path = [current_state]
    visited = {current_state}
    max_space = 1
    temperature = 1000
    cooling_rate = 0.995
    iterations = 1000

    while current_state != GOAL_STATE and iterations > 0:
        temperature *= cooling_rate
        neighbors = get_neighbors(current_state)
        next_state = random.choice(neighbors)
        delta = manhattan_distance(next_state) - manhattan_distance(current_state)
        if delta <= 0 or random.random() < math.exp(-delta / temperature):
            current_state = next_state
            path.append(current_state)
            visited.add(current_state)
            max_space = max(max_space, len(visited))
        iterations -= 1
    if current_state == GOAL_STATE:
        return {
            "path": path,
            "steps": len(path) - 1,
            "cost": len(path) - 1,
            "time": time.time() - start_time,
            "space": max_space
        }
    return None

def beam_search(start_state, beam_width=3):
    start_time = time.time()
    beam = [(manhattan_distance(start_state), start_state, [start_state])]
    visited = {start_state}
    max_space = 1

    while beam:
        new_beam = []
        for _, state, path in beam:
            if state == GOAL_STATE:
                return {
                    "path": path,
                    "steps": len(path) - 1,
                    "cost": len(path) - 1,
                    "time": time.time() - start_time,
                    "space": max_space
                }
            for next_state in get_neighbors(state):
                if next_state not in visited:
                    visited.add(next_state)
                    new_beam.append((manhattan_distance(next_state), next_state, path + [next_state]))
        beam = sorted(new_beam)[:beam_width]
        max_space = max(max_space, len(beam) + len(visited))
        if not beam:
            break
    return None