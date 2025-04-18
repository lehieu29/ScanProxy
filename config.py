# src/config.py
import os
from dotenv import load_dotenv

# Tải các biến môi trường từ file .env (nếu có)
load_dotenv()

# Thông tin chung
PROJECT_NAME = "ProxyScanner"
VERSION = "0.1.0"

# Đường dẫn đến thư mục dữ liệu
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")

# Cấu hình quét thân thiện
SCAN_RATE = {
    "discovery": 15,   # packets/giây cho quét thăm dò
    "targeted": 30,    # packets/giây cho quét mục tiêu
    "peak_hour_factor": 0.5  # Giảm 50% tốc độ quét vào giờ cao điểm
}

# Độ trễ giữa các quét (giây)
JITTER = {
    "min": 0.1,
    "max": 2.0
}

# Thời gian nghỉ giữa các batch (giây)
BATCH_DELAY = {
    "min": 60,
    "max": 300
}

# Kích thước batch
BATCH_SIZE = 20

# Số lượng kết nối đồng thời tối đa khi xác minh proxy
MAX_CONCURRENT_VERIFICATIONS = 5

# Cổng proxy phổ biến cần quét
PROXY_PORTS = {
    "http": [80, 8080, 3128, 8000, 8888, 8118, 6588, 8090, 8123],
    "https": [443, 8443, 4443, 3129, 8444],
    "socks4": [1080, 4145, 1081, 1090, 3629],
    "socks5": [1080, 9050, 8880, 1081, 5678]
}

# Ưu tiên quét
PORT_PRIORITY = {
    "high": [8080, 3128],      # Quét trong giai đoạn thăm dò
    "medium": [80, 8000, 443], # Quét trong giai đoạn đầu mục tiêu
    "low": list(set(sum(PROXY_PORTS.values(), [])))  # Tất cả cổng khác
}

# Danh sách User-Agent
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
    # Thêm nhiều User-Agent khác...
]

# Cấu hình API
API_HOST = "0.0.0.0"
API_PORT = 5000