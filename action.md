# Kế hoạch triển khai công cụ quét proxy tự động

## Tổng quan dự án

**Tên dự án:** ProxyScanner - Công cụ quét proxy tự động từ dải IP Việt Nam  
**Mục tiêu:** Phát triển công cụ tự động scan proxy từ Internet bằng cách quét dải IP Việt Nam, xác minh và lưu trữ kết quả  
**Mục tiêu bổ sung:** 
- Triển khai các kỹ thuật quét port thân thiện (Low-Impact Port Scanning)
- Ứng dụng các biện pháp chống phát hiện và tránh bị nhà mạng chặn
- Đảm bảo tuân thủ bảo mật mạng và quy định pháp lý
  
**Thời gian triển khai:** 5 tuần  
**Ngày bắt đầu:** 25/04/2025  
**Ngày hoàn thành dự kiến:** 29/05/2025

## Bảng tiến độ công việc

| Giai đoạn | Công việc | Thời gian | Tiến độ | Người thực hiện |
|-----------|-----------|-----------|---------|-----------------|
| 1 | Nghiên cứu và chuẩn bị | 25/04 - 29/04 | Chưa bắt đầu | [YOUR_NAME] |
| 2 | Xây dựng chức năng quét cơ bản | 30/04 - 06/05 | Chưa bắt đầu | [YOUR_NAME] |
| 3 | Xác minh và phân loại proxy | 07/05 - 13/05 | Chưa bắt đầu | [YOUR_NAME] |
| 4 | Xây dựng API và lưu trữ | 14/05 - 18/05 | Chưa bắt đầu | [YOUR_NAME] |
| 5 | Kiểm thử và tối ưu | 19/05 - 22/05 | Chưa bắt đầu | [YOUR_NAME] |

## Chi tiết triển khai

### Giai đoạn 1: Nghiên cứu và chuẩn bị (25/04 - 29/04)

- [x] **Ngày 1-2 (25/04 - 26/04)**: Nghiên cứu và thu thập dữ liệu
  - [x] Thu thập danh sách dải IP Việt Nam cập nhật
  - [x] Nghiên cứu công cụ quét (nmap, zmap) và thư viện hỗ trợ
  - [x] Xác định các cổng proxy phổ biến cần quét
  - [ ] Nghiên cứu các hệ thống phát hiện xâm nhập mạng (IDS/IPS) và cách hoạt động
  - [ ] Tìm hiểu các chính sách về an ninh mạng và giới hạn của nhà mạng Việt Nam

- [x] **Ngày 3-4 (27/04 - 28/04)**: Thiết kế cấu trúc dự án
  - [x] Thiết kế cấu trúc mã nguồn theo mô hình module
  - [x] Lựa chọn thư viện và công cụ phù hợp (scapy, asyncio, aiohttp)
  - [x] Cài đặt môi trường phát triển
  - [ ] Thiết kế hệ thống theo dõi và điều chỉnh tốc độ quét tự động

- [ ] **Ngày 5 (29/04)**: Xây dựng kế hoạch kiểm thử và tài liệu
  - [ ] Xây dựng kế hoạch kiểm thử với mục tiêu đảm bảo quét thân thiện
  - [x] Chuẩn bị tài liệu kỹ thuật cho dự án
  - [ ] Thiết kế hệ thống giám sát để phát hiện sớm khi bị chặn
  - [ ] Xây dựng quy trình phản ứng khi phát hiện bị chặn
  - [ ] Phát triển tiêu chí đánh giá hiệu quả của phương pháp quét thân thiện

### Giai đoạn 2: Triển khai phương pháp quét port thân thiện (30/04 - 03/05)

- [ ] **Ngày 1-2 (30/04 - 01/05)**: Nghiên cứu và thiết kế quét port thân thiện
  - [ ] Phân tích các phương pháp quét thân thiện (Slow Scanning, Distributed Scanning, Incremental Scanning)
  - [ ] Nghiên cứu kỹ thuật SYN Scanning với độ trễ và Passive OS Fingerprinting
  - [ ] Thiết kế mô hình quét 3 giai đoạn (thăm dò, mục tiêu, xác minh)
  - [ ] Xây dựng chiến lược quét theo thời gian và phân tán theo không gian IP

