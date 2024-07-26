## Luồng thiết bị 1
1. Bật ứng dụng
2. Call api kèm tọa độ -> nhận về ảnh bản đồ + tốc độ giới hạn. Để nhận được ảnh và tốc độ giới hạn thì phải tạo kế hoạch tuần tra trên dashboard.
- `Thành công`: báo thành công
- `Thất bại`: kèm log mã code từ api.
3. Ấn nút chụp ảnh
- Thực hiện xử lý hình ảnh để extract thông tin: `loại phương tiện` + `biển số` + `tốc độ của phương tiện`.
- Đóng gói dữ liệu `ảnh chụp từ camera` + `thông tin vừa extract` + `tốc độ giới hạn` sang thiết bị 2.
    - Thiết bị 2 ấn `Accept` hoặc quá 60s không phản hồi thì gửi: `ảnh chụp từ camera` + `ảnh bản đồ` + `thông tin đã extract` + `tốc độ giới hạn` sang server.
    - Thiết bị 2 ấn `Cancel`: Xóa ảnh và thông tin đã extract.
    - Thiết bị 2 ấn `Edit` (thông tin extract): ngừng timeout 60s đợi cho đến khi thiết bị 2 gửi lại thông tin đã chỉnh sửa và gửi tất cả thông tin lên server. Trong quá trình `Edit` mà thiết bị 2 gửi lại lệnh `Cancel` hoặc `Accept` thì thực hiện lệnh tương ứng.
4. Ảnh sau khi gửi thì không xóa mà đưa vào thư mục `Sent Report`. Ảnh đang được xử lý thì lưu ở `Proccessing Report`.