import cv2
import numpy as np
from pyzbar.pyzbar import decode
from fxplc_lib import FXPLC

# Khởi tạo camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Không thể mở camera. Kiểm tra kết nối camera.")

# Kết nối PLC qua cổng COM
try:
    f = FXPLC('COM9')
except Exception as e:
    raise RuntimeError(f"Lỗi kết nối PLC: {e}")

while True:
    # Đọc khung hình từ camera
    success, img = cap.read()
    if not success:
        print("Không thể đọc khung hình từ camera. Kiểm tra lại.")
        break

    # Decode các mã barcode trong hình ảnh
    barcodes = decode(img)
    if not barcodes:
        cv2.imshow('Result', img)
        key = cv2.waitKey(1)
        if key == 27:  # Nhấn ESC để thoát
            break
        continue

    for barcode in barcodes:
        try:
            # Giải mã dữ liệu barcode
            myData = barcode.data.decode('utf-8')
            print("Dữ liệu barcode:", myData)

            # Vẽ đa giác bao quanh barcode
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (255, 0, 255), 5)

            # Hiển thị dữ liệu barcode
            pts2 = barcode.rect
            cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (255, 0, 255), 2)

            # Kiểm tra dữ liệu barcode và điều khiển PLC
            if myData == "K205520114130":
                f.write_bit("M100", True)
                f.write_bit("M101", False)
            elif myData == "K205520114093":
                f.write_bit("M100", False)
                f.write_bit("M101", True)
        except Exception as e:
            print(f"Lỗi xử lý barcode: {e}")

    # Hiển thị khung hình
    cv2.imshow('Result', img)

    # Kiểm tra phím thoát
    key = cv2.waitKey(1)
    if key == 27:  # Nhấn ESC để thoát
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
