import heapq

queue = []
heapq.heappush(queue, 12)
heapq.heappush(queue, 1123)
heapq.heappush(queue, 1)
heapq.heappush(queue, 1)
heapq.heappush(queue, 123)
a = heapq.heappop(queue)
print(a)