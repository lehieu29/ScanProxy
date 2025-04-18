# src/ip_range_manager.py
import os
import ipaddress
import random
import logging
from src.config import DATA_DIR

logger = logging.getLogger("ip_manager")


class IPRangeManager:
    """Quản lý và xử lý các dải IP Việt Nam"""

    def __init__(self, ip_ranges_file=None):
        """
        Khởi tạo IP Manager

        Args:
            ip_ranges_file: Đường dẫn đến file chứa danh sách dải IP Việt Nam
        """
        self.ip_ranges = []

        # File mặc định
        if not ip_ranges_file:
            ip_ranges_file = os.path.join(DATA_DIR, "vietnam_ip_ranges.txt")

        # Đọc danh sách dải IP nếu file tồn tại
        if os.path.exists(ip_ranges_file):
            self.load_ip_ranges(ip_ranges_file)
        else:
            # Sử dụng danh sách dải IP mặc định nếu không có file
            self.ip_ranges = [
                "14.160.0.0/11",  # VNPT
                "14.224.0.0/11",  # Viettel
                "27.64.0.0/12",  # Viettel
                "42.112.0.0/13",  # VNPT
                "45.121.152.0/22",  # FPT
                "113.160.0.0/11",  # VNPT
                "123.16.0.0/12",  # Viettel
                "171.224.0.0/11",  # VNPT
                "203.162.0.0/16",  # FPT
                "203.210.128.0/17"  # CMC
            ]
            logger.warning(f"File dải IP không tồn tại: {ip_ranges_file}, sử dụng danh sách mặc định")

    def load_ip_ranges(self, file_path):
        """
        Đọc danh sách dải IP từ file

        Args:
            file_path: Đường dẫn đến file chứa danh sách dải IP
        """
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        self.ip_ranges.append(line)
            logger.info(f"Đã đọc {len(self.ip_ranges)} dải IP từ file: {file_path}")
        except Exception as e:
            logger.error(f"Lỗi khi đọc file dải IP: {e}")

    def save_ip_ranges(self, file_path=None):
        """
        Lưu danh sách dải IP vào file

        Args:
            file_path: Đường dẫn đến file để lưu danh sách dải IP
        """
        if not file_path:
            file_path = os.path.join(DATA_DIR, "vietnam_ip_ranges.txt")

        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                for ip_range in self.ip_ranges:
                    f.write(f"{ip_range}\n")
            logger.info(f"Đã lưu {len(self.ip_ranges)} dải IP vào file: {file_path}")
        except Exception as e:
            logger.error(f"Lỗi khi lưu file dải IP: {e}")

    def get_random_ranges(self, count=5):
        """
        Lấy ngẫu nhiên một số dải IP

        Args:
            count: Số lượng dải IP cần lấy

        Returns:
            list: Danh sách dải IP được chọn ngẫu nhiên
        """
        if not self.ip_ranges:
            return []

        return random.sample(self.ip_ranges, min(count, len(self.ip_ranges)))

    def get_ranges_by_priority(self, high_priority_count=2, medium_priority_count=3):
        """
        Lấy dải IP theo mức độ ưu tiên

        Args:
            high_priority_count: Số lượng dải IP ưu tiên cao
            medium_priority_count: Số lượng dải IP ưu tiên trung bình

        Returns:
            dict: Dictionary các dải IP theo mức độ ưu tiên
        """
        # Danh sách dải IP ưu tiên (dải lớn, VNPT, Viettel)
        high_priority = [
            r for r in self.ip_ranges if
            ("14.160.0.0/11" in r or "14.224.0.0/11" in r or
             "27.64.0.0/12" in r or "113.160.0.0/11" in r or
             "123.16.0.0/12" in r or "171.224.0.0/11" in r)
        ]

        # Danh sách dải IP ưu tiên trung bình (FPT, CMC, dải nhỏ hơn)
        medium_priority = [
            r for r in self.ip_ranges if r not in high_priority
        ]

        # Lấy ngẫu nhiên theo số lượng yêu cầu
        selected_high = random.sample(high_priority, min(high_priority_count, len(high_priority)))
        selected_medium = random.sample(medium_priority, min(medium_priority_count, len(medium_priority)))

        return {
            "high": selected_high,
            "medium": selected_medium
        }

    def estimate_ip_count(self, ip_range):
        """
        Ước tính số lượng IP trong một dải

        Args:
            ip_range: Dải IP (CIDR hoặc dạng x.x.x.x-y.y.y.y)

        Returns:
            int: Ước tính số lượng IP
        """
        try:
            if "/" in ip_range:  # CIDR format
                network = ipaddress.IPv4Network(ip_range)
                return network.num_addresses
            elif "-" in ip_range:  # Range format
                start_ip, end_ip = ip_range.split("-")
                start_int = int(ipaddress.IPv4Address(start_ip.strip()))
                end_int = int(ipaddress.IPv4Address(end_ip.strip()))
                return end_int - start_int + 1
            else:
                return 1  # Single IP
        except Exception as e:
            logger.error(f"Lỗi khi ước tính số lượng IP cho dải {ip_range}: {e}")
            return 0