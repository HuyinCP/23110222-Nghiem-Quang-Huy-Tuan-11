import cv2
import dlib
import numpy as np
import imutils

# Cài đặt bộ phát hiện khuôn mặt và các điểm đặc trưng trên khuôn mặt
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Hàm tính Eye Aspect Ratio (EAR)
def eye_aspect_ratio(eye):
    # Tính toán tỷ lệ giữa các điểm của mắt
    A = np.linalg.norm(eye[1] - eye[5])  # Từ điểm 1 đến điểm 5
    B = np.linalg.norm(eye[2] - eye[4])  # Từ điểm 2 đến điểm 4
    C = np.linalg.norm(eye[0] - eye[3])  # Từ điểm 0 đến điểm 3
    ear = (A + B) / (2.0 * C)
    return ear

# Tải video hoặc camera trực tiếp
cap = cv2.VideoCapture(0)  # Hoặc "video_file.mp4" cho video

while True:
    # Đọc từng khung hình từ video
    ret, frame = cap.read()
    if not ret:
        break

    frame = imutils.resize(frame, width=640)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Phát hiện khuôn mặt
    faces = detector(gray)

    for face in faces:
        # Phát hiện các điểm đặc trưng trên khuôn mặt
        shape = predictor(gray, face)
        shape = np.array([[p.x, p.y] for p in shape.parts()])

        # Lấy các điểm cho mắt trái và mắt phải
        left_eye = shape[36:42]
        right_eye = shape[42:48]

        # Tính EAR cho hai mắt
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)

        # Tính EAR trung bình
        ear = (left_ear + right_ear) / 2.0

        # Nếu EAR quá thấp, có thể người lái xe đang buồn ngủ
        if ear < 0.2:
            cv2.putText(frame, "Drowsiness Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # Cảnh báo buồn ngủ (có thể thêm âm thanh hoặc ánh sáng nhấp nháy)
            print("Warning: Drowsiness detected!")

    # Hiển thị video
    cv2.imshow("Drowsiness Detection", frame)

    # Dừng lại nếu nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
