# Khóa luận tốt nghiệp - new

## Các bước chạy
- Lấy dữ liệu từ getphone trước (vào folder getphone để xem chi tiết)
- Chạy `pipeline.py` để load dữ liệu vào postgreSQL
  - Khởi động docker postgresql ở port 5432
  - Mở Navicat kết nối vào postgres và khởi tạo lại database ở backend/olddb
  - Chạy pipeline: `py pipeline.py`

## Tài liệu tham khảo
- [spark postgreSQL](https://mmuratarat.github.io/2020-06-18/pyspark-postgresql-locally)

## Stop:
- Dừng ở bước chuyển dữ liệu từ csv sang postgreSQL 

## Yêu cầu
### Thư viện
- `pip install psycopg2`: import database for postgresql

### Khác
- Font UTM Avo cho báo cáo tableau
- Cài hình nếu có của Tableau vào folder trong document. 

## Note
- Sau khi làm xong phần tableau, xem lại video 31 để thêm phần hướng dẫn sử dụng.