- [ ] **Ngày 3-4 (02/05 - 03/05)**: Triển khai các module quét thân thiện
  - [ ] Phát triển class AdaptiveRateController để điều chỉnh tốc độ quét tự động
  - [ ] Triển khai Connection Pooling để quản lý kết nối
  - [ ] Phát triển kỹ thuật Smart Retries với thời gian chờ tăng dần
  - [ ] Xây dựng module phân tích mức độ hoạt động mạng và điều chỉnh quét theo giờ
  - [ ] Phát triển hệ thống quét theo batch với nghỉ thông minh

### Giai đoạn 3: Xây dựng chức năng quét cơ bản và kỹ thuật chống phát hiện (04/05 - 10/05)

- [ ] **Ngày 1-2 (04/05 - 05/05)**: Triển khai chức năng quét cơ bản
  - [ ] Phát triển module xử lý dải IP
  - [ ] Tích hợp nmap/zmap với các tham số thân thiện
  - [ ] Phát triển lựa chọn cổng thông minh (Port Selection Optimization)

- [ ] **Ngày 3-4 (06/05 - 07/05)**: Tối ưu hóa quét và triển khai biện pháp chống phát hiện
  - [ ] Triển khai quét đa luồng có kiểm soát
  - [ ] Cấu hình tốc độ quét thấp (30-50 packets/giây ban ngày, 50-100 packets/giây ban đêm)
  - [ ] Xây dựng cơ chế xoay IP
  - [ ] Triển khai kỹ thuật TCB (Temporal Covert Behavior) và phân mảnh gói tin
  - [ ] Cài đặt hệ thống phát hiện và phản ứng khi bị chặn

- [ ] **Ngày 5-7 (08/05 - 10/05)**: Hoàn thiện và kiểm thử quét
  - [ ] Triển khai cơ chế giới hạn tốc độ động và jitter ngẫu nhiên
  - [ ] Cài đặt lịch quét thông minh (quét vào thời điểm lưu lượng mạng thấp)
  - [ ] Triển khai phân tán quét trên nhiều dải IP đồng thời
  - [ ] Kiểm thử hiệu suất quét và khả năng né tránh phát hiện
  - [ ] Đo đạc và tối ưu tỷ lệ quét thành công

### Giai đoạn 4: Xác minh và phân loại proxy (11/05 - 17/05)

- [ ] **Ngày 1-2 (11/05 - 12/05)**: Xác minh proxy thân thiện
  - [ ] Phát triển logic kiểm tra kết nối proxy với biện pháp chống phát hiện
  - [ ] Xác minh proxy HTTP và HTTPS với headers đa dạng
  - [ ] Triển khai kiểm tra bất đồng bộ với giới hạn kết nối và jitter
  - [ ] Thực hiện xác minh theo lô nhỏ với độ trễ ngẫu nhiên

- [ ] **Ngày 3-4 (13/05 - 14/05)**: Xác minh proxy nâng cao
  - [ ] Bổ sung xác minh SOCKS4 và SOCKS5
  - [ ] Đo tốc độ và độ trễ proxy theo nhiều thời điểm
  - [ ] Kiểm tra độ ẩn danh của proxy với nhiều phương pháp
  - [ ] Phát triển xác minh theo mô hình phân tầng (đánh dấu độ tin cậy)

- [ ] **Ngày 5-7 (15/05 - 17/05)**: Phân loại và lọc proxy
  - [ ] Phân loại proxy theo loại (HTTP, HTTPS, SOCKS)
  - [ ] Phân loại proxy theo mức độ ẩn danh
  - [ ] Phân loại theo vị trí địa lý và tốc độ
  - [ ] Phát triển hệ thống xếp hạng proxy theo nhiều tiêu chí
  - [ ] Triển khai theo dõi độ ổn định proxy theo thời gian

### Giai đoạn 5: Xây dựng API và lưu trữ (18/05 - 22/05)

- [ ] **Ngày 1-2 (18/05 - 19/05)**: Lưu trữ proxy thông minh
  - [ ] Triển khai lưu trữ trong RAM với cấu trúc dữ liệu tối ưu
  - [ ] Xây dựng cơ chế cập nhật liên tục với kiểm soát tải
  - [ ] Theo dõi thời gian sống và độ ổn định của proxy
  - [ ] Thiết kế hệ thống xếp hạng và thay thế proxy tự động

