import sys
from ui.main_window import MainWindow

def main():
    app = MainWindow()
    # Pastikan listener dan thread berhenti saat jendela di-close (X)
    app.protocol("WM_DELETE_WINDOW", app.close_event)
    app.mainloop()

if __name__ == "__main__":
    main()
