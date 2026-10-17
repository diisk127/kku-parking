import cv2
import pickle
import numpy as np
from shapely.geometry import Polygon
from ultralytics import YOLO

# 1. โหลดโมเดล YOLOv8 และไฟล์พิกัดช่องจอด
model = YOLO('yolov8n.pt') #
video_path = 'assets/video_test.mp4' #
pos_file = 'ai_engine/parking_positions.pkl'

# โหลดพิกัดช่องจอด
with open(pos_file, 'rb') as f:
    pos_list = pickle.load(f)

# จัดกลุ่มพิกัดทีละ 4 จุดเป็น 1 ช่องจอด (Polygon)
slots = [pos_list[i:i + 4] for i in range(0, len(pos_list), 4) if len(pos_list[i:i + 4]) == 4]

cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # วนลูปเล่นวิดีโอซ้ำเมื่อจบ
        continue

    # 2. รัน YOLOv8 ตรวจจับเฉพาะรถยนต์ (Class 2 = car)
    results = model(frame, classes=[2], verbose=False)[0] #

    # ดึง Bounding Box ของรถยนต์ทั้งหมดในเฟรม
    detected_cars = []
    for box in results.boxes.xyxy.cpu().numpy():
        x1, y1, x2, y2 = box
        detected_cars.append(Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)]))

    empty_slots = 0
    total_slots = len(slots)

    # 3. คำนวณการทับซ้อน (Overlap) ระหว่างตำแหน่งรถกับช่องจอด
    for i, slot_pts in enumerate(slots):
        slot_poly = Polygon(slot_pts)
        is_occupied = False

        for car_poly in detected_cars:
            if slot_poly.intersects(car_poly):
                overlap = slot_poly.intersection(car_poly).area / slot_poly.area
                if overlap > 0.3: # ทับซ้อนเกิน 30% ถือว่าไม่ว่าง
                    is_occupied = True
                    break

        # 4. แสดงผลกรอบ (เขียว = ว่าง / แดง = ไม่ว่าง)
        color = (0, 0, 255) if is_occupied else (0, 255, 0) #
        pts_np = np.array(slot_pts, np.int32)
        cv2.polylines(frame, [pts_np], isClosed=True, color=color, thickness=3) #

        if not is_occupied:
            empty_slots += 1

    # 5. แสดงสถิติจำนวนช่องว่างสดๆ บนวิดีโอ
    cv2.putText(frame, f"Available: {empty_slots}/{total_slots}", (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3) #

    cv2.imshow("WhereToPark KKU - AI Detector Demo", frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()