- [ ] **Ngày 3-5 (20/05 - 22/05)**: Xây dựng REST API thân thiện
  - [ ] Triển khai API lấy danh sách proxy với nhiều tùy chọn lọc
  - [ ] Triển khai API lấy proxy ngẫu nhiên theo tiêu chí (tốc độ, ổn định, khu vực)
  - [ ] Triển khai API thống kê với nhiều chỉ số
  - [ ] Triển khai giới hạn tốc độ gọi API để tránh quá tải
  - [ ] Viết tài liệu API chi tiết

### Giai đoạn 6: Kiểm thử và tối ưu (23/05 - 29/05)

- [ ] **Ngày 1-3 (23/05 - 25/05)**: Kiểm thử tổng thể
  - [ ] Kiểm thử toàn diện chức năng quét thân thiện
  - [ ] Kiểm thử hiệu suất và tác động của quét thân thiện đến mạng
  - [ ] Kiểm thử xác minh proxy với nhiều kịch bản sử dụng
  - [ ] Kiểm thử API và hiệu năng dưới tải
  - [ ] Kiểm thử khả năng chống phát hiện và tránh bị chặn
  - [ ] Kiểm thử phục hồi sau khi bị chặn tạm thời
  - [ ] Kiểm thử tính ổn định trong thời gian dài (24-48 giờ)

- [ ] **Ngày 4-7 (26/05 - 29/05)**: Tối ưu hóa và hoàn thiện
  - [ ] Tối ưu hiệu suất quét thân thiện dựa trên dữ liệu kiểm thử
  - [ ] Tối ưu bộ nhớ sử dụng và quản lý tài nguyên
  - [ ] Hiệu chỉnh thông số quét để tối ưu khả năng né tránh
  - [ ] Thiết lập hệ thống cảnh báo và tự phục hồi
  - [ ] Phát triển dashboard giám sát hiệu suất quét và phát hiện anomaly
  - [ ] Chuẩn bị các giá trị mặc định được tối ưu cho quét thân thiện
  - [ ] Hoàn thiện tài liệu và hướng dẫn sử dụng với tập trung vào quét thân thiện

## Đánh giá rủi ro và biện pháp ứng phó

| Rủi ro | Mức độ ảnh hưởng | Khả năng xảy ra | Biện pháp ứng phó |
|--------|-----------------|-----------------|-------------------|
| Bị nhà mạng chặn khi quét | Cao | Trung bình | **Quét thân thiện**: Giảm tốc độ quét (30-50 packets/giây), xoay IP nguồn, phân bổ quét, sử dụng kỹ thuật mô hình quét 3 giai đoạn (thăm dò, mục tiêu, xác minh) |
| Bị phát hiện là bot bởi hệ thống tự vệ | Cao | Cao | **Quét ngụy trang**: Tùy chỉnh header, thay đổi TTL, kích thước gói tin, sử dụng nhiều IP nguồn, triển khai TCB và jitter ngẫu nhiên (0.1-2s) |
| Tỷ lệ proxy hoạt động thấp | Trung bình | Cao | **Quét thông minh**: Port Selection Optimization, quét vào giờ thấp điểm (22:00 - 06:00), quét theo thời gian dựa trên phân tích tỷ lệ thành công |
| Quá tải do quét nhiều IP | Trung bình | Thấp | **Quét theo batch**: Batch nhỏ (20-50 IP/batch), thời gian nghỉ ngẫu nhiên giữa các batch (1-5 phút), tránh scan liên tục |
| Vấn đề tuân thủ pháp lý | Cao | Trung bình | **Quét có trách nhiệm**: Đảm bảo tuân thủ, quét với tốc độ cực thấp, ưu tiên IP mạng có chính sách cho phép quét, bỏ qua hệ thống quan trọng |
| Bị chặn vĩnh viễn bởi nhà mạng | Cao | Thấp | **Quét thích nghi**: Tự động giảm 50% tốc độ khi phát hiện dấu hiệu chặn, thời gian nghỉ dài (2-6 giờ), chiến lược luân phiên giữa các nhóm IP |
| Tác động tiêu cực đến hệ thống đích | Cao | Trung bình | **Quét thân thiện với hệ thống**: Sử dụng SYN scan với retransmit thấp, đóng kết nối đúng cách, phát hiện và bỏ qua hệ thống nhạy cảm |
| Xác minh proxy gây tải lớn | Trung bình | Cao | **Xác minh thông minh**: Giới hạn 5-10 kết nối đồng thời, thời gian chờ thích ứng, adaptive backoff khi thất bại |

