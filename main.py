import customtkinter as ctk
from slangs import SlangNormalizer  # Add this import at the top of main.py
from karen_brain import KarenBrain
from actions.hardware_ops import HardwareOps
from actions.app_launcher import AppLauncher
from actions.os_ops import OSOps
from ui_modules.hud_view import HudView
from ui_modules.analytics_view import AnalyticsView
from ui_modules.tracker_view import TrackerView
import threading

class KarenMainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("KAREN // Modular OS")
        self.geometry("950x620")
        self.config(bg="#0a0a0c")
        
        self.brain = KarenBrain(model_name="phi4-mini")

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar Navigation
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#121218")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="KAREN", font=ctk.CTkFont(size=22, weight="bold"), text_color="#00ffcc")
        self.logo_label.pack(pady=30, padx=20)

        self.btn_hud = ctk.CTkButton(self.sidebar, text="Command HUD", fg_color="#1f538d", command=lambda: self.switch_tab("hud"))
        self.btn_hud.pack(pady=10, padx=20, fill="x")

        self.btn_analytics = ctk.CTkButton(self.sidebar, text="Analytics", fg_color="transparent", command=lambda: self.switch_tab("analytics"))
        self.btn_analytics.pack(pady=10, padx=20, fill="x")

        self.btn_tracker = ctk.CTkButton(self.sidebar, text="Trackers", fg_color="transparent", command=lambda: self.switch_tab("tracker"))
        self.btn_tracker.pack(pady=10, padx=20, fill="x")

        # Main Content Area
        self.content_frame = ctk.CTkFrame(self, fg_color="#0e0e12")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.current_hud = None
        self.switch_tab("hud")

    def switch_tab(self, tab_name):
        if tab_name == "hud":
            self.btn_hud.configure(fg_color="#1f538d")
            self.btn_analytics.configure(fg_color="transparent")
            self.btn_tracker.configure(fg_color="transparent")
            self.current_hud = HudView(self.content_frame, self)
            self.log_message("[System Initialized. Micro-Modular architecture active. Ready.]\n", "system")
        elif tab_name == "analytics":
            self.btn_analytics.configure(fg_color="#1f538d")
            self.btn_hud.configure(fg_color="transparent")
            self.btn_tracker.configure(fg_color="transparent")
            AnalyticsView(self.content_frame)
        elif tab_name == "tracker":
            self.btn_tracker.configure(fg_color="#1f538d")
            self.btn_hud.configure(fg_color="transparent")
            self.btn_analytics.configure(fg_color="transparent")
            TrackerView(self.content_frame)

    def log_message(self, text, tag="karen"):
        if threading.current_thread() is not threading.main_thread():
            self.after(0, lambda: self.log_message(text, tag))
            return
        if self.current_hud and hasattr(self.current_hud, 'append_log'):
            self.current_hud.append_log(text, tag)

    def process_command(self):
        if not self.current_hud:
            return
        command = self.current_hud.get_entry_text().strip()
        if not command:
            return
        
        self.log_message(f"User: {command}", "user")
        self.current_hud.clear_entry()

        threading.Thread(target=self.handle_execution, args=(command,), daemon=True).start()

    def handle_execution(self, command):
        # Normalize slang and broken inputs first
        normalized_cmd = SlangNormalizer.normalize(command)
        cmd_lower = normalized_cmd.lower()
        
        if cmd_lower.startswith("open "):
            app = cmd_lower.replace("open ", "", 1)
            res = AppLauncher.find_and_open_app(app)
            self.log_message(f"Karen: {res}", "karen")
        elif cmd_lower.startswith("close "):
            app = cmd_lower.replace("close ", "", 1)
            res = OSOps.close_application(app)
            self.log_message(f"Karen: {res}", "karen")
        elif "load file" in cmd_lower or "find file" in cmd_lower or "media" in cmd_lower:
            import re
            query_match = re.search(r'["\']([^"\']+)["\']', command)
            filename = query_match.group(1) if query_match else (cmd_lower.split("named")[-1].strip() if "named" in cmd_lower else "govtschool")
            res = AppLauncher.locate_downloaded_media(filename)
            self.log_message(f"Karen:\n{res}", "karen")
        elif "list files" in cmd_lower:
            res = OSOps.list_directory()
            self.log_message(f"Karen:\n{res}", "karen")
        elif "memory" in cmd_lower or "ram" in cmd_lower or "process" in cmd_lower:
            res = HardwareOps.get_top_memory_table()
            self.log_message(f"Karen:\n{res}", "karen")
        elif "stats" in cmd_lower or "diagnostic" in cmd_lower:
            res = HardwareOps.get_system_stats()
            self.log_message(f"Karen: {res}", "karen")
        else:
            self.log_message("Karen: Thinking...", "system")
            ai_response = self.brain.chat_offline(command)
            self.log_message(f"Karen: {ai_response}", "karen")

if __name__ == "__main__":
    app = KarenMainApp()
    app.mainloop()