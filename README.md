# XÂY DỰNG ỨNG DỤNG GIẢI BÀI TOÁN 8 PUZZLE BẰNG CÁC THUẬT TOÁN TÌM KIẾM

## Thông tin đề tài

* **Trường**: HCMC University of Technology and Education
* **Môn học**: Trí Tuệ Nhân Tạo
* **Giảng viên hướng dẫn**: TS. Phan Thị Huyền Trang
* **Mã số sinh viên**: 23110222
* **Tên sinh viên**: Nghiêm Quang Huy 

---

## Mục lục

1. [Mục tiêu](#mục-tiêu)
2. [Tổng quan các thuật toán áp dụng](#tổng-quan-các-thuật-toán-áp-dụng)

   * [Uninformed Search](#1-uninformed-search)
   * [Informed Search](#2-informed-search)
   * [Local Search](#3-local-search)
   * [Complex Spaces Search](#4-complex-spaces-search)
   * [Constrained Search](#5-constrained-search)
   * [Reinforcement Learning](#6-reinforcement-learning)

---

## Mục tiêu

Phát triển ứng dụng giải bài toán **8 Puzzle** sử dụng và so sánh hiệu quả các nhóm thuật toán tìm kiếm phổ biến trong trí tuệ nhân tạo, gồm:

* **Uninformed Search** (Tìm kiếm không thông tin)
* **Informed Search** (Tìm kiếm có thông tin)
* **Local Search** (Tìm kiếm cục bộ)
* **Complex Spaces Search** (Tìm kiếm trong không gian phức tạp)
* **Constrained Search** (Tìm kiếm có ràng buộc)
* **Reinforcement Learning** (Học tăng cường)

---

## Tổng quan các thuật toán áp dụng

### 1. Uninformed Search

Các thuật toán tìm kiếm không dùng thông tin heuristic, hoạt động hoàn toàn dựa vào cấu trúc không gian trạng thái:

#### ▸ Breadth-First Search (BFS)
* **Chiến lược**: Duyệt theo **chiều rộng**, mở rộng từng lớp trước khi xuống sâu hơn.
* **Cấu trúc dữ liệu**: Queue.
* **Ưu điểm**: Tìm được lời giải **ngắn nhất** nếu chi phí đều.
* **Nhược điểm**: Tốn bộ nhớ khi không gian tìm kiếm rộng.
* **Độ phức tạp**:
  - Thời gian: `O(b^d)`
  - Bộ nhớ: `O(b^d)`
  - Trong đó:
     * b (branching factor): số lượng trạng thái con trung. Trong 8 Puzzle, tối đa có 4 nước đi (lên, xuống, trái, phải), vậy b = 4.
     * d (depth): độ sâu của nút GOAL_STATE trong cây.

#### ▸ Depth-First Search (DFS)
* **Chiến lược**: Duyệt **sâu trước**, mở rộng hết một nhánh rồi quay lại.
* **Cấu trúc dữ liệu**: Stack.
* **Ưu điểm**: Tốn ít bộ nhớ.
* **Nhược điểm**: Không đảm bảo tìm lời giải ngắn nhất, dễ đi vào vòng lặp nếu không kiểm tra trạng thái.
* **Độ phức tạp**:
  - Thời gian: `O(b^m)`
  - Bộ nhớ: `O(bm)`
  - Trong đó:
      * `b` (branching factor): số lượng trạng thái con trung. Trong 8 Puzzle, tối đa có 4 nước đi (lên, xuống, trái, phải), vậy b = 4.
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
      * `C*` là chi phí tối ưu và `ε` là bước chi phí nhỏ nhất.
      * `b` (branching factor): số lượng trạng thái con trung. Trong 8 Puzzle, tối đa có 4 nước đi (lên, xuống, trái, phải), vậy b = 4.
      * `C^*`: chi phí tối ưu để tìm lời giải
      * `ε`: là bước chi phí nhỏ nhất.

#### ▸ Iterative Deepening Search (IDS)
* **Chiến lược**: Kết hợp DFS và BFS bằng cách lặp lại DFS với giới hạn độ sâu tăng dần.
* **Ưu điểm**: Tìm được lời giải **ngắn nhất** như BFS nhưng **tốn ít bộ nhớ** như DFS.
* **Nhược điểm**: Tốn thời gian do lặp lại các node.
* **Độ phức tạp**:
  - Thời gian: `O(b^d)`
  - Bộ nhớ: `O(bd)`
  - Trong đó:
       * `b` (branching factor): số lượng trạng thái con trung. Trong 8 Puzzle, tối đa có 4 nước đi (lên, xuống, trái, phải), vậy `b` = 4.
       * `d` (depth): độ sâu của nút GOAL_STATE trong cây.

---

### 2. Informed Search

Các thuật toán sử dụng heuristic để ước lượng chi phí từ trạng thái hiện tại đến đích, ưu tiên mở rộng các trạng thái có khả năng dẫn đến lời giải nhanh hơn.
Trong bài toán **8 Puzzle**, các thuật toán Informed Search như:

- Greedy Best-First Search  
- A* Search  
- Iterative Deepening A* (IDA*)  

#### ▸ Greedy Best-First Search (GBFS)
* **Chiến lược**: Giả sử đang đứng ở trạng thái X thì ta luôn mở rộng trạng thái lận cận X có giá trị heuristic `h(n)` nhỏ nhất.
* **Cấu trúc dữ liệu**: Priority Queue (min heap).
* **Ưu điểm**:  
  - Tìm kiếm nhanh, tận dụng thông tin heuristic để đi thẳng đến đích.  
  - Tiết kiệm bộ nhớ hơn so với các thuật toán tìm kiếm không thông tin như BFS hay UCS nếu heuristic tốt.
* **Nhược điểm**:  
  - Không đảm bảo tìm ra lời giải tối ưu (ngắn nhất).  
  - Có thể bị mắc kẹt ở các điểm local minima hoặc đi sai hướng nếu heuristic không chính xác.
* **Độ phức tạp**:  
  - Thời gian và bộ nhớ trong trường hợp xấu nhất: `O(b^m)`:
  - Trong đó:
    - `b`: (branching factor): số lượng trạng thái con trung. Trong 8 Puzzle, tối đa có 4 nước đi (lên, xuống, trái, phải), vậy b = 4.
    - `m`: (maximum depth): độ sâu lớn nhất mà DFS có thể đi tới trong cây.

#### ▸ A* Search
* **Chiến lược**: Kết hợp chi phí thực tế đã đi từ gốc đến hiện tại `g(n)` và ước lượng chi phí đến đích heuristic `h(n)` để đánh giá node theo `f(n) = g(n) + h(n)`.
* **Ưu điểm**:  
  - Tìm được lời giải tối ưu nếu heuristic là **đúng và không vượt quá thực tế**. 
  - Hiệu quả hơn so với tìm kiếm không thông tin.
* **Nhược điểm**: Tốn bộ nhớ lớn khi không gian tìm kiếm rộng.
* **Độ phức tạp**:
  - Thời gian: 
    - Trường hợp xấu nhất là `O(b^d)`.
    - Phụ thuộc vào cách thiết kế heuristic, heuristic tốt thì khả năng cao tìm nhanh, heuristic xấu thì khả năng cao tìm lâu.
  - Bộ nhớ: 
    - `O(b^d)`, vì A* lưu toàn bộ các node đã duyệt trong bộ nhớ để tránh lặp lại và đảm bảo tìm lời giải tối ưu.
  - Trong đó:
    - `b`: (branching factor): số lượng trạng thái con trung. Trong 8 Puzzle, tối đa có 4 nước đi (lên, xuống, trái, phải), vậy b = 4.
    - `m`: (maximum depth): độ sâu lớn nhất mà DFS có thể đi tới trong cây.

#### ▸ Iterative Deepening A* (IDA*)
* **Chiến lược**: Kết hợp ý tưởng IDS và A* bằng cách lặp lại tìm kiếm sâu với ngưỡng giới hạn tăng dần, mỗi lần tìm kiếm sâu chỉ mở rộng các nút có `f(n) <= ngưỡng hiện tại` trong đó `f(n) tương tự của A*.
* **Ưu điểm**:  
  - Giảm bộ nhớ sử dụng so với A*.  
  - Vẫn giữ được tính tối ưu của A*.
* **Nhược điểm**: Có thể lặp lại mở rộng node nhiều lần, gây tốn thời gian.
* **Độ phức tạp**:
  - Thời gian: 
    - Trường hợp xấu nhất là `O(b^d)`.
  - Bộ nhớ:
  - Trong đó:
    - `O(d)`, vì IDA* chỉ lưu trữ đường đi hiện tại trong stack thay thì toàn bộ cây như A*.
    - `b`: (branching factor): số lượng trạng thái con trung. Trong 8 Puzzle, tối đa có 4 nước đi (lên, xuống, trái, phải), vậy b = 4.
    - `m`: (maximum depth): độ sâu lớn nhất mà DFS có thể đi tới trong cây.

---


### 3. Local Search

Tìm kiếm theo hướng cải thiện trạng thái hiện tại mà không cần lưu toàn bộ đường đi, phù hợp với không gian trạng thái lớn hoặc không rõ ràng về đích cụ thể:

* Hill Climbing (Simple, Steepest, Stochastic)
* Simulated Annealing
* Beam Search
* AND-OR Graph Search
* Belief Search

#### ▸ Simple Hill Climbing
* **Chiến lược**: Từ trạng thái hiện tại, chọn trạng thái đầu tiên có giá trị heuristic tốt hơn, nói cách khác chọn next_state đầu tiên sao cho `h(current_state) < h(next_state)`.
* **Ưu điểm**: Cài đặt đơn giản, tốc độ nhanh
* **Nhược điểm**: Dễ kẹt ở local optimum, plateau hoặc điểm cao giả (shoulder).
* **Độ phức tạp**:
  - Thời gian: 
    - Trường hợp xấu nhất là `O(bm)`.
  - Bộ nhớ: 
    - `O(1)`.
  - Trong đó:
    - `b`: (branching factor): số lượng trạng thái con trung. Trong 8 Puzzle, tối đa có 4 nước đi (lên, xuống, trái, phải), vậy b = 4.
    - `m`: (maximum depth): độ sâu lớn nhất mà DFS có thể đi tới trong cây.

#### ▸ Steepest Hill Climbing
* **Chiến lược**: So sánh toàn bộ trạng thái lân cận và chọn trạng thái có giá trị heuristic tốt nhất.
* **Ưu điểm**: Tăng khả năng tránh lựa chọn sai như Simple Hill Climbing.
* **Nhược điểm**: Tốn thời gian để đánh giá toàn bộ lân cận; vẫn dễ bị kẹt ở local optimum.
* **Độ phức tạp**:
  - Thời gian: 
    - Trường hợp xấu nhất là `O(bm)`.
  - Bộ nhớ: 
    - `O(1)`.
  - Trong đó:
    - `b`: (branching factor): số lượng trạng thái con trung. Trong 8 Puzzle, tối đa có 4 nước đi (lên, xuống, trái, phải), vậy b = 4.
    - `m`: (maximum depth): độ sâu lớn nhất mà DFS có thể đi tới trong cây.

#### ▸ Stochastic Hill Climbing
* **Chiến lược**: Chọn ngẫu nhiên một trong các trạng thái lân cận có cải thiện heuristic, thay vì chọn tốt nhất.
* **Ưu điểm**: Tăng khả năng thoát local optimum, tránh rơi vào vùng phẳng (plateau).
* **Nhược điểm**: Kết quả không ổn định, phụ thuộc vào ngẫu nhiên.
* **Độ phức tạp**:
  - Thời gian: 
    - Trường hợp xấu nhất là `O(bm)`.
  - Bộ nhớ: 
    - `O(1)`.
  - Trong đó:
    - `b`: (branching factor): số lượng trạng thái con trung. Trong 8 Puzzle, tối đa có 4 nước đi (lên, xuống, trái, phải), vậy b = 4.
    - `m`: (maximum depth): độ sâu lớn nhất mà DFS có thể đi tới trong cây.

#### ▸ Simulated Annealing
* **Chiến lược**: Cho phép chọn trạng thái xấu hơn với xác suất giảm dần theo thời gian, tránh mắc kẹt ở local optimum.
* **Ưu điểm**: Có thể thoát local optimum và tìm lời giải tốt hơn.
* **Nhược điểm**: Hiệu quả phụ thuộc vào cách giảm nhiệt độ (cooling schedule).
* **Độ phức tạp**:
  - Thời gian: 
    - Trường hợp xấu nhất là `O(bm)`.
  - Bộ nhớ: 
    - `O(1)`.
  - Trong đó:
    - `b`: (branching factor): số lượng trạng thái con trung. Trong 8 Puzzle, tối đa có 4 nước đi (lên, xuống, trái, phải), vậy b = 4.
    - `m`: (maximum depth): độ sâu lớn nhất mà DFS có thể đi tới trong cây.

#### ▸ Beam Search
* **Chiến lược**: Tại mỗi bước, giữ lại `k` trạng thái tốt nhất (k gọi là beam width) thay vì chỉ một.
* **Ưu điểm**: Dễ mở rộng, tránh kẹt local optimum tốt hơn Hill Climbing.
* **Nhược điểm**: Không đảm bảo tối ưu, dễ bỏ sót lời giải nếu `k` quá nhỏ.
* **Độ phức tạp**:
  - Thời gian: 
    - Trường hợp xấu nhất `O(kbm)`.
  - Bộ nhớ: 
    - `O(k)`.
  - Trong đó:
    - `b`: (branching factor): số lượng trạng thái con trung. Trong 8 Puzzle, tối đa có 4 nước đi (lên, xuống, trái, phải), vậy b = 4.
    - `m`: (maximum depth): độ sâu lớn nhất mà DFS có thể đi tới trong cây.
    - `k`: (beam width): k trạng thái tốt nhất.

### 4. Complex Spaces Search

Các kỹ thuật dành cho không gian tìm kiếm rất lớn hoặc có cấu trúc phức tạp. Có thể áp dụng tree decomposition, domain-specific search, hoặc phân cụm trạng thái.

#### ▸ AND-OR Graph Search
* **Chiến lược**: Dành cho bài toán có tính phân nhánh điều kiện (non-deterministic); kết hợp cả node "AND" (cần tất cả con) và "OR" (chỉ cần một con).
* **Ưu điểm**: Tốt cho các hệ thống có nhiều kết quả khả thi phụ thuộc vào hành động.
* **Nhược điểm**: Cấu trúc phức tạp, khó triển khai với không gian lớn như 8 Puzzle.
* **Độ phức tạp**:
  - Thời gian: 
    - Trường hợp xấu nhất là `O(bm)`.
  - Bộ nhớ: 
    - `O(b^d)`.
  - Trong đó:
    - `b`: (branching factor): số lượng trạng thái con trung. Trong 8 Puzzle, tối đa có 4 nước đi (lên, xuống, trái, phải), vậy b = 4.
    - `d` (depth): độ sâu của nút GOAL_STATE trong cây.

#### ▸ Belief Search
* **Chiến lược**: Tìm kiếm trong không gian xác suất (belief space), nơi trạng thái không xác định chính xác mà là một phân phối xác suất..
* **Ưu điểm**: Áp dụng được trong môi trường không chắc chắn, ví dụ như robot sensing.
* **Nhược điểm**: Không phù hợp với bài toán xác định như 8 Puzzle, tính toán phức tạp.
* **Độ phức tạp**:
  - Thời gian: 
    - Trường hợp xấu nhất là `O(b^m)`.
  - Bộ nhớ: 
    - `O(b^m * N)`, vì A* lưu toàn bộ các node đã duyệt trong bộ nhớ để tránh lặp lại và đảm bảo tìm lời giải tối ưu.
  - Trong đó:
    - `b`: (branching factor): số lượng trạng thái con trung. Trong 8 Puzzle, tối đa có 4 nước đi (lên, xuống, trái, phải), vậy b = 4.
    - `d` (depth): độ sâu của nút GOAL_STATE trong cây.
    - `N`: số lượng trạng thái trong không gian ban đầu (với 8 Puzzle là 9! = 362,880).

---

### 5. Constrained Search

Giải quyết các bài toán ràng buộc như Sudoku, bản đồ màu, v.v.:

* **Backtracking**
* **Forward Checking**
* **Constraint Propagation**

---

### 6. Reinforcement Learning

Tìm chính sách hành động tối ưu thông qua tương tác với môi trường:

* **Q-Learning**
* **SARSA**
* **Deep Q-Networks (DQN)** – với không gian trạng thái lớn

---

## Liên hệ

Mọi đóng góp hoặc phản hồi vui lòng gửi về nhóm sinh viên thực hiện thông qua GitHub hoặc email cá nhân.

---

*Cảm ơn bạn đã quan tâm đến dự án!*
