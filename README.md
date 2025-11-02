
# Website Bán Đồ Ngọt - Sweetshop

Đây là một dự án ứng dụng web thương mại điện tử hoàn chỉnh được xây dựng bằng Python và framework Flask. Ứng dụng mô phỏng một cửa hàng bánh ngọt trực tuyến, bao gồm các chức năng cho cả khách hàng và người quản trị.

## Tính năng chính

### Chức năng cho Người dùng (Khách hàng)

- **Xác thực:** Đăng ký tài khoản mới, đăng nhập và đăng xuất.
- **Xem sản phẩm:** Duyệt xem danh sách sản phẩm, xem thông tin chi tiết của từng sản phẩm.
- **Giỏ hàng:** Thêm sản phẩm vào giỏ, xem giỏ hàng, cập nhật số lượng hoặc xóa sản phẩm.
- **Thanh toán:** Thực hiện quy trình đặt hàng với phương thức thanh toán khi nhận hàng (COD).
- **Quản lý tài khoản:** Xem lại lịch sử các đơn hàng đã đặt.

### Chức năng cho Quản trị viên

- **Bảng điều khiển (Dashboard):** Trang tổng quan dành riêng cho quản trị viên.
- **Quản lý sản phẩm:** Thêm, sửa, xóa các sản phẩm của cửa hàng.
- **Quản lý đơn hàng:** Xem tất cả đơn hàng từ khách hàng và cập nhật trạng thái (ví dụ: Đang xử lý -> Đang giao hàng).
- **Quản lý người dùng:** Xem danh sách tất cả người dùng trong hệ thống.

---

## Công nghệ sử dụng

- **Backend:**
  - Ngôn ngữ: **Python 3**
  - Framework: **Flask**
  - ORM (Object-Relational Mapping): **Flask-SQLAlchemy**
  - Xử lý CSDL Migrations: **Flask-Migrate**
  - Xác thực người dùng: **Flask-Login**
  - Xử lý Biểu mẫu (Forms): **Flask-WTF**
- **Frontend:**
  - Template Engine: **Jinja2**
  - CSS Framework: **Bootstrap 5** (thông qua các class trong template)
- **Cơ sở dữ liệu:**
  - Môi trường phát triển: **SQLite**

---

## Hướng dẫn Cài đặt và Chạy dự án

Làm theo các bước dưới đây để chạy dự án trên máy tính của bạn.

### 1. Yêu cầu

- Python 3.8 trở lên
- Git

### 2. Các bước cài đặt

**Bước 1: Tải mã nguồn về máy**

Mở terminal (hoặc Command Prompt/PowerShell trên Windows) và chạy lệnh sau:
```bash
git clone https://github.com/KTD1108/web_py.git
cd sweetshop
```

**Bước 2: Tạo và kích hoạt môi trường ảo**

Việc này giúp cô lập các thư viện của dự án, tránh xung đột với các dự án Python khác.
```bash
# Lệnh tạo môi trường ảo có tên là 'venv'
python -m venv venv

# Kích hoạt môi trường ảo
# Trên Windows:
.\venv\Scripts\activate

# Trên macOS/Linux:
source venv/bin/activate
```

**Bước 3: Cài đặt các thư viện cần thiết**

Lệnh sau sẽ tự động cài đặt tất cả các thư viện được liệt kê trong `requirements.txt`.
```bash
pip install -r requirements.txt
```

**Bước 4: Cấu hình biến môi trường**

Tạo một tệp mới tên là `.env` trong thư mục gốc của dự án và thêm nội dung sau vào. Đây là khóa bí mật để Flask bảo vệ session của người dùng.
```
SECRET_KEY='mot-chuoi-bi-mat-ngau-nhien-do-ban-tu-tao-ra'
```

**Bước 5: Khởi tạo Cơ sở dữ liệu**

Chạy lệnh sau để tạo các bảng trong cơ sở dữ liệu SQLite dựa trên các model đã định nghĩa.
```bash
flask db upgrade
```

**Bước 6: Chạy ứng dụng**

Khởi động server phát triển của Flask.
```bash
flask run
```

Sau khi server khởi động, mở trình duyệt và truy cập vào địa chỉ: `http://127.0.0.1:5000`

### 3. Tạo tài khoản Admin

Để truy cập trang quản trị, bạn cần một tài khoản có quyền admin. Chạy các lệnh sau trong terminal (đảm bảo môi trường ảo đã được kích hoạt):

1. Mở Flask shell:
   ```bash
   flask shell
   ```

2. Bên trong shell, chạy các lệnh Python sau:
   ```python
   from app import create_app, db
   from app.models import User
   
   app = create_app()
   with app.app_context():
       # Thay đổi username và password tùy ý
       admin = User(username='admin', email='admin@example.com', is_admin=True)
       admin.set_password('admin123')
       db.session.add(admin)
       db.session.commit()
       print('Admin user created successfully!')
   ```

Bây giờ bạn có thể đăng nhập bằng tài khoản `admin` và mật khẩu `admin123` để truy cập các chức năng quản trị.

---

## Cấu trúc thư mục

```
/sweetshop
|-- app/              # Mã nguồn chính của ứng dụng
|   |-- admin/        # Blueprint cho trang quản trị
|   |-- auth/         # Blueprint cho xác thực
|   |-- main/         # Blueprint cho các chức năng chính
|   |-- static/       # Chứa CSS, JS, hình ảnh
|   |-- templates/    # Chứa các tệp HTML
|   |-- __init__.py   # Application Factory (hàm create_app)
|   |-- models.py     # Định nghĩa các bảng CSDL
|-- migrations/       # Chứa các script cập nhật CSDL
|-- instance/         # Chứa file CSDL SQLite
|-- config.py         # Các lớp cấu hình
|-- run.py            # Tệp để chạy ứng dụng
|-- requirements.txt  # Danh sách thư viện
|-- .env              # File biến môi trường
`-- README.md         # Tệp hướng dẫn này
```
