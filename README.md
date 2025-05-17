# XÂY DỰNG ỨNG DỤNG GIẢI BÀI TOÁN 8 PUZZLE BẰNG CÁC THUẬT TOÁN TÌM KIẾM

## Thông tin đề tài
- **Trường**: HCMC University of Technology and Education  
- **Môn học**: Trí Tuệ Nhân Tạo  
- **Giảng viên hướng dẫn**: TS. Phan Thị Huyền Trang

---

## Mục lục
1. [Mục tiêu](#mục-tiêu)  
2. [Tổng quan các thuật toán áp dụng](#tổng-quan-các-thuật-toán-áp-dụng)  
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
Các thuật toán tìm kiếm không dùng thông tin heuristic, hoạt động hoàn toàn dựa vào cấu trúc không gian trạng thái:

#### ▸ Breadth-First Search (BFS)
- **Chiến lược**: Duyệt theo **chiều rộng**, mở rộng từng lớp trước khi xuống sâu hơn.
- **Cấu trúc dữ liệu**: Hàng đợi (First In First Out).
- **Ưu điểm**: Tìm được lời giải **ngắn nhất** nếu chi phí đều.
- **Nhược điểm**: Tốn bộ nhớ khi không gian tìm kiếm rộng.
- **Phức tạp**:
  - Thời gian: \(O(b^d)\)  
  - Bộ nhớ: \(O(b^d)\)
- **Giải thích các ký hiệu**:
  - \(b\) (branching factor): số lượng trạng thái con trung bình mà mỗi trạng thái sinh ra. Trong bài toán 8 Puzzle, tối đa là 4.
  - \(d\) (depth): độ sâu của nút giải pháp trong cây tìm kiếm, tức số bước di chuyển từ trạng thái ban đầu đến trạng thái đích.
- **Áp dụng trong 8 Puzzle**:  
  BFS sẽ duyệt theo từng lớp trạng thái, từ trạng thái ban đầu mở rộng tất cả các trạng thái có thể đi tới sau 1 bước, sau đó 2 bước, ... cho tới khi tìm được trạng thái đích.

#### ▸ Depth-First Search (DFS)
- **Chiến lược**: Duyệt **sâu trước**, mở rộng hết một nhánh rồi quay lại.
- **Cấu trúc dữ liệu**: Ngăn xếp (Last In First Out).
- **Ưu điểm**: Tốn ít bộ nhớ hơn BFS.
- **Nhược điểm**: Không đảm bảo tìm lời giải ngắn nhất, dễ rơi vào vòng lặp nếu không kiểm tra trạng thái đã duyệt.
- **Phức tạp**:
  - Thời gian: \(O(b^m)\)  
  - Bộ nhớ: \(O(bm)\)
- **Giải thích các ký hiệu**:
  - \(b\) là branching factor, tối đa 4 ở bài 8 Puzzle.
  - \(m\) là độ sâu lớn nhất có thể tìm được (có thể rất sâu).
- **Áp dụng trong 8 Puzzle**:  
  DFS sẽ đi sâu vào một chuỗi trạng thái cho tới khi đạt tới trạng thái đích hoặc không còn đường đi tiếp, rồi quay lui để thử nhánh khác.

#### ▸ Uniform Cost Search (UCS)
- **Chiến lược**: Mở rộng node có **tổng chi phí thấp nhất** từ gốc đến trạng thái hiện tại.
- **Cấu trúc dữ liệu**: Hàng đợi ưu tiên (Priority Queue).
- **Ưu điểm**: Tìm lời giải **tối ưu** nếu chi phí luôn dương.
- **Nhược điểm**: Tốn bộ nhớ và thời gian như BFS trong không gian lớn.
- **Phức tạp**:
  - Thời gian và bộ nhớ:
  
  $$
  O\left(b^{1 + \frac{C^*}{\varepsilon}}\right)
  $$
  
  - Trong đó:
    - \(b\) là branching factor.
    - \(C^*\) là chi phí tối ưu của lời giải.
    - \(\varepsilon\) là bước chi phí nhỏ nhất.
- **Áp dụng trong 8 Puzzle**:  
  UCS mở rộng trạng thái theo thứ tự tổng chi phí nhỏ nhất, thích hợp khi mỗi bước di chuyển có chi phí khác nhau (ví dụ, chi phí di chuyển khác nhau giữa các hướng).

#### ▸ Iterative Deepening Search (IDS)
- **Chiến lược**: Kết hợp DFS và BFS bằng cách lặp lại DFS với giới hạn độ sâu tăng dần.
- **Ưu điểm**: Tìm lời giải ngắn nhất như BFS, nhưng tốn bộ nhớ ít như DFS.
- **Nhược điểm**: Tốn thời gian do lặp lại các node nhiều lần.
- **Phức tạp**:
  - Thời gian: \(O(b^d)\)  
  - Bộ nhớ: \(O(bd)\)
- **Giải thích các ký hiệu**:
  - \(b\) là branching factor.
  - \(d\) là độ sâu lời giải.
- **Áp dụng trong 8 Puzzle**:  
  IDS sẽ thực hiện DFS với độ sâu 0, rồi 1, rồi 2... cho tới khi tìm được trạng thái đích.

---

Bạn có muốn mình mở rộng phần **Informed Search** hay các nhóm thuật toán khác chi tiết như vậy không?
