[app]

# (str) Tên tiêu đề của ứng dụng
title = Tải Video Nhanh

# (str) Tên package (viết liền, không dấu)
package.name = videodownloader

# (str) Tên miền package ngược
package.domain = org.example

# (list) Các file nguồn cần đưa vào app
source.include_exts = py,png,jpg,kv,atlas

# (list) Thư mục chứa mã nguồn
source.dir = .

# (str) File Python chạy chính đầu tiên
source.main = main.py

# (list) Các thư viện Python cần thiết
requirements = python3,kivy,requests,beautifulsoup4,yt-dlp

# (str) Định dạng hướng màn hình (portrait = dọc)
orientation = portrait

# (list) Các quyền cần xin trên Android (INTERNET để tải video, bộ nhớ để lưu file)
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (list) Kiến trúc chip hỗ trợ (arm64-v8a cho máy đời mới, armeabi-v7a cho máy cũ)
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) Mức độ log (0 = vừa, 1 = chi tiết, 2 = debug sâu)
log_level = 2
