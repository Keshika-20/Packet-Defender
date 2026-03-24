import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import re
import firewall

COLORS = {
    "bg_dark":      "#0d1117",
    "bg_panel":     "#161b22",
    "bg_card":      "#21262d",
    "accent_blue":  "#1f6feb",
    "accent_green": "#238636",
    "accent_red":   "#da3633",
    "accent_orange":"#d29922",
    "text_primary": "#e6edf3",
    "text_muted":   "#8b949e",
    "border":       "#30363d",
    "allowed":      "#3fb950",
    "blocked":      "#f85149",
    "btn_hover":    "#388bfd",
}
CURRENT_ROLE=None
FONT_TITLE  = ("Courier New", 22, "bold")
FONT_HEADER = ("Courier New", 13, "bold")
FONT_BODY   = ("Courier New", 11)
FONT_MONO   = ("Courier New", 10)
FONT_SMALL  = ("Courier New", 9)




def styled_button(parent, text, command, color=None, width=22):
    """Create a consistently styled button."""
    bg = color or COLORS["accent_blue"]
    btn = tk.Button(
        parent, text=text, command=command,
        bg=bg, fg=COLORS["text_primary"],
        font=FONT_BODY, relief="flat", bd=0,
        activebackground=COLORS["btn_hover"],
        activeforeground="white",
        padx=10, pady=6, cursor="hand2", width=width,
    )
    return btn


def section_label(parent, text):
    """A bold section header label."""
    return tk.Label(
        parent, text=text,
        bg=COLORS["bg_panel"], fg=COLORS["text_primary"],
        font=FONT_HEADER,
    )


def entry_field(parent, width=28):
    """A styled entry field."""
    return tk.Entry(
        parent, width=width,
        bg=COLORS["bg_card"], fg=COLORS["text_primary"],
        insertbackground=COLORS["text_primary"],
        font=FONT_BODY, relief="flat", bd=4,
    )


def info_box(parent, height=6, width=55):
    """A read-only scrolled text box for output."""
    box = scrolledtext.ScrolledText(
        parent, height=height, width=width,
        bg=COLORS["bg_card"], fg=COLORS["text_primary"],
        font=FONT_MONO, relief="flat", bd=4,
        state="disabled", wrap="word",
    )
    return box


def write_to_box(box, text, color=None):
    """Write text to a read-only scrolled text box."""
    box.config(state="normal")
    box.delete("1.0", tk.END)
    box.insert(tk.END, text)
    if color:
        box.config(fg=color)
    box.config(state="disabled")



class RoleSelectionScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Packet Defender – Firewall System")
        self.root.geometry("540x400")
        self.root.configure(bg=COLORS["bg_dark"])
        self.root.resizable(False, False)
        self._build()

    def _build(self):
        # Title
        tk.Label(
            self.root, text="Packet Defender",
            bg=COLORS["bg_dark"], fg=COLORS["accent_blue"],
            font=FONT_TITLE,
        ).pack(pady=(50, 4))

        tk.Label(
            self.root, text="Network Firewall Control System",
            bg=COLORS["bg_dark"], fg=COLORS["text_muted"],
            font=FONT_BODY,
        ).pack(pady=(0, 40))

        tk.Label(
            self.root, text="Select your role to continue:",
            bg=COLORS["bg_dark"], fg=COLORS["text_primary"],
            font=FONT_HEADER,
        ).pack(pady=(0, 20))

        btn_frame = tk.Frame(self.root, bg=COLORS["bg_dark"])
        btn_frame.pack()

        styled_button(
            btn_frame, "🔐  Administrator", self._open_admin_login,
            color=COLORS["accent_blue"], width=24,
        ).grid(row=0, column=0, padx=15, pady=8)

        styled_button(
            btn_frame, "👤  User", self._open_user_panel,
            color=COLORS["accent_green"], width=24,
        ).grid(row=0, column=1, padx=15, pady=8)

        tk.Label(
            self.root,
            text="Admin requires authentication  |  User access is open",
            bg=COLORS["bg_dark"], fg=COLORS["text_muted"],
            font=FONT_SMALL,
        ).pack(pady=(20, 0))

    def _open_admin_login(self):
        global CURRENT_ROLE
        CURRENT_ROLE = "ADMIN"
        self.root.withdraw()
        AdminLoginWindow(self.root)

    def _open_user_panel(self):
        global CURRENT_ROLE
        CURRENT_ROLE = "USER"
        self.root.withdraw()
        UserPanelWindow(self.root)


