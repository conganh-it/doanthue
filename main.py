import cv2  # Thư viện OpenCV để xử lý hình ảnh và video
import numpy as np  # Thư viện tính toán và xử lý mảng
from pyzbar.pyzbar import decode  # Hàm decode để giải mã barcode và QR code
from fxplc_lib import FXPLC  # Thư viện điều khiển PLC qua giao thức FXPLC

# Khởi tạo camera
cap = cv2.VideoCapture(0)  # Mở camera mặc định (ID = 0)
if not cap.isOpened():  # Kiểm tra xem camera có mở thành công không
    raise RuntimeError("Không thể mở camera. Kiểm tra kết nối camera.")  # Nếu không, báo lỗi và dừng chương trình

# Kết nối PLC qua cổng COM
try:
    f = FXPLC('COM9')  # Kết nối với PLC qua cổng COM9
except Exception as e:  # Nếu có lỗi trong quá trình kết nối
    raise RuntimeError(f"Lỗi kết nối PLC: {e}")  # In thông báo lỗi chi tiết và dừng chương trình

while True:  # Bắt đầu vòng lặp chính để xử lý từng khung hình từ camera
    # Đọc khung hình từ camera
    success, img = cap.read()  # Lấy khung hình từ camera; trả về success (True/False) và hình ảnh (img)
    if not success:  # Nếu không đọc được khung hình (success == False)
        print("Không thể đọc khung hình từ camera. Kiểm tra lại.")  # Thông báo lỗi
        break  # Thoát vòng lặp chính

    # Decode các mã barcode trong hình ảnh
    barcodes = decode(img)  # Giải mã tất cả các barcode và QR code có trong khung hình
    if not barcodes:  # Nếu không tìm thấy barcode nào
        cv2.imshow('Result', img)  # Hiển thị khung hình hiện tại (không có barcode)
        key = cv2.waitKey(1)  # Chờ 1ms để kiểm tra phím nhấn từ người dùng
        if key == 27:  # Nếu nhấn phím ESC (mã ASCII là 27), thoát chương trình
            break  # Thoát vòng lặp chính
        continue  # Bỏ qua phần còn lại của vòng lặp và tiếp tục khung hình tiếp theo

    for barcode in barcodes:  # Lặp qua từng barcode được tìm thấy trong khung hình
        try:
            # Giải mã dữ liệu barcode
            myData = barcode.data.decode('utf-8')  # Chuyển dữ liệu barcode từ byte sang chuỗi UTF-8
            print("Dữ liệu barcode:", myData)  # In dữ liệu barcode ra màn hình

            # Vẽ đa giác bao quanh barcode
            pts = np.array([barcode.polygon], np.int32)  # Lấy các điểm (polygon) tạo nên barcode
            pts = pts.reshape((-1, 1, 2))  # Định hình lại dữ liệu để phù hợp với hàm vẽ của OpenCV
            cv2.polylines(img, [pts], True, (255, 0, 255), 5)  # Vẽ đường đa giác trên ảnh (màu hồng, độ dày 5px)

            # Hiển thị dữ liệu barcode trên khung hình
            pts2 = barcode.rect  # Lấy tọa độ hình chữ nhật bao quanh barcode
            cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (255, 0, 255), 2)  # Hiển thị dữ liệu barcode trên ảnh (màu hồng, font kích thước 0.9)

            # Kiểm tra dữ liệu barcode và điều khiển PLC
            if myData == "K205520114130":  # Nếu dữ liệu barcode khớp với mã này
                f.write_bit("M100", True)  # Ghi tín hiệu M100 = True (bật)
                f.write_bit("M101", False)  # Ghi tín hiệu M101 = False (tắt)
            elif myData == "K205520114093":  # Nếu dữ liệu barcode khớp với mã này
                f.write_bit("M100", False)  # Ghi tín hiệu M100 = False (tắt)
                f.write_bit("M101", True)  # Ghi tín hiệu M101 = True (bật)
        except Exception as e:  # Nếu xảy ra lỗi trong quá trình xử lý barcode
            print(f"Lỗi xử lý barcode: {e}")  # Thông báo lỗi chi tiết

    # Hiển thị khung hình lên màn hình
    cv2.imshow('Result', img)  # Hiển thị khung hình (có barcode hoặc không)

    # Kiểm tra phím thoát
    key = cv2.waitKey(1)  # Chờ 1ms và kiểm tra phím nhấn
    if key == 27:  # Nếu nhấn ESC (mã ASCII là 27), thoát chương trình
        break  # Thoát vòng lặp chính

# Giải phóng tài nguyên
cap.release()  # Giải phóng camera
cv2.destroyAllWindows()  # Đóng tất cả các cửa sổ OpenCV
