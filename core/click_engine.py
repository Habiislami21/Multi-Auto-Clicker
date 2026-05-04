from pynput.mouse import Controller as MouseController, Button
import pyautogui
import time
from utils.logger import logger

class ClickEngine:
    def __init__(self):
        self.mouse = MouseController()
        
    def execute_click(self, point):
        """
        Mengeksekusi satu klik berdasarkan konfigurasi ClickPoint.
        Mengembalikan True jika sukses, False jika gagal atau failsafe aktif.
        """
        # Safety Check: Cegah runaway click dengan mengarahkan mouse ke pojok layar
        if self._is_failsafe_triggered():
            logger.warning("Failsafe aktif! Mouse terdeteksi di pojok layar. Menghentikan klik.")
            return False

        try:
            # Pindahkan kursor
            self.mouse.position = (point.x, point.y)
            time.sleep(0.05) # Delay super singkat agar OS register pergerakan mouse
            
            # Tentukan jenis tombol mouse
            if point.button == 'left':
                btn = Button.left
            elif point.button == 'right':
                btn = Button.right
            else:
                btn = Button.middle
                
            # Tentukan jumlah klik (single atau double)
            click_count = 2 if point.click_type == 'double' else 1
            
            # Eksekusi
            self.mouse.click(btn, click_count)
            logger.debug(f"Clicked at ({point.x}, {point.y}) - {point.button} {point.click_type}")
            return True
            
        except Exception as e:
            logger.error(f"Error saat mengeksekusi klik: {e}")
            return False
            
    def _is_failsafe_triggered(self):
        """Mengecek apakah kursor berada di salah satu pojok layar"""
        try:
            x, y = pyautogui.position()
            screen_width, screen_height = pyautogui.size()
            
            # Cek pojok kiri atas, kanan atas, kiri bawah, kanan bawah
            if (x <= 2 and y <= 2) or \
               (x >= screen_width - 2 and y <= 2) or \
               (x <= 2 and y >= screen_height - 2) or \
               (x >= screen_width - 2 and y >= screen_height - 2):
                return True
        except Exception:
            pass
        return False
