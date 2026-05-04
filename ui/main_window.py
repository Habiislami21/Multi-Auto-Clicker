import customtkinter as ctk
import tkinter as tk
import pyautogui
from models.profile import Profile, ClickPoint, ProfileManager
from core.scheduler import Scheduler
from core.hotkey_manager import HotkeyManager
from utils.logger import logger

# Setup tema bawaan
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Multi Auto Clicker Pro")
        self.geometry("900x650")
        self.minsize(800, 600)
        
        # Inisialisasi Modul
        self.profile_manager = ProfileManager()
        self.scheduler = Scheduler()
        self.hotkey_manager = HotkeyManager(
            start_stop_cb=self.toggle_clicking,
            pause_resume_cb=self.toggle_pause,
            grab_cb=self.handle_grab
        )
        self.hotkey_manager.start_listening()
        
        # State
        self.point_frames = []
        self.current_profile_name = "default"
        self.grabbing_mode = False
        
        # Build UI
        self.setup_ui()
        self.load_profiles_list()
        
    def setup_ui(self):
        # Grid System
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # === Sidebar (Kiri) ===
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(5, weight=1) # Memberi ruang agar mode app ke bawah
        
        # Logo / Judul
        self.logo_label = ctk.CTkLabel(self.sidebar, text="AutoClicker Pro", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        
        # Profile Section
        ctk.CTkLabel(self.sidebar, text="Profile Management:").grid(row=1, column=0, padx=20, pady=(0, 5), sticky="w")
        
        self.profile_var = ctk.StringVar(value="Pilih Profil...")
        self.profile_dropdown = ctk.CTkOptionMenu(self.sidebar, variable=self.profile_var, command=self.on_profile_select)
        self.profile_dropdown.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        self.btn_save_profile = ctk.CTkButton(self.sidebar, text="Simpan Profil", command=self.save_current_profile)
        self.btn_save_profile.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        
        self.btn_new_profile = ctk.CTkButton(self.sidebar, text="Profil Baru", command=self.clear_points, fg_color="gray", hover_color="darkgray")
        self.btn_new_profile.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        
        # Theme Section
        self.appearance_label = ctk.CTkLabel(self.sidebar, text="Mode Tampilan:")
        self.appearance_label.grid(row=6, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.appearance_menu = ctk.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"], command=self.change_appearance)
        self.appearance_menu.grid(row=7, column=0, padx=20, pady=(5, 20), sticky="ew")
        self.appearance_menu.set("Dark")
        
        # === Main Content (Kanan) ===
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Header Controls (Top)
        self.top_controls = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.top_controls.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.btn_add_point = ctk.CTkButton(self.top_controls, text="+ Tambah Titik", command=self.add_point_ui)
        self.btn_add_point.pack(side="left", padx=5)
        
        self.btn_grab_point = ctk.CTkButton(self.top_controls, text="Ambil Kordinat (F8)", command=self.toggle_grab_mode, fg_color="#D35B58", hover_color="#C75050")
        self.btn_grab_point.pack(side="left", padx=5)
        
        self.lbl_status = ctk.CTkLabel(self.top_controls, text="Status: IDLE", text_color="gray", font=ctk.CTkFont(weight="bold"))
        self.lbl_status.pack(side="right", padx=10)
        
        # Scrollable Area untuk List Titik
        self.scrollable_points = ctk.CTkScrollableFrame(self.main_frame, label_text="Daftar Urutan Klik")
        self.scrollable_points.grid(row=1, column=0, sticky="nsew")
        
        # Footer Controls (Bottom)
        self.bottom_controls = ctk.CTkFrame(self.main_frame)
        self.bottom_controls.grid(row=2, column=0, sticky="ew", pady=(15, 0), ipadx=10, ipady=10)
        
        # Loop Settings
        self.loop_var = ctk.StringVar(value="infinite")
        self.radio_infinite = ctk.CTkRadioButton(self.bottom_controls, text="Tak Terbatas", variable=self.loop_var, value="infinite")
        self.radio_infinite.pack(side="left", padx=15, pady=10)
        
        self.radio_fixed = ctk.CTkRadioButton(self.bottom_controls, text="Batas Loop:", variable=self.loop_var, value="fixed")
        self.radio_fixed.pack(side="left", padx=(15, 5), pady=10)
        
        self.entry_loop_count = ctk.CTkEntry(self.bottom_controls, width=60)
        self.entry_loop_count.insert(0, "1")
        self.entry_loop_count.pack(side="left", padx=5, pady=10)
        
        # Action Buttons
        self.btn_start = ctk.CTkButton(self.bottom_controls, text="MULAI (F6)", command=self.toggle_clicking, fg_color="#28a745", hover_color="#218838", font=ctk.CTkFont(weight="bold"))
        self.btn_start.pack(side="right", padx=15, pady=10)
        
        self.btn_pause = ctk.CTkButton(self.bottom_controls, text="PAUSE (F7)", command=self.toggle_pause, state="disabled", fg_color="#ffc107", hover_color="#e0a800", text_color="black", font=ctk.CTkFont(weight="bold"))
        self.btn_pause.pack(side="right", padx=5, pady=10)

    # --- Appearance ---
    def change_appearance(self, new_mode: str):
        ctk.set_appearance_mode(new_mode)
        
    # --- Profile Management ---
    def load_profiles_list(self):
        profiles = self.profile_manager.get_all_profiles()
        if profiles:
            self.profile_dropdown.configure(values=profiles)
            
    def on_profile_select(self, choice):
        profile = self.profile_manager.load_profile(choice)
        if profile:
            self.current_profile_name = profile.name
            self.loop_var.set(profile.loop_type)
            self.entry_loop_count.delete(0, tk.END)
            self.entry_loop_count.insert(0, str(profile.loop_count))
            
            # Hapus titik yg ada dan tambahkan yg baru
            self.clear_points()
            for p in profile.points:
                self.add_point_ui(p.x, p.y, p.interval, p.button, p.click_type, p.delay_awal)
                
    def clear_points(self):
        for pf in self.point_frames:
            pf.destroy()
        self.point_frames.clear()
        self.profile_var.set("Pilih Profil...")
        
    def save_current_profile(self):
        dialog = ctk.CTkInputDialog(text="Masukkan Nama Profil:", title="Simpan Profil")
        name = dialog.get_input()
        if name:
            self.current_profile_name = name
            prof = self.get_current_profile_data()
            if prof:
                self.profile_manager.save_profile(prof)
                self.load_profiles_list()
                self.profile_var.set(name)
                
    def get_current_profile_data(self):
        points = []
        for pf in self.point_frames:
            try:
                x = int(pf.data['x'].get())
                y = int(pf.data['y'].get())
                delay = float(pf.data['delay'].get())
                interval = float(pf.data['interval'].get())
                btn = pf.data['button'].get()
                ctype = pf.data['type'].get()
                points.append(ClickPoint(x, y, interval, btn, ctype, delay))
            except ValueError:
                logger.error("Input tidak valid pada form titik klik.")
                # Tampilkan error sederhana
                self.lbl_status.configure(text="Error: Input Angka Tidak Valid", text_color="red")
                self.after(3000, lambda: self.lbl_status.configure(text="Status: IDLE", text_color="gray"))
                return None
                
        try:
            loop_cnt = int(self.entry_loop_count.get())
        except ValueError:
            loop_cnt = 1
            
        return Profile(self.current_profile_name, points, self.loop_var.get(), loop_cnt)

    # --- Point UI Management ---
    def add_point_ui(self, x=0, y=0, interval=1.0, button="left", click_type="single", delay_awal=0.0):
        frame = ctk.CTkFrame(self.scrollable_points)
        frame.pack(fill="x", padx=5, pady=5)
        
        idx = len(self.point_frames) + 1
        ctk.CTkLabel(frame, text=f"#{idx}", width=30).pack(side="left", padx=5)
        
        # Koordinat
        ctk.CTkLabel(frame, text="X:").pack(side="left", padx=2)
        entry_x = ctk.CTkEntry(frame, width=55)
        entry_x.insert(0, str(x))
        entry_x.pack(side="left", padx=2)
        
        ctk.CTkLabel(frame, text="Y:").pack(side="left", padx=2)
        entry_y = ctk.CTkEntry(frame, width=55)
        entry_y.insert(0, str(y))
        entry_y.pack(side="left", padx=2)
        
        # Timing
        ctk.CTkLabel(frame, text="Delay(s):").pack(side="left", padx=(10, 2))
        entry_delay = ctk.CTkEntry(frame, width=45)
        entry_delay.insert(0, str(delay_awal))
        entry_delay.pack(side="left", padx=2)
        
        ctk.CTkLabel(frame, text="Interval(s):").pack(side="left", padx=(10, 2))
        entry_interval = ctk.CTkEntry(frame, width=45)
        entry_interval.insert(0, str(interval))
        entry_interval.pack(side="left", padx=2)
        
        # Actions
        btn_var = ctk.StringVar(value=button)
        ctk.CTkOptionMenu(frame, values=["left", "right", "middle"], variable=btn_var, width=80).pack(side="left", padx=(10, 5))
        
        type_var = ctk.StringVar(value=click_type)
        ctk.CTkOptionMenu(frame, values=["single", "double"], variable=type_var, width=80).pack(side="left", padx=5)
        
        # Delete Button
        btn_del = ctk.CTkButton(frame, text="X", width=30, fg_color="#dc3545", hover_color="#c82333", 
                                command=lambda f=frame: self.remove_point_ui(f))
        btn_del.pack(side="right", padx=10)
        
        # Simpan referensi input ke dalam dictionary di frame object
        frame.data = {
            'x': entry_x, 'y': entry_y, 'delay': entry_delay, 
            'interval': entry_interval, 'button': btn_var, 'type': type_var
        }
        
        self.point_frames.append(frame)
        self._update_point_labels()
        
    def remove_point_ui(self, frame):
        frame.destroy()
        self.point_frames.remove(frame)
        self._update_point_labels()
        
    def _update_point_labels(self):
        """Update nomor urut setelah penghapusan."""
        for i, frame in enumerate(self.point_frames):
            # Mencari widget label pertama yang merupakan nomor urutan
            for widget in frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and widget.cget("text").startswith("#"):
                    widget.configure(text=f"#{i+1}")
                    break

    # --- Engine Controls ---
    def toggle_clicking(self):
        if not self.scheduler.running:
            prof = self.get_current_profile_data()
            if not prof or not prof.points:
                self.lbl_status.configure(text="Peringatan: Tidak ada titik klik!", text_color="orange")
                self.after(3000, lambda: self.lbl_status.configure(text="Status: IDLE", text_color="gray"))
                return
            
            # Update UI
            self.lbl_status.configure(text="Status: RUNNING", text_color="#28a745")
            self.btn_start.configure(text="BERHENTI (F6)", fg_color="#dc3545", hover_color="#c82333")
            self.btn_pause.configure(state="normal")
            
            # Start Scheduler
            self.scheduler.start(prof, self.on_scheduler_stop)
        else:
            self.scheduler.stop()
            self.on_scheduler_stop()
            
    def toggle_pause(self):
        if self.scheduler.running:
            is_paused = self.scheduler.pause_resume()
            if is_paused:
                self.lbl_status.configure(text="Status: DIPAUSE", text_color="#ffc107")
                self.btn_pause.configure(text="LANJUTKAN (F7)")
            else:
                self.lbl_status.configure(text="Status: RUNNING", text_color="#28a745")
                self.btn_pause.configure(text="PAUSE (F7)")
                
    def on_scheduler_stop(self):
        # Karena dipanggil dari thread, pindahkan ke main thread (Tkinter mainloop)
        self.after(0, self._update_ui_on_stop)
        
    def _update_ui_on_stop(self):
        self.lbl_status.configure(text="Status: IDLE", text_color="gray")
        self.btn_start.configure(text="MULAI (F6)", fg_color="#28a745", hover_color="#218838")
        self.btn_pause.configure(text="PAUSE (F7)", state="disabled", fg_color="#ffc107")

    # --- Grab Coordinate Mode ---
    def toggle_grab_mode(self):
        self.grabbing_mode = not self.grabbing_mode
        if self.grabbing_mode:
            self.btn_grab_point.configure(text="Menunggu F8...", fg_color="orange", hover_color="darkorange")
            self.lbl_status.configure(text="Tekan F8 di posisi yg diinginkan", text_color="orange")
        else:
            self.btn_grab_point.configure(text="Ambil Kordinat (F8)", fg_color="#D35B58", hover_color="#C75050")
            self.lbl_status.configure(text="Status: IDLE", text_color="gray")

    def handle_grab(self):
        if self.grabbing_mode:
            x, y = pyautogui.position()
            # Harus lewat `after` agar sinkron dengan main thread GUI
            self.after(0, lambda: self.add_point_ui(x, y))
            self.grabbing_mode = False
            self.after(0, lambda: self.btn_grab_point.configure(text="Ambil Kordinat (F8)", fg_color="#D35B58"))
            self.after(0, lambda: self.lbl_status.configure(text="Kordinat berhasil diambil!", text_color="green"))
            self.after(2000, lambda: self.lbl_status.configure(text="Status: IDLE", text_color="gray"))

    def close_event(self):
        """Menutup aplikasi dengan aman, mematikan thread & listener."""
        self.scheduler.stop()
        self.hotkey_manager.stop_listening()
        self.destroy()
