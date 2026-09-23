import customtkinter as ctk

class TrackerView:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.render()

    def render(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        title = ctk.CTkLabel(self.parent, text="SELF-IMPROVEMENT & TASK TRACKER", font=ctk.CTkFont(size=16, weight="bold"), text_color="#00ffcc")
        title.pack(anchor="w", padx=20, pady=20)
        tracker_box = ctk.CTkTextbox(self.parent, width=680, height=340, fg_color="#050507", text_color="#ffffff", font=("Consolas", 13))
        tracker_box.pack(padx=20, pady=10)
        tracker_box.insert("end", "[Tracker Module Initialized]\n- Daily Calisthenics Routine: Pending\n- Code Commits (GitHub): Active\n- YouTube Content Pipeline: Standby")
        tracker_box.configure(state="disabled")
