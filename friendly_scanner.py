# src/friendly_scanner.py
import asyncio
import random
import time
import ipaddress
import logging
import subprocess
import json
import os
from datetime import datetime

from src.config import (
    SCAN_RATE, JITTER, BATCH_SIZE, BATCH_DELAY,
    USER_AGENTS, PORT_PRIORITY, DATA_DIR
)

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logs/scanner.log'
)
logger = logging.getLogger("friendly_scanner")


class FriendlyScanner:
    """Scanner thân thiện với các cơ chế tránh phát hiện"""

    def __init__(self,
                 scan_type="discovery",
                 custom_rate=None,
                 max_concurrent=5):
        """
        Khởi tạo scanner thân thiện

        Args:
            scan_type: Loại quét ("discovery", "targeted")
            custom_rate: Tốc độ quét tùy chỉnh (packets/giây)
            max_concurrent: Số lượng kết nối đồng thời tối đa
        """
        # Thiết lập tốc độ quét dựa trên loại quét
        self.scan_type = scan_type
        self.scan_rate = custom_rate if custom_rate else SCAN_RATE[scan_type]

        # Điều chỉnh tốc độ quét dựa trên thời gian trong ngày
        self._adjust_rate_for_time()

        # Khởi tạo các tham số khác
        self.max_concurrent = max_concurrent
        self.jitter_min = JITTER["min"]
        self.jitter_max = JITTER["max"]
        self.batch_size = BATCH_SIZE
        self.batch_delay_min = BATCH_DELAY["min"]
        self.batch_delay_max = BATCH_DELAY["max"]

        # Thời gian quét gần nhất (để kiểm soát tốc độ)
        self.last_scan_time = 0

        logger.info(f"Scanner khởi tạo: loại={scan_type}, tốc độ={self.scan_rate} packets/giây")

    def _adjust_rate_for_time(self):
        """Điều chỉnh tốc độ quét dựa trên thời gian trong ngày"""
        hour = datetime.now().hour

        # Giờ cao điểm: 8:00 - 22:00
        if 8 <= hour < 22:
            self.scan_rate *= SCAN_RATE["peak_hour_factor"]
            logger.info(f"Giờ cao điểm: Giảm tốc độ quét xuống {self.scan_rate} packets/giây")

    def is_off_peak_hour(self):
        """Kiểm tra xem có phải giờ thấp điểm không"""
        hour = datetime.now().hour
        # Giờ thấp điểm: 22:00 - 06:00
        return 22 <= hour or hour < 6

    async def scan_ip_port(self, ip, port):
        """
        Quét một IP và port cụ thể với kiểm soát tốc độ

        Args:
            ip: Địa chỉ IP cần quét
            port: Cổng cần quét

        Returns:
            bool: True nếu cổng mở, False nếu đóng
        """
        # Đảm bảo giới hạn tốc độ bằng cách kiểm soát thời gian giữa các lần quét
        current_time = time.time()
        time_since_last = current_time - self.last_scan_time
        min_interval = 1.0 / self.scan_rate

        if time_since_last < min_interval:
            await asyncio.sleep(min_interval - time_since_last)

        self.last_scan_time = time.time()

        # Thêm độ trễ ngẫu nhiên (jitter) để tránh mẫu quét dễ nhận biết
        jitter = random.uniform(self.jitter_min, self.jitter_max)
        await asyncio.sleep(jitter)

        try:
            # Thực hiện kết nối TCP
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port),
                timeout=2
            )
            writer.close()
            await writer.wait_closed()
            logger.debug(f"Cổng mở: {ip}:{port}")
            return True
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            logger.debug(f"Cổng đóng hoặc không phản hồi: {ip}:{port}")
            return False

    async def scan_batch(self, ip_list, ports):
        """
        Quét một batch các IP và port

        Args:
            ip_list: Danh sách các IP cần quét
            ports: Danh sách các cổng cần quét

        Returns:
            list: Danh sách kết quả [(ip, port, is_open), ...]
        """
        tasks = []
        results = []

        logger.info(f"Bắt đầu quét batch: {len(ip_list)} IP, {len(ports)} cổng")

        # Tạo tasks cho tất cả các cặp (ip, port)
        for ip in ip_list[:self.batch_size]:  # Giới hạn kích thước batch
            for port in ports:
                tasks.append(self.scan_ip_port(ip, port))

        # Quét batch và thu thập kết quả
        batch_results = await asyncio.gather(*tasks)

        # Kết hợp kết quả với thông tin IP/port
        result_idx = 0
        for ip in ip_list[:self.batch_size]:
            for port in ports:
                if batch_results[result_idx]:
                    results.append((ip, port, True))
                result_idx += 1

        # Nghỉ giữa các batch với thời gian ngẫu nhiên
        batch_delay = random.uniform(self.batch_delay_min, self.batch_delay_max)
        logger.info(f"Hoàn thành batch, nghỉ {batch_delay:.2f} giây")
        await asyncio.sleep(batch_delay)

        return results

    def run_masscan(self, ip_range, ports, output_file=None):
        """
        Chạy masscan với các tùy chọn thân thiện

        Args:
            ip_range: Dải IP cần quét (dạng CIDR hoặc x.x.x.x-y.y.y.y)
            ports: Danh sách các cổng cần quét
            output_file: Tên file output (mặc định: random name)

        Returns:
            list: Danh sách các IP và cổng mở phát hiện được
        """
        if not output_file:
            output_file = os.path.join(DATA_DIR, f"scan_{random.randint(1000, 9999)}.json")

        # Chuyển danh sách port thành chuỗi
        ports_str = ",".join(map(str, ports))

        # Tạo lệnh masscan với các tùy chọn thân thiện
        cmd = [
            "masscan",
            ip_range,
            "-p", ports_str,
            "--rate", str(self.scan_rate),
            "--randomize-hosts",  # Trộn ngẫu nhiên các địa chỉ host
            "--source-port", str(random.randint(30000, 65000)),  # Cổng nguồn ngẫu nhiên
            "--ttl", str(random.randint(48, 255)),  # TTL ngẫu nhiên
            "-oJ", output_file  # Output dạng JSON
        ]

        logger.info(f"Chạy lệnh: {' '.join(cmd)}")

        try:
            # Chạy lệnh masscan
            subprocess.run(cmd, check=True, timeout=600)  # Timeout 10 phút

            # Đọc kết quả
            with open(output_file, "r") as f:
                results = json.load(f)

            logger.info(f"Hoàn thành quét, tìm thấy {len(results)} kết quả")
            return results
        except subprocess.SubprocessError as e:
            logger.error(f"Lỗi khi chạy masscan: {e}")
            return []
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"Lỗi khi đọc file kết quả: {e}")
            return []

    def split_ip_range(self, ip_range):
        """
        Chia dải IP thành các batch nhỏ

        Args:
            ip_range: Dải IP dạng CIDR (x.x.x.x/y) hoặc dải (x.x.x.x-y.y.y.y)

        Returns:
            list: Danh sách các dải IP nhỏ
        """
        batches = []

        if "-" in ip_range:
            # Dải IP dạng x.x.x.x-y.y.y.y
            start_ip, end_ip = ip_range.split("-")
            start_int = int(ipaddress.IPv4Address(start_ip.strip()))
            end_int = int(ipaddress.IPv4Address(end_ip.strip()))

            # Tính số lượng IP
            ip_count = end_int - start_int + 1

            # Chia thành các batch
            batch_size = min(ip_count, self.batch_size * 5)  # Batch cho masscan lớn hơn
            for i in range(start_int, end_int + 1, batch_size):
                batch_end = min(i + batch_size - 1, end_int)
                batch_start_ip = str(ipaddress.IPv4Address(i))
                batch_end_ip = str(ipaddress.IPv4Address(batch_end))
                batches.append(f"{batch_start_ip}-{batch_end_ip}")

        elif "/" in ip_range:
            # Dải IP dạng CIDR x.x.x.x/y
            network = ipaddress.IPv4Network(ip_range)
            ip_count = network.num_addresses

            if ip_count <= self.batch_size * 5:
                batches.append(ip_range)
            else:
                # Chia thành các subnet nhỏ hơn
                new_prefix = network.prefixlen
                while True:
                    new_prefix += 1
                    subnet_size = 2 ** (32 - new_prefix)
                    if subnet_size <= self.batch_size * 5 or new_prefix >= 28:
                        break

                for subnet in network.subnets(new_prefix=new_prefix):
                    batches.append(str(subnet))

        # Xáo trộn các batch
        random.shuffle(batches)
        logger.info(f"Chia dải IP {ip_range} thành {len(batches)} batch")
        return batches