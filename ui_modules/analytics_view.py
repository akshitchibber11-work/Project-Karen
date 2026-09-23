import customtkinter as ctk
from actions.hardware_ops import HardwareOps
import threading

class AnalyticsView:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.render()

    def render(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        title = ctk.CTkLabel(self.parent, text="ANALYTICS & HARDWARE MONITOR", font=ctk.CTkFont(size=16, weight="bold"), text_color="#00ffcc")
        title.pack(anchor="w", padx=20, pady=20)
        self.stats_box = ctk.CTkTextbox(self.parent, width=680, height=340, fg_color="#050507", text_color="#00ffcc", font=("Consolas", 12))
        self.stats_box.pack(padx=20, pady=10)
        self.stats_box.insert("end", "Gathering live system analytics...")
        self.stats_box.configure(state="disabled")
        threading.Thread(target=self.live_loop, daemon=True).start()

    def live_loop(self):
        while True:
            try:
                stats_text = HardwareOps.get_system_stats() + "\n\n" + HardwareOps.get_top_memory_table()
                if hasattr(self, 'stats_box') and self.stats_box.winfo_exists():
                    self.stats_box.after(0, lambda t=stats_text: self.update_box(t))
            except Exception:
                break
            threading.Event().wait(2.0)

    def update_box(self, text):
        if self.stats_box.winfo_exists():
            self.stats_box.configure(state="normal")
            self.stats_box.delete("1.0", "end")
            self.stats_box.insert("end", text)
            self.stats_box.configure(state="disabled")
