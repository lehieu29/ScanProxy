# ProxyScanner

Công cụ quét proxy tự động từ dải IP Việt Nam với phương pháp quét port thân thiện.

## Tính năng

- Quét thăm dò ban đầu với tốc độ thấp để tìm các máy chủ hoạt động
- Quét mục tiêu để tìm các cổng proxy mở
- Xác minh proxy hoạt động và phân loại
- API REST để truy vấn proxy đã tìm thấy
- Triển khai các kỹ thuật quét thân thiện và tránh bị chặn

## Cài đặt

1. Clone repository:
- git clone https://github.com/yourusername/ProxyScanner.git
- cd ProxyScanner
2. Tạo môi trường ảo Python:
- python -m venv venv
- source venv/bin/activate  # Linux/Mac
- venv\Scripts\activate  # Windows
3. Cài đặt các thư viện:
- pip install -r requirements.txt
4. Cài đặt masscan (nếu chưa có):
- **Ubuntu/Debian**
- sudo apt-get install git gcc make libpcap-dev
- git clone https://github.com/robertdavidgraham/masscan
- cd masscan
- make
- sudo make install

## Sử dụng

1. Chạy quét thăm dò: python -m src.main
2. Quét với tham số tùy chỉnh: python -m src.main --range 14.160.0.0/11 --port 8080,3128 --scan-rate 15