def is_valid_ip(ip):
    pattern = r"^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\." \
              r"(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\." \
              r"(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\." \
              r"(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$"
    return re.match(pattern, ip) is not None

class AdminLoginWindow:
    def __init__(self, parent):
        self.parent = parent
        self.win = tk.Toplevel(parent)
        self.win.title("Admin Login")
        self.win.geometry("420x320")
        self.win.configure(bg=COLORS["bg_dark"])
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW", self._go_back)
        self._build()

    def _build(self):
        tk.Label(
            self.win, text="🔐 Administrator Login",
            bg=COLORS["bg_dark"], fg=COLORS["accent_blue"],
            font=FONT_HEADER,
        ).pack(pady=(30, 20))

        form = tk.Frame(self.win, bg=COLORS["bg_dark"])
        form.pack(pady=10)

        tk.Label(form, text="Username:", bg=COLORS["bg_dark"],
                 fg=COLORS["text_primary"], font=FONT_BODY).grid(row=0, column=0, sticky="e", pady=8, padx=8)
        self.username_entry = entry_field(form, width=22)
        self.username_entry.grid(row=0, column=1, pady=8)

        tk.Label(form, text="Password:", bg=COLORS["bg_dark"],
                 fg=COLORS["text_primary"], font=FONT_BODY).grid(row=1, column=0, sticky="e", pady=8, padx=8)
        self.password_entry = entry_field(form, width=22)
        self.password_entry.config(show="●")
        self.password_entry.grid(row=1, column=1, pady=8)

        self.error_label = tk.Label(
            self.win, text="", bg=COLORS["bg_dark"],
            fg=COLORS["accent_red"], font=FONT_SMALL,
        )
        self.error_label.pack()

        btn_frame = tk.Frame(self.win, bg=COLORS["bg_dark"])
        btn_frame.pack(pady=16)

        styled_button(btn_frame, "Login", self._attempt_login,
                      color=COLORS["accent_blue"], width=14).grid(row=0, column=0, padx=8)
        styled_button(btn_frame, "← Back", self._go_back,
                      color=COLORS["bg_card"], width=14).grid(row=0, column=1, padx=8)

        self.win.bind("<Return>", lambda e: self._attempt_login())

    def _attempt_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if firewall.admin_login(username, password):
            self.win.destroy()
            AdminPanelWindow(self.parent)
        else:
            self.error_label.config(text="❌ Invalid credentials. Try again.")

    def _go_back(self):
        self.win.destroy()
        self.parent.deiconify()