## Tài nguyên cần thiết

- **Phần cứng**:
  - Máy chủ với băng thông cao
  - Đường truyền mạng ổn định (tốt nhất là nhiều kết nối mạng khác nhau)
  - Tối thiểu 4GB RAM
  - Nếu có thể, sử dụng nhiều máy chủ với nhiều IP khác nhau
  - Các máy chủ nên đặt ở vị trí địa lý khác nhau (để phân tán quét)

- **Phần mềm**:
  - Python 3.8+
  - Nmap hoặc Zmap với tùy chọn nâng cao
  - Nmap cho quét thăm dò thân thiện
  - Flask hoặc FastAPI cho REST API
  - Thư viện: 
    - scapy (cho tùy chỉnh gói tin thân thiện)
    - asyncio, aiohttp (cho quét và xác minh bất đồng bộ)
    - requests (cho xác minh đơn giản)
    - geoip2 (định vị địa lý)
    - pytz (hỗ trợ múi giờ để quét theo thời gian)
    - numpy, pandas (phân tích dữ liệu quét)
  - Proxy rotator (để xoay IP nguồn nếu cần)
  - VPN hoặc proxy (để thay đổi IP nguồn)
  - Hệ thống giám sát mạng (network monitoring)

- **Dữ liệu**:
  - Danh sách dải IP Việt Nam cập nhật
  - Cơ sở dữ liệu GeoIP để xác định vị trí
  - Danh sách User-Agent đa dạng (>100 mẫu)
  - Dữ liệu phân tích lưu lượng mạng theo thời gian để lên lịch quét tối ưu
  - Danh sách cổng proxy phân theo mức độ phổ biến
  - Blacklist các IP/dải IP nhạy cảm cần tránh quét

## Mốc kiểm tra tiến độ

- **Tuần 1 (29/04)**: Hoàn thành kế hoạch, nghiên cứu và thiết kế
- **Tuần 2 (03/05)**: Hoàn thành triển khai phương pháp quét port thân thiện
- **Tuần 3 (10/05)**: Hoàn thành chức năng quét cơ bản và kỹ thuật chống phát hiện
- **Tuần 4 (17/05)**: Hoàn thành xác minh và phân loại proxy
- **Tuần 5 (22/05)**: Hoàn thành API và lưu trữ
- **Cuối dự án (29/05)**: Hoàn thành kiểm thử và tối ưu hóa

### Tiêu chí đánh giá mốc

1. **Mốc phương pháp quét port thân thiện**:
   - Thực hiện thành công quét thăm dò với tốc độ <50 packets/giây
   - Đạt hiệu suất quét mà không kích hoạt IDS/IPS
   - Triển khai thành công mô hình quét 3 giai đoạn
   - Xác minh tác động thấp đến hệ thống đích

2. **Mốc chức năng quét và chống phát hiện**:
   - Quét thành công ít nhất 3 dải IP lớn mà không bị chặn
   - Xác minh tính năng phát hiện và phản ứng khi bị chặn
   - Kiểm chứng hiệu quả của kỹ thuật ngụy trang quét

3. **Mốc xác minh proxy**:
   - Xác minh thành công ít nhất 50 proxy
   - Phân loại chính xác theo loại và mức độ ẩn danh
   - Đánh giá được tốc độ và độ ổn định

4. **Mốc API và kiểm thử**:
   - API hoàn chỉnh với đầy đủ tính năng
   - Kiểm thử toàn diện trên nhiều kịch bản
   - Vận hành ổn định trong ít nhất 48 giờ

## Chiến lược quét thân thiện

### Mô hình quét 3 giai đoạn

1. **Giai đoạn 1: Quét thăm dò (Discovery Scanning)**
   - **Tốc độ quét**: Cực thấp (10-20 packets/giây)
   - **Phương pháp**: SYN scan hoặc Connection scan với độ trễ cao
   - **Phạm vi**: Quét rộng trên các dải IP để xác định host đang hoạt động
   - **Cổng**: Chỉ quét 1-2 cổng phổ biến nhất (8080, 3128)
   - **Độ trễ giữa các gói tin**: 50-200ms
   - **Thời gian quét**: Ưu tiên quét vào giờ thấp điểm (22:00 - 06:00)

