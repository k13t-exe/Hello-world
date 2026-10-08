# Threat Model

## 1. Vai trò người dùng

- **Admin:** toàn quyền truy xuất thông tin để quản lý toàn diện, xử lý sự cố
- **Operator:** tra cứu thông tin cần để giám sát hạ tầng mạng, phản hồi sự cố
- **Viewer:** chỉ được xem các thông tin được cho phép, không nhạy cảm

## 2. Asset nhạy cảm

- **Thông tin định danh và định tuyến:** IP nội bộ, MAC, routing tables,...
- **Thông tin thiết bị:** phiên bản OS, firmware,...
- **Thông tin xác thực:** chuỗi xác thực SNMP, API key, SSH key,...

## 3. Trust boundary

Trust boundary giữa AuthN và AuthZ bị bỏ qua nếu hàm không kiểm tra role trước khi trả kết quả. Người dùng không tin cậy có thể thực hiện chức năng đặc quyền, truy cập và thao túng mọi dữ liệu nhạy cảm.

## 4. Threat

| Threat | STRIDE | Kịch bản |
|---|---|---|
| Không xác thực user | I / E | Không kiểm tra role trước khi trả kết quả |
| Trả thừa thông tin so với quyền | I | Được gọi hàm nhưng kết quả chứa cả thông tin dành cho role cao hơn |
| Rò rỉ qua lỗi và log | I | Lỗi trả về làm lộ schema, cấu trúc, hoặc token. Log ghi lại thông tin nhạy cảm |
| Giả mạo role | S / E | User chỉnh sửa request để mạo danh admin và leo thang đặc quyền |
| Leo thang đặc quyền | E | Sau khi lấy được credential của admin, user đăng nhập và chiếm quyền kiểm soát |
| Lộ cấu trúc mạng | I | Attacker dựng lại network topology để chọn mục tiêu, tìm điểm yếu để tấn công |
| Không truy vết được | R | Log, dữ liệu giám sát có thể bị xóa, chỉnh sửa |
