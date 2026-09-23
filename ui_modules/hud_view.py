import customtkinter as ctk

class HudView:
    def __init__(self, parent_frame, controller):
        self.parent = parent_frame
        self.controller = controller
        self.render()

    def render(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self.parent, text="SYSTEM COMMAND HUD", font=ctk.CTkFont(size=16, weight="bold"), text_color="#00ffcc")
        title.pack(anchor="w", padx=20, pady=20)

        self.console_output = ctk.CTkTextbox(self.parent, width=680, height=320, fg_color="#050507", font=("Consolas", 12))
        self.console_output.pack(padx=20, pady=10)
        
        self.console_output._textbox.tag_config("user", foreground="#ffffff")
        self.console_output._textbox.tag_config("karen", foreground="#00ffcc")
        self.console_output._textbox.tag_config("system", foreground="#88ccbb")

        input_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=10)

        self.cmd_entry = ctk.CTkEntry(input_frame, placeholder_text="Type command (e.g., 'open davinci resolve', 'memory')...", width=540, height=40)
        self.cmd_entry.pack(side="left", padx=(0, 10))
        self.cmd_entry.bind("<Return>", lambda event: self.controller.process_command())

        send_btn = ctk.CTkButton(input_frame, text="Execute", width=100, height=40, fg_color="#00ffcc", text_color="#000000", font=ctk.CTkFont(weight="bold"), command=self.controller.process_command)
        send_btn.pack(side="left")

    def get_entry_text(self):
        return self.cmd_entry.get()

    def clear_entry(self):
        self.cmd_entry.delete(0, "end")

    def append_log(self, text, tag="karen"):
        self.console_output.configure(state="normal")
        self.console_output._textbox.insert("end", f"{text}\n", tag)
        self.console_output.see("end")
        self.console_output.configure(state="disabled")