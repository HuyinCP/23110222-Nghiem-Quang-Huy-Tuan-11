import pickle

# Tải mô hình từ file
try:
    with open("models.pkl", "rb") as f:
        models = pickle.load(f)

    # Xem các thuật toán trong mô hình (key của từ điển models)
    print("Các thuật toán có trong mô hình:")
    for algo in models:
        print(f"- {algo}")
    
    # Kiểm tra cấu trúc của một mô hình, ví dụ: RandomForestRegressor
    # Lấy mô hình cho BFS (hoặc bất kỳ thuật toán nào bạn đã huấn luyện)
    bfs_model = models.get("BFS")
    
    if bfs_model:
        print("\nCấu trúc của mô hình RandomForest cho BFS:")
        print(bfs_model)

    # Dự đoán với mô hình (ví dụ với một số đặc trưng)
    sample_features = [3, 4, 5]  # Một ví dụ về đặc trưng
    prediction = bfs_model.predict([sample_features])
    print(f"\nDự đoán thời gian cho BFS với đặc trưng {sample_features}: {prediction[0]} giây")

except FileNotFoundError:
    print("Không tìm thấy file 'models.pkl'.")
except Exception as e:
    print(f"Đã xảy ra lỗi: {str(e)}")
