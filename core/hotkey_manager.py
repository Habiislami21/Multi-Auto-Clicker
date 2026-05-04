from pynput import keyboard
from utils.logger import logger

class HotkeyManager:
    def __init__(self, start_stop_cb, pause_resume_cb, grab_cb):
        self.start_stop_cb = start_stop_cb
        self.pause_resume_cb = pause_resume_cb
        self.grab_cb = grab_cb
        self.listener = None
        
        # Binding default (bisa dibuat dinamis ke depannya)
        self.toggle_key = keyboard.Key.f6
        self.pause_key = keyboard.Key.f7
        self.grab_key = keyboard.Key.f8

    def start_listening(self):
        """Memulai mendengarkan input keyboard secara global"""
        if self.listener is None:
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
            logger.info("Hotkey listener aktif (F6: Start/Stop, F7: Pause, F8: Grab Posisi).")

    def stop_listening(self):
        """Menghentikan listener"""
        if self.listener:
            self.listener.stop()
            self.listener = None
            logger.info("Hotkey listener dimatikan.")

    def on_press(self, key):
        """Menangani event tombol ditekan"""
        try:
            if key == self.toggle_key:
                logger.debug("Hotkey Start/Stop ditekan.")
                self.start_stop_cb()
            elif key == self.pause_key:
                logger.debug("Hotkey Pause/Resume ditekan.")
                self.pause_resume_cb()
            elif key == self.grab_key:
                logger.debug("Hotkey Grab ditekan.")
                self.grab_cb()
        except Exception as e:
            logger.error(f"Error pada handler hotkey: {e}")
