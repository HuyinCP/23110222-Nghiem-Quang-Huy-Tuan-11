import time
from collections import deque
import heapq
import random
import math
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import pickle

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

def linear_conflict(state):
    """Calculate the linear conflict heuristic for the state."""
    distance = manhattan_distance(state)
    conflict = 0
    
    # Check rows for conflicts
    for row in range(3):
        row_tiles = state[row*3:row*3+3]
        for i in range(3):
            for j in range(i+1, 3):
                if row_tiles[i] != 0 and row_tiles[j] != 0:
                    goal_i_row, goal_i_col = (row_tiles[i] - 1) // 3, (row_tiles[i] - 1) % 3
                    goal_j_row, goal_j_col = (row_tiles[j] - 1) // 3, (row_tiles[j] - 1) % 3
                    if goal_i_row == goal_j_row and goal_i_col > goal_j_col:
                        conflict += 2
    
    # Check columns for conflicts
    for col in range(3):
        col_tiles = [state[i*3 + col] for i in range(3)]
        for i in range(3):
            for j in range(i+1, 3):
                if col_tiles[i] != 0 and col_tiles[j] != 0:
                    goal_i_row, goal_i_col = (col_tiles[i] - 1) // 3, (col_tiles[i] - 1) % 3
                    goal_j_row, goal_j_col = (col_tiles[j] - 1) // 3, (col_tiles[j] - 1) % 3
                    if goal_i_col == goal_j_col and goal_i_row > goal_j_row:
                        conflict += 2

    return conflict

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
        h_cost = linear_conflict(state)
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
        neighbors = [(linear_conflict(next_state), next_state) for next_state in get_neighbors(state)]
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
    bound = linear_conflict(start_state)
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
    """Uninformed search: tìm kiếm không có thông tin"""
    start_time = time.time()
    queue = deque([(start_state, [start_state])]) # (state, path)
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
                max_space = max(max_space, len(queue))
    return None

def dfs(start_state):
    """Uninformed search: tìm kiếm không có thông tin"""
    start_time = time.time()
    stack = [(start_state, [start_state])]  # (state, path)
    visited = {start_state}
    max_space = len(stack)

    while stack:
        state, path = stack.pop()
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
                stack.append((neighbor, path + [neighbor]))
                max_space = max(max_space, len(stack))
    return None

def ucs(start_state):
    """Uninformed search: tìm kiếm không có thông tin"""
    start_time = time.time()
    priority_queue = []  
    heapq.heappush(priority_queue, (0, start_state, [start_state]))
    visited = set()
    dist = {start_state: 0}
    max_space = len(priority_queue)

    while priority_queue:
        cur_Cost, cur_State, cur_Path = heapq.heappop(priority_queue)
        if cur_Cost > dist.get(cur_State, float('inf')):
            continue
        if cur_State == GOAL_STATE:
            return {
                "path": cur_Path,
                "steps": len(cur_Path) - 1,
                "cost": cur_Cost,
                "time": time.time() - start_time,
                "space": max_space
            } 
        for next_state in get_neighbors(cur_State):
            new_cost = cur_Cost + 1
            if new_cost < dist.get(next_state, float('inf')) and next_state not in visited:
                visited.add(next_state)
                dist[next_state] = new_cost
                heapq.heappush(priority_queue, (new_cost, next_state, cur_Path + [next_state]))
                max_space = max(max_space, len(priority_queue))
    return None

def ids(start_state):
    """Uninformed search: tìm kiếm không có thông tin"""
    start_time = time.time()
    max_space = 0
    stack = []
    def dfs(state, path, depth, visited):
        stack.append(1)
        nonlocal max_space
        if state == GOAL_STATE:
            return path
        if depth == 0:
            return None
        visited.add(state)
        max_space = max(max_space, len(stack))

        for next_state in get_neighbors(state):
            if next_state not in visited:
                result = dfs(next_state, path + [next_state], depth - 1, visited)
                if result:
                    return result
        visited.remove(state)
        stack.pop()
        return None

    depth = 0
    while True:
        visited = set()
        result = dfs(start_state, [start_state], depth, visited)
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

