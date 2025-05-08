# **Giải bài toán 8-Puzzle**
## **Giới thiệu**
8-Puzzle Solver là 1 ứng dụng đồ họa cho phép giải quyết bài toán 8-Puzzle bằng nhiều thuật toán tìm kiếm khác nhau. Ứng dụng cung cậps giao diện trực quan để theo dõi quá trình giải quyết, so sánh hiệu suất giữa các thuật toán và xuất kết quả để phân tích.

## **Bài toán 8-Puzzle là gì?**
Bài toán 8-Puzzle là một trò chơi di chuyển các ô số trên bảng 3x3, trong đó có 8 được đánh số từ 1 - 8 và 1 ô trống. Người chơi chỉ có thể di chuyển các ô liền kề với ô trống vào vị trí của ô trống. Mục tiêu là sắp xếp các ô về trạng thái mục tiêu mà người chơi đề ra. 
Trong ứng dụng này, trạng thái đích là:

              | 1 | 2 | 3 |
              | 4 | 5 | 6 |
              | 7 | 8 | 0 |

## **Tính năng**
* **Đa dạng thuật toán:** BFS,DFS,UCS,GBFS,A*,IDA*,Hill ClimBing,Stochastic Hill Climbing, Simulated Anealing, Beam Search, And or search , Belief Enviroment Search, BackTracking
* **Giao diện trực quan:** Theo dõi các trạng thái bắt đầu, hiện tại và đích
* **Điều khiển bước giải:** Chạy từng bước, tự động chạy, quay ngược bước trước
* **Tùy chỉnh trạng thái ban đầu:** Nhập trạng thái 8-Puzzle tùy chọn
* **Thống kê chi tiết:** So sánh thời gian thực thi, số bước thực hiện, chi phí và không gian tìm kiếm giữa các thuật toán
* **Trực quan hóa dữ liệu**: Tạo biểu đồ so sánh hiệu suất giữa các thuật toán
* **Xuất kết quả:** Lưu kết quả và đường đi vào file Excel để tiện cho phân tích sau này
## **Yêu cầu hệ thống**
Môi trường Python
Các thư viện: 
  * Tkinter(GUI)
  * pandas (Xử lý dữ liệu)
  * matplotlib (Trực quan hóa)
  * Các thư viên chuẩn khác : time, copy, collections, heapq
## **Hướng dẫn sử dụng**
### **Cách thiết lập trạng thái ban đầu**
Trạng thái ban đầu (mặc định):

         | 1 | 6 | 2 |
         | 5 | 7 | 4 |
         | 8 | 3 | 0 |
1. Nhập các giá trị có giá từ 0-8 vào lưới "Start State" (0 đại diện cho ô trống hoặc không nhập gì)
2. Nhấn nút "Update Start" để cập nhật lại trạng thái ban đầu
   ![State 8-Puzzle](https://github.com/user-attachments/assets/dacc31eb-68c5-469e-8e19-a11d263a3886)
   
### **Chạy các thuật toán**
1. Chọn thuật toán từ menu dropdown (BFS,DFS,UCS,...) hoặc các thuật toán có hướng xử lý khác ở bên ngoài menu
   ![Select Algorithm](https://github.com/user-attachments/assets/0418a759-fb66-485b-8cce-b552caa83046)
2. Nhấn nút "Run Algorithm" để thực thi thuật toán
3. Theo dõi tiến trình giải quyết trên giao diện "Current State"
### **Điều khiển quá trình giải**
  * **Next Step:** Di chuyển đến bước tiếp theo trong giải pháp
  * **Back Step:** Quay lại bước trước đó
  * **Auto Run:** Tự động thực hiện các bước với tốc độ 1 bước/giây
  * **Stop:** Dừng chế độ tự động chạy
  ![image](https://github.com/user-attachments/assets/f4ab9ac7-f8de-4131-b7b2-3f60f2555438)

### **Phân tích kết quả**
  * **Export:** Lưu đường đi giải quyết vào file Excel
  * **Plot Graph:** Tạo biểu đồ so sánh hiệu suất giữa các thuật toán đã chạy
  ![image](https://github.com/user-attachments/assets/b0d6e37d-2974-4867-9218-a5caba657888)
## **Các thuật toán tìm kiếm**
### **Nhóm thuật toán tìm kiếm không có thông tin (Uninformed Search/Blind Search)**
#### 1. Breadth-First Search (BFS - Tìm kiếm theo chiều rộng):
   * Cách hoạt động: Khám phá tất cả các trạng thái ở cùng một mức (level) trước khi đi sâu hơn. Sử dụng hàng đợi
   * Ưu điểm: Đảm bảo tìm được đường đi ngắn nhất (chi phí mỗi bước là như nhau) nếu bài toán có lời giải
   * Nhược điểm: Tốn nhiều bộ nhớ vì phải lưu tất cả trạng thái ở mỗi mức
#### 2. Depth-First Search (DFS - Tìm kiếm theo chiều sâu)
   * Cách hoạt động: Khám phá một nhánh đến tận cùng trước khi quay lại và thử nhánh khác
   * Ưu điểm: Tốn ít bộ nhớ hơn BFS vì chỉ lưu một nhánh tại 1 thời điểm
   * Nhược điểm: Không đảm bảo tìm được đường đi ngắn nhất, có thể bị mắc kẹt
#### 3. Uniform Cost Search (UCS - Tìm kiếm chi phí đồng nhất)
   * Cách hoạt động: Mở rộng trạng thái có tổng chi phí thấp nhất từ trạng thái ban đầu (dựa vào chi phí đường đi không dựa trên heuritic)
   * Ưu điểm: Đảm bảo tìm được đường đi tối thiểu nếu chi phí mỗi bước là  như nhau
   * Nhược điểm: Tương tự BFS, tốn nhiều bộ nhớ
   * Trong úng dụng này, chi phí của mỗi bước di chuyển là như nhau
### **Nhóm thuật toán tìm kiếm có thông tin**
#### **Đây là nhóm thuật toán sử dụng thông tin heuristic để ưu tiên khám phá các trạng thái có khả năng dẫn đến mục tiêu nhanh hơn**
#### **Đặc điểm:**
  * Sử dụng hàm heuristic (hàm ước lượng khảng cách từ trạng thái hiện tại đến trạng thái mục tiêu) để định hướng tìm kiếm
  * Nhanh hơn các thuật toán không có thông tin nhưng không phải lúc nào cũng đảm bảo tính tối ưu
