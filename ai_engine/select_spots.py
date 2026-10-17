import cv2
import pickle
import os
import numpy as np  # เพิ่ม import numpy เพื่อแก้ NameError

# อ่านเฟรมแรกจากไฟล์วิดีโอ
video_path = 'assets/video_test.mp4' #
cap = cv2.VideoCapture(video_path)
success, frame = cap.read()

pos_list = []
pos_file = 'ai_engine/parking_positions.pkl'

# ถ้าเคยบันทึกไว้แล้ว ให้โหลดพิกัดเดิมมาแสดง
if os.path.exists(pos_file):
    with open(pos_file, 'rb') as f:
        pos_list = pickle.load(f)

def mouse_click(event, x, y, flags, params):
    # คลิกซ้ายเพื่อเพิ่มจุดมุมของช่องจอด (คลิกวน 4 จุดต่อ 1 ช่องจอด)
    if event == cv2.EVENT_LBUTTONDOWN:
        pos_list.append((x, y))
        print(f"เพิ่มพิกัด: ({x}, {y})")
    # คลิกขวาเพื่อลบพิกัดล่าสุด (กรณีคลิกผิด)
    elif event == cv2.EVENT_RBUTTONDOWN:
        if pos_list:
            pos_list.pop()
            print("ลบพิกัดล่าสุดเรียบร้อย")
            
    # บันทึกพิกัดลงไฟล์ pickle ทุกครั้งที่คลิก
    with open(pos_file, 'wb') as f:
        pickle.dump(pos_list, f)

if success:
    print("--- วิธีใช้งาน ---")
    print("1. คลิกซ้าย 4 จุดวนรอบช่องจอด เพื่อสร้าง 1 ช่องจอด")
    print("2. คลิกขวา เพื่อลบจุดล่าสุด")
    print("3. กดปุ่ม 'q' บนคีย์บอร์ดเพื่อบันทึกและปิดหน้าต่าง\n")

    while True:
        img_copy = frame.copy()
        # วาดจุดและเส้นเชื่อมช่องจอด
        for i, pos in enumerate(pos_list):
            cv2.circle(img_copy, pos, 5, (0, 255, 0), -1)
            # แสดงเส้นเชื่อมทุกๆ 4 จุด
            if (i + 1) % 4 == 0:
                pts = [pos_list[i-3], pos_list[i-2], pos_list[i-1], pos_list[i]]
                cv2.polylines(img_copy, [np.array(pts)], True, (255, 0, 0), 2)

        cv2.imshow("Select Parking Spots", img_copy)
        cv2.setMouseCallback("Select Parking Spots", mouse_click)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
else:
    print("ไม่พบไฟล์วิดีโอ กรุณาตรวจสอบว่ามีไฟล์ assets/video_test.mp4 หรือไม่")