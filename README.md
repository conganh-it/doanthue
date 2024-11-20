# FXPLC Library

## Giới thiệu
`FXPLC` là một thư viện Python hỗ trợ giao tiếp với các thiết bị FXPLC qua giao thức nối tiếp (serial). Thư viện được thiết kế để dễ dàng sử dụng trong các dự án IoT và tự động hóa.

---

## Cấu trúc thư viện

Thư viện được tổ chức với cấu trúc như sau:

![img_2.png](img%2Fimg_2.png)
 
chuẩn bị file: [__init__.py](fxplc_lib%2F__init__.py), [fxplc.py](fxplc_lib%2Ffxplc.py),[setup.py](setup.py)
cách thực hiện :
- mở cmd tại nơi chứa file setup.py 
![img_3.png](img_3.png)
chạy dòng : python setup.py sdist ( để đóng gói thư viện)
![img_4.png](img_4.png)
- cài đặt thư viện vào môi trường ảo
+ mở terminal trong pycharm
+ chạy lệnh pip install/path/to/your/fxplc_lib/fxplc-1.0.0.tar.gz
  (lưu ý: path/to/your/fxplc_lib/ là link lưu thư mục/file)
+ sử dụng bình thường
from fxplc_lib.fxplc import FXPLC
plc = FXPLC(port='COM1')
