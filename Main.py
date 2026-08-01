import os
import re
import threading
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
import yt_dlp

class VideoDownloaderApp(toga.App):
    def startup(self):
        self.main_window = toga.App.from_name(self, title="Tải Video Nhanh")
        
        # --- GIAO DIỆN CHÍNH ---
        main_box = toga.Style(direction=COLUMN, padding=15, alignment=CENTER)
        
        self.label_title = toga.Label(
            "CHIA SẺ HOẶC DÁN LINK YOUTUBE/FACEBOOK",
            style=Pack(padding_bottom=10, font_weight="bold")
        )
        
        # Ô nhập link (Sẽ tự động điền khi người dùng chia sẻ link từ app khác sang)
        self.url_input = toga.TextInput(
            placeholder="Dán link hoặc chia sẻ từ Youtube/Facebook...",
            style=Pack(padding_bottom=15, height=45)
        )
        
        # Nút bấm tải về thủ công
        self.download_button = toga.Button(
            "TẢI VỀ NGAY",
            on_press=self.start_download_thread,
            style=Pack(padding_bottom=15, height=45, background_color="#007AFF", color="#FFFFFF")
        )
        
        # Nhãn hiển thị trạng thái và tiến trình tải
        self.status_label = toga.Label(
            "Trạng thái: Đang chờ link...",
            style=Pack(padding_top=10)
        )

        main_box.add(self.label_title)
        main_box.add(self.url_input)
        main_box.add(self.download_button)
        main_box.add(self.status_label)

        self.main_window.content = main_box
        self.main_window.show()

        # Kiểm tra xem app có được mở lên thông qua tính năng "Share" của Android hay không
        self.check_shared_intent()

    def check_shared_intent(self):
        """Hàm nhận diện nội dung được chia sẻ từ Youtube hoặc Facebook sang app"""
        try:
            # Đoạn này sẽ giao tiếp với môi trường Java Android để lấy Intent chia sẻ
            import jpype
            Intent = jpype.JClass("android.content.Intent")
            activity = toga.platform.current_app._activity
            intent = activity.getIntent()
            action = intent.getAction()
            
            if Intent.ACTION_SEND == action:
                shared_text = intent.getStringExtra(Intent.EXTRA_TEXT)
                if shared_text:
                    cleaned = self.extract_clean_url(shared_text)
                    if cleaned:
                        self.url_input.value = cleaned
                        self.status_label.text = "🎯 Đã nhận link chia sẻ! Đang tự động tải..."
                        # Tự động kích hoạt tải luôn khi nhận được link chia sẻ
                        self.start_download_thread(None)
        except Exception:
            # Chạy trên môi trường thông thường nếu không bắt được intent Java
            pass

    def extract_clean_url(self, text):
        if not text:
            return None
        text = re.sub(r'^[\^\@\s\x00-\x1f]+', '', text).strip()
        url_match = re.search(r'https?://[^\s>"\']*(?:youtube\.com|youtu\.be|facebook\.com|fb\.watch)[^\s>"\']*', text)
        if not url_match:
            return None
        clean_url = url_match.group(0)
        if 'youtube.com' in clean_url or 'youtu.be' in clean_url:
            clean_url = clean_url.split('&')[0]
        else:
            clean_url = clean_url.split('?')[0]
        return clean_url

    def start_download_thread(self, widget):
        """Chạy tiến trình tải ngầm để không bị đơ giao diện (ANR)"""
        raw_text = self.url_input.value
        video_url = self.extract_clean_url(raw_text)
        
        if not video_url:
            self.status_label.text = "❌ Lỗi: Link không hợp lệ!"
            return

        self.download_button.enabled = False
        threading.Thread(target=self.download_process, args=(video_url,)).start()

    def download_process(self, video_url):
        try:
            self.status_label.text = "🌐 Đang kết nối và tải video..."
            
            # Thư mục Download trên Android
            destination_folder = "/sdcard/Download"
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder, exist_ok=True)

            output_path = os.path.join(destination_folder, '%(title)s.%(ext)s')

            def progress_hook(d):
                if d['status'] == 'downloading':
                    p = d.get('_percent_str', '0%').strip()
                    s = d.get('_speed_str', 'N/A').strip()
                    self.status_label.text = f"🚀 Đang tải: {p} | Tốc độ: {s}"

            ydl_opts = {
                'format': 'best',
                'outtmpl': output_path,
                'progress_hooks': [progress_hook],
                'socket_timeout': 30,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            self.status_label.text = "🎉 TẢI VỀ THÀNH CÔNG! Đã lưu vào thư mục Download."
        except Exception as e:
            self.status_label.text = f"❌ Lỗi tải: {str(e)}"
        finally:
            self.download_button.enabled = True

def main():
    return VideoDownloaderApp("Tải Video Nhanh", "org.example.videodownloader")

if __name__ == "__main__":
    main()
