# Security Requirements

| ID | Yêu cầu |
|---|---|
| 1 | Hệ thống gán quyền cụ thể cho từng role, sau đó kiểm tra quyền của hàm thay vì kiểm tra cứng tên role |
| 2 | Role phải được server xác thực, mặc định thông tin do user gửi đều không tin cậy. Server phải đảm bảo fail-secure |
| 3 | Nội dung thông báo lỗi chung chung, log không được chứa thông tin nhạy cảm, cấu trúc nội bộ. |
| 4 | Log phải được cấu hình gửi real-time về server lưu trữ log tập trung. Log ghi lại thông tin hỗ trợ điều tra và server lưu trữ chỉ có quyền ghi |
| 5 | Mặc định chỉ cấp quyền tối thiểu cho user hoàn thành công việc. Cần phân tách tác vụ quan trọng và phê duyệt chéo |
| 6 | Hệ thống chỉ trả về giá trị các trường cho role trong danh sách được phép truy cập ở trường đó |
| 7 | Các service trong hệ thống có chức năng khác nhau, độc lập, và phải luôn tự xác thực với nhau |
| 8 | json_search() chỉ có quyền đọc, không thể chỉnh sửa / xóa dữ liệu hoặc thực thi các lệnh độc hại |
| 9 | Cơ chế xác thực phải sử dụng chữ ký số để chống giả mạo, chống chối bỏ. Dữ liệu cần mã hóa trước khi truyền tải hoặc lưu trữ |
| 10 | Hệ thống phải vô hiệu hóa các giao thức khám phá tự động. Bắt buộc dùng SNMP v3 và chỉ cho phép IP của server giám sát kết nối SNMP |
| 11 | Không hiển thị stack traces, lệnh SQL, hoặc phiên bản OS / framework … cho user |
| 12 | json_search() phải tự kiểm tra role trước khi thực hiện chức năng. Nếu role lạ hay rỗng thì phải deny |