def a_star_manhattan(start_state):
    """Informed Search: tìm kiếm có thông tin"""
    start_time = time.time()
    priority_queue = []
    # f(n) = g(n) + h(n), bắt đầu từ start_state
    heapq.heappush(priority_queue, (manhattan_distance(start_state), start_state, [start_state]))  # (f(n), curState, curPath) 
    # dp là dictionary lưu chi phí tối thiểu g(n) cho trạng thái đó
    dp = {}  
    dp[start_state] = 0  # Chi phí thực tế từ start_state đến nút hiện tại
    max_space = len(priority_queue)

    while priority_queue:
        cur_f, cur_State, cur_Path = heapq.heappop(priority_queue)
    
        if cur_State == GOAL_STATE:
            return {
                "path": cur_Path,
                "steps": len(cur_Path) - 1,
                "cost": len(cur_Path) - 1, 
                "time": time.time() - start_time,
                "space": max_space
            }

        for next_State in get_neighbors(cur_State):
            if next_State not in dp or dp[cur_State] + 1 < dp[next_State]:
                dp[next_State] = dp[cur_State] + 1
                new_f = dp[cur_State] + 1 + manhattan_distance(next_State)  # f(n) = g(n) + h(n)
                heapq.heappush(priority_queue, (new_f, next_State, cur_Path + [next_State]))
                max_space = max(max_space, len(priority_queue))

    return None

def ida_star_manhattan(start_state):
    start_time = time.time()
    max_space = 0
    stack = []
    def dfs(state, g, bound, path, visited):
        stack.append(1)
        nonlocal max_space
        f = g + manhattan_distance(state)
        if f > bound:
            return f, None
        if state == GOAL_STATE:
            return f, path
        min_bound = float('inf')
        visited.add(state)
        max_space = max(max_space, len(stack))
        for next_State in get_neighbors(state):
            if next_State not in visited:
                visited.add(next_State)
                new_f, result = dfs(next_State, g + 1, bound, path + [next_State], visited)
                visited.remove(next_State)
                if result:
                    return new_f, result
                min_bound = min(min_bound, new_f)
        stack.pop()
        return min_bound, None

    bound = manhattan_distance(start_state)

    while True:
        visited = set()
        visited.add(start_state)
        new_bound, result = dfs(start_state, 0, bound, [start_state], visited)
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

def greedy_FS(start_state):
    """Informed Search: tìm kiếm có thông tin"""
    visited = set()
    start_time = time.time()
    max_space = 0
    curPath = [start_state]
    return cal_greedy_FS(start_state, visited, start_time, max_space, curPath)

def cal_greedy_FS(curState, visited, start_time, max_space, curPath):
    stack = [(curState, curPath)]
    visited.add(curState)
    while stack:
        curState, curPath = stack.pop()
        if curState == GOAL_STATE:
            return {
                "path": curPath,
                "steps": len(curPath) - 1,
                "cost": len(curPath) - 1,
                "time": time.time() - start_time,
                "space": max_space
            }
        
        lst_Next_Heuristic = []
        for next_State in get_neighbors(curState):
            if next_State not in visited:
                visited.add(next_State)
                lst_Next_Heuristic.append((manhattan_distance(next_State), next_State))

        if len(lst_Next_Heuristic) == 0:
            return None

        lst_Next_Heuristic.sort(key=lambda x: x[0])

        for _, next_State in reversed(lst_Next_Heuristic): 
            stack.append((next_State, curPath + [next_State]))
            max_space = max(max_space, len(stack))

    return None

def a_start_linear_conflict(start_state):
    start_time = time.time()
    queue = []  
    heapq.heappush(queue, (linear_conflict(start_state), 0, start_state, [start_state]))  # (heuristic_cost, current_cost, current_state, current_path)
    visited = {start_state}
    max_space = 1
    while queue:
        curent_h, curent_g, current_state, current_path = heapq.heappop(queue)
        
        if current_state == GOAL_STATE:
            return {
                "path": current_path,
                "steps": len(current_path) - 1,
                "cost": curent_h + curent_g,
                "time": time.time() - start_time,
                "space": max_space
            }
        
        for next_state in get_neighbors(current_state):
            if next_state not in visited:
                visited.add(next_state)
                next_h = linear_conflict(next_state)  # heuristic for next state
                next_g = curent_g + 1  # actual cost to reach next state
                next_f = next_h + next_g  # total cost = g(n) + h(n)
                heapq.heappush(queue, (next_f, next_g, next_state, current_path + [next_state]))
                max_space = max(max_space, len(queue) + len(visited))
    
    return None

