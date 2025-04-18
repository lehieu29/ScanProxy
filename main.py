# src/main.py
import asyncio
import logging
import argparse
import os
import time
from datetime import datetime

from src.config import PROXY_PORTS, PORT_PRIORITY, LOG_DIR
from src.friendly_scanner import FriendlyScanner
from src.ip_range_manager import IPRangeManager

# Thiết lập logging
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, f"proxy_scanner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("main")


async def discovery_scan(ip_ranges, scanner, ip_manager):
    """
    Thực hiện quét thăm dò ban đầu

    Args:
        ip_ranges: Danh sách các dải IP cần quét
        scanner: Đối tượng FriendlyScanner
        ip_manager: Đối tượng IPRangeManager

    Returns:
        list: Danh sách các IP và cổng mở phát hiện được
    """
    all_results = []
    discovery_ports = PORT_PRIORITY["high"]

    logger.info(f"Bắt đầu quét thăm dò trên {len(ip_ranges)} dải IP với {len(discovery_ports)} cổng")

    for ip_range in ip_ranges:
        # Chia nhỏ dải IP và xáo trộn
        batches = scanner.split_ip_range(ip_range)

        # Chỉ lấy một số batch để quét nhanh
        sample_size = min(5, len(batches))
        selected_batches = batches[:sample_size]

        logger.info(f"Quét thăm dò {sample_size}/{len(batches)} batch từ dải {ip_range}")

        for batch in selected_batches:
            # Sử dụng masscan cho quét thăm dò nhanh
            results = scanner.run_masscan(batch, discovery_ports)
            all_results.extend(results)

            # Nghỉ giữa các batch
            sleep_time = 30  # 30 giây
            logger.info(f"Nghỉ {sleep_time}s trước batch tiếp theo")
            await asyncio.sleep(sleep_time)

    logger.info(f"Hoàn thành quét thăm dò, tìm thấy {len(all_results)} kết quả")
    return all_results


async def main():
    """Hàm chính của chương trình"""
    # Xử lý tham số dòng lệnh
    parser = argparse.ArgumentParser(description='ProxyScanner - Công cụ quét proxy thân thiện')
    parser.add_argument('-r', '--range', help='Dải IP cụ thể để quét (ưu tiên cao nhất)')
    parser.add_argument('-p', '--port', help='Cổng cụ thể để quét (phân tách bằng dấu phẩy)')
    parser.add_argument('-s', '--scan-rate', type=int, default=20, help='Tốc độ quét (packets/giây)')
    args = parser.parse_args()

    logger.info(f"Khởi động ProxyScanner với tham số: {args}")

    # Khởi tạo IP Manager
    ip_manager = IPRangeManager()

    # Khởi tạo Scanner thân thiện
    scanner = FriendlyScanner(scan_type="discovery", custom_rate=args.scan_rate)

    # Xử lý dải IP
    if args.range:
        ip_ranges = [args.range]
    else:
        # Lấy dải IP ưu tiên
        ranges_by_priority = ip_manager.get_ranges_by_priority(high_priority_count=2, medium_priority_count=3)
        ip_ranges = ranges_by_priority["high"] + ranges_by_priority["medium"]

    logger.info(f"Dải IP sẽ quét: {ip_ranges}")

    # Xử lý cổng
    if args.port:
        ports = [int(p.strip()) for p in args.port.split(',')]
    else:
        # Sử dụng cổng ưu tiên cao cho quét thăm dò ban đầu
        ports = PORT_PRIORITY["high"]

    logger.info(f"Cổng sẽ quét: {ports}")

    # Thực hiện quét thăm dò
    try:
        start_time = time.time()
        logger.info("Bắt đầu quét thăm dò...")

        discovery_results = await discovery_scan(ip_ranges, scanner, ip_manager)

        elapsed_time = time.time() - start_time
        logger.info(f"Hoàn thành quét thăm dò trong {elapsed_time:.2f} giây")
        logger.info(f"Tìm thấy {len(discovery_results)} kết quả tiềm năng")

        # TODO: Tiếp tục với quét mục tiêu và xác minh proxy trong các giai đoạn tiếp theo

    except KeyboardInterrupt:
        logger.info("Người dùng dừng quét")
    except Exception as e:
        logger.error(f"Lỗi trong quá trình quét: {e}", exc_info=True)

    logger.info("Hoàn thành chương trình")


if __name__ == "__main__":
    asyncio.run(main())