class AdminPanelWindow:
    def __init__(self, parent):
        self.parent = parent
        self.win = tk.Toplevel(parent)
        self.win.title("Packet Defender – Admin Panel")
        self.win.geometry("700x620")
        self.win.configure(bg=COLORS["bg_dark"])
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW", self._go_back)
        self._build()

    def _build(self):
        # ── Header ──
        hdr = tk.Frame(self.win, bg=COLORS["bg_panel"], pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🔐  ADMINISTRATOR PANEL",
                 bg=COLORS["bg_panel"], fg=COLORS["accent_blue"],
                 font=FONT_HEADER).pack()

        # ── Main content ──
        content = tk.Frame(self.win, bg=COLORS["bg_dark"])
        content.pack(fill="both", expand=True, padx=20, pady=12)

        left = tk.Frame(content, bg=COLORS["bg_panel"], padx=16, pady=14,
                        relief="flat", bd=1)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        right = tk.Frame(content, bg=COLORS["bg_panel"], padx=16, pady=14,
                         relief="flat", bd=1)
        right.grid(row=0, column=1, sticky="nsew")

        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)

        # ── Left: IP Management ──
        section_label(left, "🌐 IP Management").pack(anchor="w", pady=(0, 10))

        tk.Label(left, text="IP Address:", bg=COLORS["bg_panel"],
                 fg=COLORS["text_muted"], font=FONT_SMALL).pack(anchor="w")
        self.ip_entry = entry_field(left, width=26)
        self.ip_entry.pack(anchor="w", pady=(2, 10))

        styled_button(left, "✅  Add to Whitelist",
                      self._add_whitelist, color=COLORS["accent_green"], width=22).pack(pady=3, anchor="w")
        styled_button(left, "🗑  Remove from Whitelist",
                      self._remove_whitelist, color=COLORS["bg_card"], width=22).pack(pady=3, anchor="w")
        styled_button(left, "🚫  Add to Blacklist",
                      self._add_blacklist, color=COLORS["accent_red"], width=22).pack(pady=3, anchor="w")
        styled_button(left, "🗑  Remove from Blacklist",
                      self._remove_blacklist, color=COLORS["bg_card"], width=22).pack(pady=3, anchor="w")

        # ── Right: Protocol Management ──
        section_label(right, "🔌 Protocol Control").pack(anchor="w", pady=(0, 10))

        self.http_var = tk.BooleanVar(value=firewall.protocol_rules["HTTP"])
        self.ftp_var  = tk.BooleanVar(value=firewall.protocol_rules["FTP"])

        proto_frame = tk.Frame(right, bg=COLORS["bg_panel"])
        proto_frame.pack(anchor="w", pady=4)

        tk.Checkbutton(
            proto_frame, text="HTTP", variable=self.http_var,
            command=lambda: self._toggle_protocol("HTTP", self.http_var.get()),
            bg=COLORS["bg_panel"], fg=COLORS["text_primary"],
            selectcolor=COLORS["bg_card"], activebackground=COLORS["bg_panel"],
            font=FONT_BODY,
        ).grid(row=0, column=0, padx=8)

        tk.Checkbutton(
            proto_frame, text="FTP", variable=self.ftp_var,
            command=lambda: self._toggle_protocol("FTP", self.ftp_var.get()),
            bg=COLORS["bg_panel"], fg=COLORS["text_primary"],
            selectcolor=COLORS["bg_card"], activebackground=COLORS["bg_panel"],
            font=FONT_BODY,
        ).grid(row=0, column=1, padx=8)

        section_label(right, "📊 System Actions").pack(anchor="w", pady=(20, 10))

        styled_button(right, "📋  View Summary",
                      self._view_summary, color=COLORS["accent_orange"], width=22).pack(pady=3, anchor="w")
        styled_button(right, "🖨  Print to Terminal",
                      self._print_terminal, color=COLORS["bg_card"], width=22).pack(pady=3, anchor="w")

        # ── Output Box ──
        out_frame = tk.Frame(self.win, bg=COLORS["bg_dark"])
        out_frame.pack(fill="x", padx=20, pady=(0, 10))
        tk.Label(out_frame, text="Output:", bg=COLORS["bg_dark"],
                 fg=COLORS["text_muted"], font=FONT_SMALL).pack(anchor="w")
        self.output_box = info_box(out_frame, height=7, width=80)
        self.output_box.pack(fill="x")

        # ── Footer ──
        footer = tk.Frame(self.win, bg=COLORS["bg_panel"], pady=8)
        footer.pack(fill="x", side="bottom")
        styled_button(footer, "← Back to Role Selection",
                      self._go_back, color=COLORS["bg_card"], width=26).pack()

    def _add_whitelist(self):
        ip = self.ip_entry.get().strip()

        if not is_valid_ip(ip):
            write_to_box(self.output_box, "❌ Invalid IP format!", COLORS["blocked"])
            return

        msg = firewall.add_to_whitelist(ip)
        write_to_box(self.output_box, msg,
                    COLORS["allowed"] if "SUCCESS" in msg else COLORS["blocked"])

    def _remove_whitelist(self):
        ip = self.ip_entry.get().strip()

        if not is_valid_ip(ip):
            write_to_box(self.output_box, "❌ Invalid IP format!", COLORS["blocked"])
            return

        msg = firewall.remove_from_whitelist(ip)
        write_to_box(self.output_box, msg, COLORS["text_primary"])

    def _add_blacklist(self):
        ip = self.ip_entry.get().strip()

        if not is_valid_ip(ip):
            write_to_box(self.output_box, "❌ Invalid IP format!", COLORS["blocked"])
            return

        msg = firewall.add_to_blacklist(ip)
        write_to_box(self.output_box, msg,
                    COLORS["blocked"] if "SUCCESS" in msg else COLORS["accent_orange"])

    def _remove_blacklist(self):
        ip = self.ip_entry.get().strip()

        if not is_valid_ip(ip):
            write_to_box(self.output_box, "❌ Invalid IP format!", COLORS["blocked"])
            return

        msg = firewall.remove_from_blacklist(ip)
        write_to_box(self.output_box, msg, COLORS["text_primary"])

    def _toggle_protocol(self, proto, enabled):
        msg = firewall.set_protocol(proto, enabled)
        write_to_box(self.output_box, msg,
                     COLORS["allowed"] if enabled else COLORS["blocked"])

    def _view_summary(self):
        SummaryWindow(self.win)

    def _print_terminal(self):
        summary = firewall.get_summary()
        print(summary)
        write_to_box(self.output_box, "✅ Summary printed to terminal.", COLORS["allowed"])

    def _go_back(self):
        self.win.destroy()
        self.parent.deiconify()