def steepest_hill_climbing(start_state):
    start_time = time.time()  
    cur_State = start_state 
    cur_Path = [cur_State]
    f = manhattan_distance(cur_State)  
    visited = set()
    max_space = 0  

    while True:
        best_neighbor = None
        best_f_value = manhattan_distance(cur_State)
        visited.add(cur_State)
        max_space = max(max_space, len(visited))
        for next_State in get_neighbors(cur_State):
            next_f = manhattan_distance(next_State)
            if next_f < best_f_value:
                best_f_value = next_f
                best_neighbor = next_State

        if best_f_value >= manhattan_distance(cur_State):
            return {
                "path": cur_Path,
                "steps": len(visited) - 1,
                "cost": f,  
                "time": time.time() - start_time,
                "space": max_space
            }
        cur_Path = cur_Path + [best_neighbor]
        cur_State = best_neighbor
        f = best_f_value

def simulated_annealing(start_state):
    start_time = time.time()
    current_state = start_state
    path = [current_state]
    visited = set()
    visited.add(current_state)
    max_space = 1
    temperature = 1000
    iterations = 100000
    cooling_rate = 0.995

    while current_state != GOAL_STATE and iterations > 0:
        neighbors = get_neighbors(current_state)
        next_state = random.choice(neighbors)
        delta = abs(manhattan_distance(next_state) - manhattan_distance(current_state))
        if random.random() < math.exp(-delta / temperature) and next_state not in visited:
            current_state = next_state
            path = path + [current_state]
            visited.add(current_state)
            max_space = max(max_space, len(visited))
        iterations -= 1
        temperature *= cooling_rate


    return {
            "path": path,
            "steps": len(path) - 1,
            "cost": len(path) - 1,
            "time": time.time() - start_time,
            "space": max_space
        }

def beam_search(start_state, beam_width=2):
    start_time = time.time()
    beam = [(manhattan_distance(start_state), start_state, [start_state])]
    visited = set()
    visited.add(start_state)
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
        max_space = max(max_space, len(beam))
        if not beam:
            break
    return None

