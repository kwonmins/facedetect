import cv2
import numpy as np
from keras.models import load_model

# ✅ 새 모델 경로로 변경
MODEL_PATH = "keras_model.h5"
LABELS_PATH = "labels.txt"

# 모델 로드
model = load_model(MODEL_PATH, compile=False)

# 라벨 불러오기
class_names = open(LABELS_PATH, "r").readlines()
class_names = [label.strip() for label in class_names]  # 개행 문자 제거

# 웹캠 실행
camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    if not ret:
        break

    # 얼굴 검출
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        face = cv2.resize(face, (224, 224))  # 모델 입력 크기 맞춤
        face = np.asarray(face, dtype=np.float32).reshape(1, 224, 224, 3)
        face = (face / 127.5) - 1  # 정규화

        # 예측 수행
        prediction = model.predict(face)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index] * 100

        # 결과 출력
        print(f"Class: {class_name}, Confidence: {confidence_score:.2f}%")

        # 화면 표시
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, f"{class_name} ({confidence_score:.2f}%)", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    cv2.imshow("Face Shape Analysis", frame)

    # ESC 키로 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

camera.release()
cv2.destroyAllWindows()
