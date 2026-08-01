[app]
title = Tải Video Nhanh
package.name = videodownloader
package.domain = org.example
source.include_exts = py,png,jpg,kv,atlas
source.dir = .
source.main = main.py
requirements = python3,kivy,requests,beautifulsoup4,yt-dlp
orientation = portrait
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
