# XÂY DỰNG ỨNG DỤNG GIẢI BÀI TOÁN 8 PUZZLE BẰNG CÁC THUẬT TOÁN TÌM KIẾM

## Thông tin đề tài
- **Trường**: HCMC University of Technology and Education  
- **Môn học**: Trí Tuệ Nhân Tạo  
- **Giảng viên hướng dẫn**: TS. Phan Thị Huyền Trang

---

## Mục lục
1. [Mục tiêu](#mục-tiêu)  
2. [Tổng quan các thuật toán áp dụng](#tổng-quan-các-thuật-toán-ápp-dụng)  
   - [Uninformed Search](#1-uninformed-search)  
   - [Informed Search](#2-informed-search)  
   - [Local Search](#3-local-search)  
   - [Complex Spaces Search](#4-complex-spaces-search)  
   - [Constrained Search](#5-constrained-search)  
   - [Reinforcement Learning](#6-reinforcement-learning)

---

## Mục tiêu  
Phát triển ứng dụng giải bài toán **8 Puzzle** sử dụng và so sánh hiệu quả các nhóm thuật toán tìm kiếm phổ biến trong trí tuệ nhân tạo, gồm:

- **Uninformed Search** (Tìm kiếm không thông tin)  
- **Informed Search** (Tìm kiếm có thông tin)  
- **Local Search** (Tìm kiếm cục bộ)  
- **Complex Spaces Search** (Tìm kiếm trong không gian phức tạp)  
- **Constrained Search** (Tìm kiếm có ràng buộc)  
- **Reinforcement Learning** (Học tăng cường)

---

## Tổng quan các thuật toán áp dụng  

### 1. Uninformed Search  
Các thuật toán tìm kiếm không dùng thông tin heuristic như:  
- BFS (Breadth-First Search)  
- DFS (Depth-First Search)  
- UCS (Uniform Cost Search)  
- IDS (Iterative Deepening Search)

### 2. Informed Search  
Các thuật toán dùng heuristic để định hướng tìm kiếm như:  
- A*  
- IDA* (Iterative Deepening A*)  
- Greedy Best-First Search

### 3. Local Search  
Tìm kiếm theo phương pháp cục bộ như:  
- Simple Hill Climb  
- Steepest Hill Climb  
- Stochastic Hill Climb  
- Simulated Annealing  
- Beam Search  
- AND-OR Search  
- Belief Search

### 4. Complex Spaces Search  
Áp dụng các kỹ thuật tìm kiếm trong không gian trạng thái phức tạp hoặc rất lớn, phục vụ các bài toán khó xử lý.

### 5. Constrained Search  
Giải bài toán với các ràng buộc cụ thể, sử dụng các kỹ thuật CSP (Constraint Satisfaction Problem), điển hình như:

- **Backtracking**: phương pháp duyệt không gian trạng thái bằng cách thử từng giá trị và quay lui khi gặp xung đột, giúp tìm lời giải thỏa mãn các ràng buộc.
- Các kỹ thuật bổ trợ như **Forward Checking**, **Constraint Propagation** để tăng hiệu quả tìm kiếm.

### 6. Reinforcement Learning  
Ứng dụng học tăng cường để tìm chính sách giải quyết bài toán thông qua tương tác với môi trường, ví dụ:  
- Q-Learning

---

*Cảm ơn bạn đã quan tâm!*
