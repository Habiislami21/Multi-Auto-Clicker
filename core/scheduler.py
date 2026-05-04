import threading
import time
from typing import Callable
from models.profile import Profile
from core.click_engine import ClickEngine
from utils.logger import logger

class Scheduler:
    def __init__(self):
        self.engine = ClickEngine()
        self.running = False
        self.paused = False
        self.thread = None
        self.on_stop_callback = None

    def start(self, profile: Profile, on_stop: Callable = None):
        """Memulai loop klik di thread terpisah."""
        if self.running:
            return
            
        self.running = True
        self.paused = False
        self.on_stop_callback = on_stop
        
        # Gunakan daemon thread agar otomatis mati jika main program di-close
        self.thread = threading.Thread(target=self._run_loop, args=(profile,), daemon=True)
        self.thread.start()
        logger.info(f"Scheduler dimulai dengan profil: {profile.name}")

    def stop(self):
        """Menghentikan loop secara paksa."""
        self.running = False
        self.paused = False
        logger.info("Scheduler dihentikan.")
        
    def pause_resume(self):
        """Toggle status pause/resume."""
        self.paused = not self.paused
        state = "dipause" if self.paused else "dilanjutkan"
        logger.info(f"Scheduler {state}.")
        return self.paused

    def _run_loop(self, profile: Profile):
        loop_count = 0
        
        while self.running:
            # Handle pause
            if self.paused:
                time.sleep(0.1)
                continue
                
            # Cek limitasi loop jika tidak infinite
            if profile.loop_type == 'fixed' and loop_count >= profile.loop_count:
                logger.info(f"Selesai! Batas loop ({profile.loop_count}) telah tercapai.")
                break

            logger.debug(f"Memulai iterasi loop ke-{loop_count + 1}")
            
            # Eksekusi setiap titik pada profil
            for point in profile.points:
                if not self.running:
                    break # Jika dihentikan di tengah-tengah
                    
                # Handle pause saat berada di dalam loop titik
                while self.paused:
                    time.sleep(0.1)
                    
                # Delay sebelum klik
                if point.delay_awal > 0:
                    time.sleep(point.delay_awal)
                    
                # Lakukan klik
                success = self.engine.execute_click(point)
                
                if not success:
                    # Failsafe aktif atau terjadi error, hentikan semuanya
                    self.running = False
                    logger.warning("Proses klik dibatalkan karena failsafe / error.")
                    break
                    
                # Tunggu interval ke klik selanjutnya (atau titik selanjutnya)
                time.sleep(point.interval)
                
            loop_count += 1
            
        self.running = False
        
        # Panggil callback untuk update UI saat berhenti
        if self.on_stop_callback:
            self.on_stop_callback()