class UserPanelWindow:
    def __init__(self, parent):
        self.parent = parent
        self.win = tk.Toplevel(parent)
        self.win.title("Packet Defender – User Panel")
        self.win.geometry("560x540")
        self.win.configure(bg=COLORS["bg_dark"])
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW", self._go_back)
        self._build()

    def _build(self):
        # ── Header ──
        hdr = tk.Frame(self.win, bg=COLORS["bg_panel"], pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="👤  USER PANEL",
                 bg=COLORS["bg_panel"], fg=COLORS["accent_green"],
                 font=FONT_HEADER).pack()

        # ── Form ──
        form = tk.Frame(self.win, bg=COLORS["bg_dark"], padx=30, pady=20)
        form.pack(fill="x")

        tk.Label(form, text="IP Address:", bg=COLORS["bg_dark"],
                 fg=COLORS["text_primary"], font=FONT_BODY).pack(anchor="w")
        self.ip_entry = entry_field(form, width=40)
        self.ip_entry.pack(anchor="w", pady=(4, 14))

        tk.Label(form, text="Protocol:", bg=COLORS["bg_dark"],
                 fg=COLORS["text_primary"], font=FONT_BODY).pack(anchor="w")

        self.protocol_var = tk.StringVar(value="HTTP")
        proto_frame = tk.Frame(form, bg=COLORS["bg_dark"])
        proto_frame.pack(anchor="w", pady=(4, 16))

        for proto in ["HTTP", "FTP"]:
            tk.Radiobutton(
                proto_frame, text=proto, variable=self.protocol_var, value=proto,
                bg=COLORS["bg_dark"], fg=COLORS["text_primary"],
                selectcolor=COLORS["bg_card"], activebackground=COLORS["bg_dark"],
                font=FONT_BODY,
            ).pack(side="left", padx=10)

        styled_button(form, "🚀  Send Request",
                      self._send_request, color=COLORS["accent_blue"], width=26).pack(pady=4)

        # ── Result Display ──
        result_frame = tk.Frame(self.win, bg=COLORS["bg_dark"], padx=30, pady=10)
        result_frame.pack(fill="x")

        tk.Label(result_frame, text="Result:", bg=COLORS["bg_dark"],
                 fg=COLORS["text_muted"], font=FONT_SMALL).pack(anchor="w")

        self.result_label = tk.Label(
            result_frame, text="—",
            bg=COLORS["bg_card"], fg=COLORS["text_primary"],
            font=("Courier New", 18, "bold"),
            width=30, pady=14, relief="flat",
        )
        self.result_label.pack(pady=(4, 0))

        self.reason_label = tk.Label(
            result_frame, text="",
            bg=COLORS["bg_dark"], fg=COLORS["text_muted"],
            font=FONT_SMALL, wraplength=460,
        )
        self.reason_label.pack(pady=(6, 0))

        # ── Recent Requests ──
        log_frame = tk.Frame(self.win, bg=COLORS["bg_dark"], padx=30, pady=10)
        log_frame.pack(fill="both", expand=True)

        tk.Label(log_frame, text="Recent Requests:", bg=COLORS["bg_dark"],
                 fg=COLORS["text_muted"], font=FONT_SMALL).pack(anchor="w")
        self.log_box = info_box(log_frame, height=7, width=68)
        self.log_box.pack(fill="x")

        # ── Footer ──
        footer = tk.Frame(self.win, bg=COLORS["bg_panel"], pady=8)
        footer.pack(fill="x", side="bottom")
        btn_row = tk.Frame(footer, bg=COLORS["bg_panel"])
        btn_row.pack()
        styled_button(btn_row, "📋  View Summary", lambda: SummaryWindow(self.win),
                      color=COLORS["accent_orange"], width=18).grid(row=0, column=0, padx=8)
        styled_button(btn_row, "← Back", self._go_back,
                      color=COLORS["bg_card"], width=18).grid(row=0, column=1, padx=8)

    def _send_request(self):
        ip = self.ip_entry.get().strip()
        protocol = self.protocol_var.get()

        if not ip:
            messagebox.showwarning("Input Required", "Please enter an IP address.")
            return

        if not is_valid_ip(ip):
            messagebox.showerror("Invalid IP", "❌ Invalid IP format!\nExample: 192.168.1.1")
            return

        result = firewall.check_request(ip, protocol)
        verdict = result["result"]
        reason  = result["reason"]

        if verdict == "ALLOWED":
            self.result_label.config(text="✅  ALLOWED", fg=COLORS["allowed"],
                                     bg=COLORS["bg_card"])
        else:
            self.result_label.config(text="🚫  BLOCKED", fg=COLORS["blocked"],
                                     bg=COLORS["bg_card"])

        self.reason_label.config(text=f"Reason: {reason}")
        self._refresh_log()

    def _refresh_log(self):
        entries = firewall.get_log_entries()
        user_entries = [e for e in entries if e["actor"] == "USER"][-8:]
        lines = []
        for e in reversed(user_entries):
            icon = "✅" if e["result"] == "ALLOWED" else "🚫"
            lines.append(
                f"{icon} [{e['timestamp']}]  {e['ip']:15s}  {e['protocol']:4s}  "
                f"{e['result']:7s}  {e['reason']}"
            )
        write_to_box(self.log_box, "\n".join(lines) if lines else "(no requests yet)")

    def _go_back(self):
        self.win.destroy()
        self.parent.deiconify()



