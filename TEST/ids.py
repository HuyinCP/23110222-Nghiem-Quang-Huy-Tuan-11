import sys
import heapq

sys.stdout = open(r'D:\BAI TAP CAC MON\AI\practic bla bla\output.txt', 'w')
sys.stdin = open(r'D:\BAI TAP CAC MON\AI\practic bla bla\input.txt', 'r')

def dfs(adj, node, goal, depth, visited):
    if node == goal:
        return [node]
    if depth == 0:
        return None

    visited.add(node) 

    for v, w in adj[node]:
        if v not in visited:  
            result = dfs(adj, v, goal, depth - 1, visited)
            if result:
                return [node] + result

    visited.remove(node) 
    return None

def iterative_deepening_search(adj, start, goal):
    depth = 0
    while True:
        visited = set()
        result = dfs(adj, start, goal, depth, visited)
        if result:
            return result
        depth += 1

if __name__ == '__main__':
    n, m, s = map(int, input().split())

    adj = [[] for _ in range(n)]
    
    for _ in range(m):
        u, v, w = map(int, input().split())
        adj[u].append((v, w))
        adj[v].append((u, w))  

    path = iterative_deepening_search(adj, s, n - 1)
    
    if path:
        print("FOUND")
        print(" -> ".join(map(str, path)))
    else:
        print("NOT FOUND")