def q_learning(start_state, episodes=10000, alpha=0.1, gamma=0.9, epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=0.995, q_table_file="q_table.pkl"):
    """Q-learning algorithm for 8-puzzle with Q-table persistence."""
    start_time = time.time()
    actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    # Load existing Q-table if available
    try:
        with open(q_table_file, "rb") as f:
            q_table = pickle.load(f)
            q_table = defaultdict(lambda: np.zeros(4), q_table)  # Convert back to defaultdict
    except FileNotFoundError:
        q_table = defaultdict(lambda: np.zeros(4))  # Initialize new Q-table

    max_space = len(q_table)

    def state_to_tuple(state):
        return tuple(state)

    def get_action(state, epsilon):
        if random.random() < epsilon: # chọn hành động khai phá
            valid_actions = []
            zero_idx = state.index(0)
            row, col = zero_idx // 3, zero_idx % 3
            for i, (dr, dc) in enumerate(actions):
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 3 and 0 <= new_col < 3:
                    valid_actions.append(i)
            return random.choice(valid_actions) if valid_actions else random.randint(0, 3)
        else: # chọn hành động khai thác
            valid_actions = []
            zero_idx = state.index(0)
            row, col = zero_idx // 3, zero_idx % 3
            #q_values = [Q(state,a0), Q(state,a1), Q(state,a2), Q(state,a3)]).
            q_values = q_table[state_to_tuple(state)]
            for i, (dr, dc) in enumerate(actions):
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 3 and 0 <= new_col < 3:
                    valid_actions.append((q_values[i], i))
            if not valid_actions: # Nếu không có hành động hợp lệ, chọn đại một hành động.
                return random.randint(0, 3)
            return max(valid_actions)[1] # Ngược chọn hành động có Q-value cao nhất (max(valid_actions) trả về tuple có Q lớn nhất, [1] là chỉ số hành động).

    def apply_action(state, action_idx):
        zero_idx = state.index(0)
        row, col = zero_idx // 3, zero_idx % 3
        dr, dc = actions[action_idx]
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_idx = new_row * 3 + new_col
            new_state = list(state)
            new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
            return tuple(new_state), -1  # Reward -1 for each move
        return state, -10  # Penalty for invalid move

    # Training phase
    epsilon = epsilon_start
    for episode in range(episodes):
        state = start_state if episode % 100 == 0 else tuple(random.sample(range(9), 9))  # Random state
        if not is_solvable(state):
            continue
        steps = 0
        while steps < 1000000000:  # Max steps per episode
            action = get_action(state, epsilon)
            next_state, reward = apply_action(state, action)
            if next_state == GOAL_STATE:
                reward = 100  # Reward for reaching goal
            next_q_values = q_table[state_to_tuple(next_state)]
            q_table[state_to_tuple(state)][action] += alpha * (
                reward + gamma * np.max(next_q_values) - q_table[state_to_tuple(state)][action]
            )
            state = next_state
            steps += 1
            max_space = max(max_space, len(q_table))
            if state == GOAL_STATE:
                break

        epsilon = max(epsilon_end, epsilon * epsilon_decay)

    # Save Q-table to file
    with open(q_table_file, "wb") as f:
        pickle.dump(dict(q_table), f)

    # Inference phase: find path from start_state
    if not is_solvable(start_state):
        return None
    state = start_state
    path = [state]
    visited = {state}
    steps = 0
    while state != GOAL_STATE and steps < 1000000000:
        action = get_action(state, 0)  # Greedy action (epsilon=0)
        next_state, _ = apply_action(state, action)
        if next_state in visited or next_state == state:
            return None  # Stuck or invalid move
        state = next_state
        path.append(state)
        visited.add(state)
        steps += 1
        max_space = max(max_space, len(q_table))

    if state != GOAL_STATE:
        return None
    
    
    for i, state in enumerate(path):
        q_vals = q_table[state]
        plt.figure()
        plt.plot(['Up', 'Down', 'Left', 'Right'], q_vals, marker='o', linestyle='-', color='b')  # Vẽ đường
        plt.title(f"Step {i}: State = {state}")
        plt.ylabel("Q-value")
        plt.ylim(-10, 100)  # Điều chỉnh tùy theo reward trong thuật toán
        plt.xlabel("Actions")  # Nhãn cho trục x
        plt.grid(True)
        plt.show()

    return {
        "path": path,
        "steps": len(path) - 1,
        "cost": len(path) - 1,
        "time": time.time() - start_time,
        "space": max_space
    }

def belief(start_state, belief_state=(1, 2, 3)):
    """
    Perform DFS search with belief state constraint: only consider states where
    the first row is [1, 2, 3] (i.e., state[0:3] == (1, 2, 3)).
    Returns a dictionary with path, steps, cost, time, and space complexity.
    """
    start_time = time.time()

    def satisfies_belief(state):
        return state[:3] == belief_state  # Kiểm tra 3 vị trí đầu là (1, 2, 3)
    
    # Kiểm tra tính khả nghiệm
    if not is_solvable(start_state):
        return None
    
    stack = [(start_state, [start_state], 0)]  # (state, path, depth)
    visited = {start_state}
    max_space = 1
    
    while stack:
        
        state, path, depth = stack.pop()  # Lấy trạng thái từ đỉnh stack (DFS)
        
        # Kiểm tra trạng thái mục tiêu
        if state == GOAL_STATE:
            return {
                "path": path,
                "steps": len(path) - 1,
                "cost": len(path) - 1,
                "time": time.time() - start_time,
                "space": max_space
            }
        
        # Tạo và kiểm tra các trạng thái lân cận
        for neighbor in get_neighbors(state):
            if neighbor not in visited and satisfies_belief(neighbor):  # Chỉ xét trạng thái thỏa mãn belief
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor], depth + 1))
                max_space = max(max_space, len(stack) + len(visited))
    
    print("Belief: No solution found within constraints!")
    return None