class SummaryWindow:
    def __init__(self, parent):
        self.win = tk.Toplevel(parent)
        self.win.title("Packet Defender – System Summary")
        self.win.geometry("780x540")
        self.win.configure(bg=COLORS["bg_dark"])
        self.win.resizable(True, True)
        self._build()

    def _build(self):
        tk.Label(
            self.win, text="📊  FIREWALL SYSTEM SUMMARY",
            bg=COLORS["bg_dark"], fg=COLORS["accent_orange"],
            font=FONT_HEADER,
        ).pack(pady=(14, 8))

        txt = scrolledtext.ScrolledText(
            self.win, font=FONT_MONO,
            bg=COLORS["bg_card"], fg=COLORS["text_primary"],
            relief="flat", bd=8, wrap="none",
        )
        txt.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        summary = firewall.get_summary()
        txt.insert(tk.END, summary)
        txt.config(state="disabled")

        styled_button(self.win, "🖨  Print to Terminal",
                      lambda: (print(summary), None),
                      color=COLORS["bg_card"], width=22).pack(pady=(0, 12))


def main():
    global CURRENT_ROLE

    print("\n Packet Defender Firewall System starting...")

    firewall.load_data()

    root = tk.Tk()
    RoleSelectionScreen(root)

    def on_exit():

        if CURRENT_ROLE == "USER":
            print(firewall.get_user_session_summary())
        else:
            print("\n--- ADMIN SUMMARY ---")
            print(firewall.get_summary())

        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_exit)

    root.mainloop()
if __name__ == "__main__":
    main()