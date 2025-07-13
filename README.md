# Mascarade ft. Python

Đồ án môn học Lập trình hướng đối tượng được lấy cảm hứng từ boardgame **Mascarade**, sử dụng thư viện **Kivy** và được xây dựng bằng 100% **Python**!

---

## Yêu cầu hệ thống

- Python **3.11** hoặc mới hơn (được test trên 3.13)
- pip **23.0** hoặc mới hơn
- OS: Windows 10+, Ubuntu/Linux 

---

## Cài đặt môi trường

### Bước 1: Tạo Virtual Environment (Tùy chọn nhưng khuyến nghị)

```bash
# Windows
python -m venv PyMascarade
PyMascarade\Scripts\activate

# Linux/macOS
python3 -m venv PyMascarade
source PyMascarade/bin/activate
```

### Bước 2: Cài đặt thư viện
Chuyển vào thư mục chính của dự án:
``` bash
cd Mascarade-ft-Python
```
Tiến hành cài đặt thư viện:
```bash
# Windows
pip install "kivy[full]" kivy_examples
pip install -r requirements.txt 

# Linux/macOS
sudo apt update
sudo apt install python3-dev python3-pip libgl1-mesa-dev libgles2-mesa-dev \
libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libmtdev-dev

pip install "kivy[full]" kivy_examples
pip install -r requirements.txt
```
### Bước 3: Khởi chạy game
**Bạn đã sẵn sàng rồi!** Hãy chạy lệnh sau (vẫn ở thư mục chính của dự án) để khởi chạy game:
``` bash
python Mascarade.py
```