2. **Giai đoạn 2: Quét mục tiêu (Targeted Scanning)**
   - **Tốc độ quét**: Thấp (20-40 packets/giây)
   - **Phương pháp**: Quét từng cổng riêng biệt với độ trễ ngẫu nhiên
   - **Phạm vi**: Chỉ quét các IP đã xác định hoạt động từ giai đoạn 1
   - **Cổng**: Quét đầy đủ các cổng proxy phổ biến (5-10 cổng)
   - **Batch size**: 20-50 IP mỗi batch
   - **Thời gian nghỉ giữa các batch**: 1-5 phút

3. **Giai đoạn 3: Xác minh proxy (Verification)**
   - **Kết nối đồng thời**: Giới hạn (5-10 kết nối)
   - **Phương pháp**: Thử kết nối qua proxy với headers ngẫu nhiên
   - **Thời gian chờ**: Thích ứng (bắt đầu 2s, tăng dần nếu cần)
   - **Jitter**: 0.1-1s giữa các lần xác minh
   - **Số lần thử lại**: 1-2 lần với backoff

### Lịch quét thông minh

- **Giờ cao điểm (8:00-22:00)**: Giảm 50% tốc độ quét, tăng jitter
- **Giờ thấp điểm (22:00-8:00)**: Có thể tăng tốc độ quét lên 30-50%
- **Cuối tuần**: Ưu tiên quét vào đêm khuya Thứ 7 và sáng sớm Chủ nhật
- **Quét xoay vòng**: Mỗi dải IP lớn chỉ quét 1 lần/tuần

### Kỹ thuật né tránh phát hiện

- **TCB (Temporal Covert Behavior)**: Quét theo mẫu thời gian không đều
- **Headers ngẫu nhiên**: Thay đổi User-Agent và Accept headers trong mỗi request
- **Phân mảnh gói tin**: Chia nhỏ gói tin TCP để tránh phát hiện
- **TTL ngẫu nhiên**: Sử dụng TTL trong khoảng 48-255
- **Kích thước gói tin thay đổi**: Thêm padding ngẫu nhiên
- **Source port ngẫu nhiên**: Thay đổi cổng nguồn trong mỗi kết nối

## Hướng dẫn sử dụng (được cập nhật sau khi hoàn thành)

- Cài đặt công cụ
- Cấu hình quét thân thiện
- Điều chỉnh tham số quét theo môi trường
- Khởi chạy và giám sát
- Sử dụng API để truy xuất proxy
- Xử lý sự cố thường gặp
- Phát hiện và phục hồi khi bị chặn

---

## Theo dõi tiến độ

| Giai đoạn | Hoàn thành | Nhận xét |
|-----------|------------|----------|
| Giai đoạn 1: Nghiên cứu và chuẩn bị | 60% | Đã thiết lập cấu trúc dự án, thư viện cần thiết và cài đặt môi trường. Đã thu thập danh sách dải IP và bắt đầu triển khai các module cơ bản. |
| Giai đoạn 2: Triển khai phương pháp quét port thân thiện | 0% | Chưa bắt đầu |
| Giai đoạn 3: Xây dựng chức năng quét cơ bản và kỹ thuật chống phát hiện | 0% | Chưa bắt đầu |
| Giai đoạn 4: Xác minh và phân loại proxy | 0% | Chưa bắt đầu |
| Giai đoạn 5: Xây dựng API và lưu trữ | 0% | Chưa bắt đầu |
| Giai đoạn 6: Kiểm thử và tối ưu | 0% | Chưa bắt đầu |
| Tổng tiến độ | 10% | Dự án đã được bắt đầu, cấu trúc cơ bản đã được thiết lập |

### Chỉ số hiệu suất quét

| Chỉ số | Mục tiêu | Hiện tại | Trạng thái |
|--------|----------|----------|------------|
| Tỷ lệ quét không bị chặn | >95% | - | Chưa đo |
| Tỷ lệ phát hiện cổng mở | >80% | - | Chưa đo |
| Tốc độ quét trung bình | 30-50 pps | 15-20 pps | Đang cấu hình |
| Mức độ phát hiện bởi IDS | <5% | - | Chưa đo |
| Số proxy đã tìm thấy | >500 | 0 | Chưa triển khai |

*Cập nhật lần cuối: 25/04/2025*