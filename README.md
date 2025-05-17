# 🧩 Xây dựng ứng dụng giải bài toán 8 Puzzle bằng các thuật toán tìm kiếm

## Thông tin đề tài

* **Trường**: HCMC University of Technology and Education
* **Môn học**: Trí Tuệ Nhân Tạo
* **Giảng viên hướng dẫn**: TS. Phan Thị Huyền Trang
* **Mã số sinh viên**: 23110222
* **Tên sinh viên**: Nghiêm Quang Huy 

---

## Mục lục

1. [Giới thiệu bài toán 8 Puzzle](#giới-thiệu-bài-toán-8-puzzle)
2. [Mục tiêu](#mục-tiêu)
3. [Tổng quan các thuật toán áp dụng](#tổng-quan-các-thuật-toán-áp-dụng)
   * [Uninformed Search](#1-uninformed-search)
   * [Informed Search](#2-informed-search)
   * [Local Search](#3-local-search)
   * [Complex Spaces Search](#4-complex-spaces-search)
   * [Reinforcement Learning](#5-reinforcement-learning)
---

## Giới thiệu bài toán 8 Puzzle

Bài toán **8 Puzzle** là một trò chơi xếp hình kinh điển, bao gồm một bảng 3x3 với 8 ô được đánh số từ 1 đến 8 và một ô trống (ký hiệu là 0). Người chơi di chuyển ô trống (lên, xuống, trái, phải) để sắp xếp các ô số về trạng thái mục tiêu: `[1, 2, 3, 4, 5, 6, 7, 8, 0]

Dự án này phát triển một ứng dụng sử dụng các thuật toán trí tuệ nhân tạo để tự động giải bài toán 8 Puzzle, đồng thời so sánh hiệu quả của các thuật toán dựa trên số bước, thời gian, và bộ nhớ sử dụng.

---

## Mục tiêu

Phát triển ứng dụng giải bài toán **8 Puzzle** 🧩, sử dụng và so sánh hiệu quả các nhóm thuật toán tìm kiếm phổ biến trong trí tuệ nhân tạo, gồm:

* **Uninformed Search** (Tìm kiếm không thông tin)
* **Informed Search** (Tìm kiếm có thông tin)
* **Local Search** (Tìm kiếm cục bộ)
* **Complex Spaces Search** (Tìm kiếm trong không gian phức tạp)
* **Reinforcement Learning** (Học tăng cường)

---

## Tổng quan các thuật toán áp dụng

### 1. Uninformed Search

Các thuật toán tìm kiếm không dùng thông tin heuristic, hoạt động dựa trên cấu trúc không gian trạng thái của 8 Puzzle:

#### ▸ Breadth-First Search (BFS)
* **Chiến lược**: Duyệt theo **chiều rộng**, mở rộng từng lớp trước khi xuống sâu hơn.
* **Cấu trúc dữ liệu**: Queue.
* **Ưu điểm**: Tìm được lời giải **ngắn nhất** nếu chi phí đều.
* **Nhược điểm**: Tốn bộ nhớ khi không gian tìm kiếm rộng (9! = 362,880 trạng thái).
* **Độ phức tạp**:
  - Thời gian: `O(b^d)`
  - Bộ nhớ: `O(b^d)`
  - Trong đó:
    * `b` (branching factor): số lượng trạng thái con trung bình (~4 trong 8 Puzzle).
    * `d` (depth): độ sâu của trạng thái mục tiêu trong cây.

#### ▸ Depth-First Search (DFS)
* **Chiến lược**: Duyệt **sâu trước**, mở rộng hết một nhánh rồi quay lại.
* **Cấu trúc dữ liệu**: Stack.
* **Ưu điểm**: Tốn ít bộ nhớ.
* **Nhược điểm**: Không đảm bảo tìm lời giải ngắn nhất, dễ đi vào vòng lặp nếu không kiểm tra trạng thái.
* **Độ phức tạp**:
  - Thời gian: `O(b^m)`
  - Bộ nhớ: `O(bm)`
  - Trong đó:
    * `b` (branching factor): số lượng trạng thái con trung bình (~4 trong 8 Puzzle).
    * `m` (maximum depth): độ sâu lớn nhất mà DFS có thể đi tới trong cây.

#### ▸ Uniform Cost Search (UCS)
* **Chiến lược**: Mở rộng node có **tổng chi phí thấp nhất** từ gốc đến hiện tại.
* **Cấu trúc dữ liệu**: Priority Queue.
* **Ưu điểm**: Tìm lời giải **tối ưu** nếu chi phí luôn dương.
* **Nhược điểm**: Tốn bộ nhớ và thời gian như BFS trong không gian lớn.
* **Độ phức tạp**:
  - Thời gian: `O(b^{1 + C*/ε})`
  - Bộ nhớ: `O(b^{1 + C*/ε})`
  - Trong đó:
    * `C*`: chi phí tối ưu để tìm lời giải.
    * `ε`: bước chi phí nhỏ nhất.
    * `b` (branching factor): số lượng trạng thái con trung bình (~4 trong 8 Puzzle).

#### ▸ Iterative Deepening Search (IDS)
* **Chiến lược**: Kết hợp DFS và BFS bằng cách lặp lại DFS với giới hạn độ sâu tăng dần.
* **Ưu điểm**: Tìm được lời giải **ngắn nhất** như BFS nhưng **tốn ít bộ nhớ** như DFS.
* **Nhược điểm**: Tốn thời gian do lặp lại các node.
* **Độ phức tạp**:
  - Thời gian: `O(b^d)`
  - Bộ nhớ: `O(bd)`
  - Trong đó:
    * `b` (branching factor): số lượng trạng thái con trung bình (~4 trong 8 Puzzle).
    * `d` (depth): độ sâu của trạng thái mục tiêu trong cây.

---

### 2. Informed Search

Các thuật toán sử dụng heuristic để ước lượng chi phí từ trạng thái hiện tại đến đích, ưu tiên mở rộng các trạng thái có khả năng dẫn đến lời giải nhanh hơn. Trong bài toán **8 Puzzle**, các thuật toán nhóm Informed Search bao gồm:

* Greedy Best-First Search
* A* Search
* Iterative Deepening A* (IDA*)

#### ▸ Greedy Best-First Search (GBFS)
* **Chiến lược**: Mở rộng trạng thái lân cận có giá trị heuristic `h(n)` nhỏ nhất (sử dụng Manhattan Distance).
* **Cấu trúc dữ liệu**: Priority Queue (min heap).
* **Ưu điểm**:
  - Tìm kiếm nhanh, tận dụng thông tin heuristic để đi thẳng đến đích.
  - Tiết kiệm bộ nhớ hơn so với BFS hay UCS nếu heuristic tốt.
* **Nhược điểm**:
  - Không đảm bảo tìm ra lời giải tối ưu (ngắn nhất).
  - Có thể bị mắc kẹt nếu heuristic không chính xác.
* **Độ phức tạp**:
  - Thời gian và bộ nhớ trong trường hợp xấu nhất: `O(b^m)`
  - Trong đó:
    * `b` (branching factor): số lượng trạng thái con trung bình (~4 trong 8 Puzzle).
    * `m` (maximum depth): độ sâu lớn nhất mà thuật toán có thể đi tới.

#### ▸ A* Search
* **Chiến lược**: Kết hợp chi phí thực tế từ gốc đến hiện tại `g(n)` và ước lượng chi phí đến đích heuristic `h(n)` để đánh giá node theo `f(n) = g(n) + h(n)` (sử dụng Manhattan Distance hoặc Linear Conflict).
* **Ưu điểm**:
  - Tìm được lời giải tối ưu nếu heuristic là **đúng và không vượt quá thực tế**.
  - Hiệu quả hơn so với tìm kiếm không thông tin.
* **Nhược điểm**: Tốn bộ nhớ lớn khi không gian tìm kiếm rộng.
* **Độ phức tạp**:
  - Thời gian: `O(b^d)` (phụ thuộc vào heuristic).
  - Bộ nhớ: `O(b^d)`
  - Trong đó:
    * `b` (branching factor): số lượng trạng thái con trung bình (~4 trong 8 Puzzle).
    * `d` (depth): độ sâu của trạng thái mục tiêu trong cây.

#### ▸ Iterative Deepening A* (IDA*)
* **Chiến lược**: Kết hợp IDS và A* bằng cách lặp lại tìm kiếm sâu với ngưỡng `f(n)` tăng dần, chỉ mở rộng các nút có `f(n) <= ngưỡng hiện tại` (sử dụng Manhattan Distance).
* **Ưu điểm**:
  - Giảm bộ nhớ sử dụng so với A*.
  - Vẫn giữ được tính tối ưu của A*.
* **Nhược điểm**: Có thể lặp lại mở rộng node nhiều lần, gây tốn thời gian.
* **Độ phức tạp**:
  - Thời gian: `O(b^d)`
  - Bộ nhớ: `O(d)`
  - Trong đó:
    * `b` (branching factor): số lượng trạng thái con trung bình (~4 trong 8 Puzzle).
    * `d` (depth): độ sâu của trạng thái mục tiêu trong cây.

---

### 3. Local Search

Tìm kiếm theo hướng cải thiện trạng thái hiện tại mà không cần lưu toàn bộ đường đi, phù hợp với không gian trạng thái lớn của 8 Puzzle. Các thuật toán nhóm Local Search bao gồm:

* Hill Climbing (Simple, Steepest, Stochastic)
* Simulated Annealing
* Beam Search

#### ▸ Simple Hill Climbing
* **Chiến lược**: Chọn trạng thái lân cận đầu tiên có giá trị heuristic tốt hơn (sử dụng Manhattan Distance).
* **Ưu điểm**: Cài đặt đơn giản, tốc độ nhanh.
* **Nhược điểm**: Dễ kẹt ở local optimum hoặc vùng phẳng (plateau).
* **Độ phức tạp**:
  - Thời gian: `O(bm)`
  - Bộ nhớ: `O(1)`
  - Trong đó:
    * `b` (branching factor): số lượng trạng thái con trung bình (~4 trong 8 Puzzle).
    * `m` (maximum depth): độ sâu lớn nhất mà thuật toán có thể đi tới.

#### ▸ Steepest Hill Climbing
* **Chiến lược**: So sánh toàn bộ trạng thái lân cận và chọn trạng thái có giá trị heuristic tốt nhất (sử dụng Manhattan Distance).
* **Ưu điểm**: Tăng khả năng tránh lựa chọn sai như Simple Hill Climbing.
* **Nhược điểm**: Tốn thời gian để đánh giá toàn bộ lân cận; vẫn dễ bị kẹt ở local optimum.
* **Độ phức tạp**:
  - Thời gian: `O(bm)`
  - Bộ nhớ: `O(1)`
  - Trong đó:
    * `b` (branching factor): số lượng trạng thái con trung bình (~4 trong 8 Puzzle).
    * `m` (maximum depth): độ sâu lớn nhất mà thuật toán có thể đi tới.

#### ▸ Stochastic Hill Climbing
* **Chiến lược**: Chọn ngẫu nhiên một trong các trạng thái lân cận có cải thiện heuristic (sử dụng Manhattan Distance).
* **Ưu điểm**: Tăng khả năng thoát local optimum, tránh rơi vào vùng phẳng.
* **Nhược điểm**: Kết quả không ổn định, phụ thuộc vào ngẫu nhiên.
* **Độ phức tạp**:
  - Thời gian: `O(bm)`
  - Bộ nhớ: `O(1)`
  - Trong đó:
    * `b` (branching factor): số lượng trạng thái con trung bình (~4 trong 8 Puzzle).
    * `m` (maximum depth): độ sâu lớn nhất mà thuật toán có thể đi tới.

#### ▸ Simulated Annealing
* **Chiến lược**: Cho phép chọn trạng thái xấu hơn với xác suất giảm dần theo thời gian, tránh mắc kẹt ở local optimum (sử dụng Manhattan Distance).
* **Ưu điểm**: Có thể thoát local optimum và tìm lời giải tốt hơn.
* **Nhược điểm**: Hiệu quả phụ thuộc vào cách giảm nhiệt độ (cooling schedule).
* **Độ phức tạp**:
  - Thời gian: `O(bm)`
  - Bộ nhớ: `O(1)`
  - Trong đó:
    * `b` (branching factor): số lượng trạng thái con trung bình (~4 trong 8 Puzzle).
    * `m` (maximum depth): độ sâu lớn nhất mà thuật toán có thể đi tới.

#### ▸ Beam Search
* **Chiến lược**: Giữ lại `k` trạng thái tốt nhất tại mỗi bước (k gọi là beam width) thay vì chỉ một (sử dụng Manhattan Distance).
* **Ưu điểm**: Dễ mở rộng, tránh kẹt local optimum tốt hơn Hill Climbing.
* **Nhược điểm**: Không đảm bảo tối ưu, dễ bỏ sót lời giải nếu `k` quá nhỏ.
* **Độ phức tạp**:
  - Thời gian: `O(kbm)`
  - Bộ nhớ: `O(k)`
  - Trong đó:
    * `b` (branching factor): số lượng trạng thái con trung bình (~4 trong 8 Puzzle).
    * `m` (maximum depth): độ sâu lớn nhất mà thuật toán có thể đi tới.
    * `k` (beam width): số trạng thái tốt nhất được giữ lại.

---

### 4. Complex Spaces Search

Các kỹ thuật dành cho không gian tìm kiếm lớn hoặc có cấu trúc phức tạp trong 8 Puzzle. Các thuật toán nhóm Complex Spaces Search bao gồm:

* AND-OR Graph Search
* Belief Search

#### ▸ AND-OR Graph Search
* **Chiến lược**: Kết hợp node "AND" (cần tất cả con) và "OR" (chỉ cần một con), sử dụng Manhattan Distance để ưu tiên.
* **Ưu điểm**: Tốt cho các hệ thống có nhiều kết quả khả thi phụ thuộc vào hành động.
* **Nhược điểm**: Cấu trúc phức tạp, khó triển khai với không gian lớn như 8 Puzzle.
* **Độ phức tạp**:
  - Thời gian: `O(bm)`
  - Bộ nhớ: `O(b^d)`
  - Trong đó:
    * `b` (branching factor): số lượng trạng thái con trung bình (~4 trong 8 Puzzle).
    * `d` (depth): độ sâu của trạng thái mục tiêu trong cây.

#### ▸ Belief Search
* **Chiến lược**: Tìm kiếm với ràng buộc belief state (ví dụ: hàng đầu tiên là [1, 2, 3]), sử dụng DFS.
* **Ưu điểm**: Áp dụng được trong môi trường không chắc chắn.
* **Nhược điểm**: Không phù hợp với bài toán xác định như 8 Puzzle, giới hạn không gian tìm kiếm.
* **Độ phức tạp**:
  - Thời gian: `O(b^m)`
  - Bộ nhớ: `O(b^m * N)`
  - Trong đó:
    * `b` (branching factor): số lượng trạng thái con trung bình (~4 trong 8 Puzzle).
    * `m` (maximum depth): độ sâu lớn nhất mà thuật toán có thể đi tới.
    * `N`: số lượng trạng thái trong không gian ban đầu (với 8 Puzzle là 9! = 362,880).

---

### 5. Reinforcement Learning

Tìm chính sách hành động tối ưu thông qua tương tác với môi trường 8 Puzzle:

#### ▸ Q-Learning
* **Chiến lược**: Học chính sách hành động bằng cách cập nhật Q-table, sử dụng epsilon-greedy để cân bằng khám phá và khai thác.
* **Ưu điểm**: Có thể học từ môi trường mà không cần heuristic.
* **Nhược điểm**: Tốn thời gian huấn luyện, phụ thuộc vào tham số (alpha, gamma, epsilon).
* **Độ phức tạp**:
  - Thời gian: Phụ thuộc vào số episode và bước tối đa mỗi episode.
  - Bộ nhớ: Tăng theo kích thước Q-table.

---
