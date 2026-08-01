# Đăng ký bộ lọc Intent để bắt sự kiện chia sẻ văn bản (Text/Link) từ các app khác
android.additional_activities = <intent-filter> \
    <action android:name="android.intent.action.SEND" /> \
    <category android:name="android.intent.category.DEFAULT" /> \
    <data android:mimeType="text/plain" /> \
</intent-filter>

