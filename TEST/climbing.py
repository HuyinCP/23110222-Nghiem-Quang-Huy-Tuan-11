import sys
import heapq
sys.stdout = open(r'D:\BAI TAP CAC MON\AI\23110222 Nghiem Quang Huy Tuan 8\TEST\output.txt', 'w')
sys.stdin = open(r'D:\BAI TAP CAC MON\AI\23110222 Nghiem Quang Huy Tuan 8\TEST\input.txt', 'r')


def sol(adj, a, start, end, n, m):
    if start == end:
        return True
    
    fl = False
    next = []
    for x in adj[start]:
        next.append(x)

    for v in adj[start]:
        if a[v - 1] < a[start - 1]:
            fl = True
            if(sol(adj, a, v, end, n, m) == False):
                return True
            
    if fl == False:
        return False
    
    return False

if __name__ == '__main__':
    n, m = map(int, input().split())   
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)

    a = list(map(int, input().split()))
    fl = sol(adj, a, 1, n, n, m)
    print("YES" if fl else "NO")