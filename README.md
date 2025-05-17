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
* **Phức tạp**:

  * Thời gian: `O(b^d)`
  * Bộ nhớ: `O(b^d)`
     * b (branching factor): số lượng trạng thái con trung. Trong 8 Puzzle, tối đa có 4 nước đi (lên, xuống, trái, phải), vậy b = 4.
     * d (depth): độ sâu của nút GOAL_STATE trong cây.

#### ▸ Depth-First Search (DFS)

* **Chiến lược**: Duyệt **sâu trước**, mở rộng hết một nhánh rồi quay lại.
* **Cấu trúc dữ liệu**: Stack.
* **Ưu điểm**: Tốn ít bộ nhớ.
* **Nhược điểm**: Không đảm bảo tìm lời giải ngắn nhất, dễ đi vào vòng lặp nếu không kiểm tra trạng thái.
* **Phức tạp**:

  * Thời gian: `O(b^m)`
  * Bộ nhớ: `O(bm)`
      * `b` (branching factor): số lượng trạng thái con trung. Trong 8 Puzzle, tối đa có 4 nước đi (lên, xuống, trái, phải), vậy b = 4.
      * `m` (maximum depth): độ sâu lớn nhất mà DFS có thể đi tới trong cây.

#### ▸ Uniform Cost Search (UCS)

* **Chiến lược**: Mở rộng node có **tổng chi phí thấp nhất** từ gốc đến hiện tại.
* **Cấu trúc dữ liệu**: Priority Queue.
* **Ưu điểm**: Tìm lời giải **tối ưu** nếu chi phí luôn dương.
* **Nhược điểm**: Tốn bộ nhớ và thời gian như BFS trong không gian lớn.
* **Phức tạp**:

  * Thời gian/Bộ nhớ: `O(b^{1 + C*/ε})`
  * Với `C*` là chi phí tối ưu và `ε` là bước chi phí nhỏ nhất.
      * `b` (branching factor): số lượng trạng thái con trung. Trong 8 Puzzle, tối đa có 4 nước đi (lên, xuống, trái, phải), vậy b = 4.
      * `C^*`: chi phí tối ưu để tìm lời giải
      * `ε`: là bước chi phí nhỏ nhất.

#### ▸ Iterative Deepening Search (IDS)

* **Chiến lược**: Kết hợp DFS và BFS bằng cách lặp lại DFS với giới hạn độ sâu tăng dần.
* **Ưu điểm**: Tìm được lời giải **ngắn nhất** như BFS nhưng **tốn ít bộ nhớ** như DFS.
* **Nhược điểm**: Tốn thời gian do lặp lại các node.
* **Phức tạp**:

  * Thời gian: `O(b^d)`
  * Bộ nhớ: `O(bd)`
       * `b` (branching factor): số lượng trạng thái con trung. Trong 8 Puzzle, tối đa có 4 nước đi (lên, xuống, trái, phải), vậy `b` = 4.
       * `d` (depth): độ sâu của nút GOAL_STATE trong cây.

---

### 2. Informed Search

Các thuật toán sử dụng heuristic để ước lượng chi phí từ trạng thái hiện tại đến đích, ưu tiên mở rộng các trạng thái có khả năng dẫn đến lời giải nhanh hơn.
Trong bài toán **8 Puzzle**, các thuật toán Informed Search như:

- Greedy Best-First Search  
- A* Search  
- Iterative Deepening A* (IDA*)  

đều sử dụng chung một hàm heuristic phổ biến là **khoảng cách Manhattan**.

#### Khoảng cách Manhattan là gì?

- Khoảng cách Manhattan giữa một ô trong trạng thái hiện tại và vị trí đúng của nó là tổng số bước đi theo chiều ngang và chiều dọc cần thiết để di chuyển ô đó về đúng vị trí.
- Cụ thể, với mỗi ô có tọa độ hiện tại \((x_1, y_1)\) và tọa độ đích \((x_2, y_2)\), khoảng cách Manhattan được tính bằng:

\[
h = |x_1 - x_2| + |y_1 - y_2|
\]

- Hàm heuristic tổng là tổng khoảng cách Manhattan của tất cả các ô trên bảng (trừ ô trống).
#### ▸ Greedy Best-First Search (GBFS)

* **Chiến lược**: Luôn mở rộng node có giá trị heuristic `h(n)` nhỏ nhất — tức là node được ước lượng gần đích nhất.
* **Cấu trúc dữ liệu**: Priority Queue (hàng đợi ưu tiên), sắp xếp theo giá trị heuristic.
* **Ưu điểm**:  
  - Tìm kiếm nhanh, tận dụng thông tin heuristic để đi thẳng đến đích.  
  - Tiết kiệm bộ nhớ hơn so với các thuật toán tìm kiếm không thông tin như BFS hay UCS nếu heuristic tốt.
* **Nhược điểm**:  
  - Không đảm bảo tìm ra lời giải tối ưu (ngắn nhất).  
  - Có thể bị mắc kẹt ở các điểm local minima hoặc đi sai hướng nếu heuristic không chính xác.
* **Phức tạp**:  
  - Thời gian và bộ nhớ trong trường hợp xấu nhất: \(O(b^m)\), trong đó:  
    - \(b\): branching factor (số nhánh trung bình mỗi node).  
    - \(m\): độ sâu lớn nhất của cây tìm kiếm.

* **Ứng dụng trong bài toán 8 Puzzle**:  
  - Sử dụng các heuristic phổ biến như **tổng khoảng cách Manhattan** hoặc **số ô sai vị trí**.  
  - Thuật toán luôn chọn trạng thái kế tiếp có giá trị heuristic nhỏ nhất để mở rộng, giúp tìm đường đi đến trạng thái đích nhanh hơn.

---

#### ▸ A* Search

* **Chiến lược**: Kết hợp chi phí thực tế đã đi từ gốc \(g(n)\) và ước lượng heuristic còn lại \(h(n)\) để đánh giá node theo \(f(n) = g(n) + h(n)\).
* **Ưu điểm**:  
  - Tìm được lời giải tối ưu nếu heuristic là **đúng và không vượt quá thực tế** (admissible).  
  - Hiệu quả hơn so với tìm kiếm không thông tin.
* **Nhược điểm**: Tốn bộ nhớ lớn khi không gian tìm kiếm rộng.
* **Phức tạp**: Tương tự GBFS trong trường hợp xấu nhất, nhưng thực tế thường nhanh hơn.

---

#### ▸ Iterative Deepening A* (IDA*)

* **Chiến lược**: Kết hợp ý tưởng của IDS và A* bằng cách sử dụng iterative deepening dựa trên ngưỡng \(f\)-cost tăng dần.
* **Ưu điểm**:  
  - Giảm bộ nhớ sử dụng so với A*.  
  - Vẫn giữ được tính tối ưu của A*.
* **Nhược điểm**: Có thể lặp lại mở rộng node nhiều lần, gây tốn thời gian.
* **Phức tạp**: Tương tự A* nhưng bộ nhớ thấp hơn.

---

### 3. Local Search

Tìm kiếm theo hướng cải thiện trạng thái hiện tại mà không cần lưu toàn bộ đường đi:

* Hill Climbing (Simple, Steepest, Stochastic)
* Simulated Annealing
* Beam Search
* AND-OR Graph Search
* Belief Search

---

### 4. Complex Spaces Search

Các kỹ thuật dành cho không gian tìm kiếm rất lớn hoặc có cấu trúc phức tạp. Có thể áp dụng tree decomposition, domain-specific search, hoặc phân cụm trạng thái.

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

ghi rõ cách áp dụng trong bài toán 8 puzzle
