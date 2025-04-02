import sys
import heapq
sys.stdout = open(r'D:\BAI TAP CAC MON\AI\practic bla bla\output.txt', 'w')
sys.stdin = open(r'D:\BAI TAP CAC MON\AI\practic bla bla\input.txt', 'r')



def dijkstra(n, m, start, adj):
    dp = [float('inf')] * (n)
    dp[0] = 0
    pq = [(0, start)]
    while pq:
        dist, u = heapq.heappop(pq)
        
        if dist > dp[u]:
            continue

        for v, w in adj[u]:
            if dp[u] + w < dp[v]:
                dp[v] = dp[u] + w
                heapq.heappush(pq, (dp[v], v))

    return [d if d < float('inf') else -1 for d in dp]
    

if __name__ == '__main__':
    n, m, s = map(int, input().split())   
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, w = map(int, input().split())
        adj[v].append((u, w))
        adj[u].append((v, w))

    res = dijkstra(n, m, s, adj)
    print(res)