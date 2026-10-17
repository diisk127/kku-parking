
# KKU Parking Demo (Web App & AI Spot Detection)

โปรเจกต์ระบบค้นหาและแจ้งสถานะที่จอดรถภายในมหาวิทยาลัยขอนแก่นแบบ Real-time

## วิธีตั้งค่าเครื่องสำหรับฝั่ง Python (AI)

1. สร้าง Virtual Environment: `python3 -m venv venv`
2. เปิดใช้งาน: `source venv/bin/activate` (Mac) หรือ `venv\Scripts\activate` (Windows)
3. ติดตั้ง Dependencies: `pip install -r requirements.txt`
4. วางไฟล์ `firebase_key.json` และ `video_test.mp4` ไว้ในเครื่องตัวเอง

## วิธีรัน AI Detector

1. มาร์กพิกัดช่องจอด: `python ai_engine/select_spots.py`
2. รันระบบตรวจจับ: `python ai_engine/main_detector.py`
