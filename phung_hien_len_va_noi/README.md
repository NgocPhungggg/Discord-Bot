Phụng Hiện Lên Và Nói là một bot voice dành cho Discord, giúp chuyển văn bản thành giọng đọc tiếng Việt do Ngọc Phụng xây dựng và phát triển.

---

## 1. Cài đặt thư viện cần thiết

### 1.1 Cài đặt Python
Tải Python 3.11 tại:
https://www.python.org/downloads/release/python-3119/

Kiểm tra: python --version

### 1.2 Cài đặt thư viện Python
- pip install discord.py
- pip install gTTS
- pip install PyNaCl

### 1.3 Cài đặt ffmpeg

Tải FFmpeg tại: https://www.gyan.dev/ffmpeg/builds/

Khuyến nghị tải: ffmpeg-release-essentials.zip

Sau đó khai báo biến môi trường trong phần "Edit the system enviroment variables" 

Restart máy và mở cmd lên, gõ lệnh "ffmpeg -version" để kiểm tra đã cài đặt chưa


## 2. Hướng dẫn sử dụng

!p-join → gọi bot vào voice channel của bạn

!pt <nội dung> → lệnh để bot nói

s-- Ví dụ
!pt xin chào tôi là ngọc phụng


