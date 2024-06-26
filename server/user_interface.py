import tkinter as tk
from tkinter import ttk
from signals import Signals

class UserInterface(tk.Tk):
    SERVER_STATE_STARTING = "Starting"
    SERVER_STATE_STOPPING = "Stopping"
    SERVER_STATE_RUNNING = "Running"
    SERVER_STATE_NOT_RUNNING = "Not Running"
    
    def __init__(self):
        super().__init__()
        self.log_box_signal = Signals(str)
        self.start_stop_signal = Signals(bool)
        self.server_state_signal = Signals(str)
        self._server_state = self.SERVER_STATE_NOT_RUNNING
        
        self.setup_ui()
        
    def setup_ui(self):
        self.title("Auto Writer Server")
        self.iconbitmap(r"public/icon.ico")
        self.geometry("800x400")
        
        self.style = ttk.Style(self)
        self.set_style()
        
        self.main_frame = ttk.Frame(self, padding="20")
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        
        self.setup_log_box()
        self.setup_start_stop_button()
        
        self.log_box_signal.connect(self.on_log_add)
        self.server_state_signal.connect(self.set_server_state)
        
    def set_style(self):
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#20232a')
        self.style.configure('TButton', font=('Helvetica', 14, 'bold'), padding=10, background='#FF5733', foreground='#20232a', borderwidth=0, focuscolor=self.style.configure(".")["background"])
        self.style.map('TButton', background=[('active', '#FF5733')], foreground=[('active', '#282c34')])
        self.style.configure('TLabel', background='#20232a', font=('Helvetica', 12), foreground='#FF5733')
        self.style.configure('TScrollbar', gripcount=0, background='#282c34', darkcolor='#20232a', lightcolor='#282c34', troughcolor='#20232a', bordercolor='#282c34', arrowcolor='#61dafb')

    def setup_log_box(self):
        log_frame = ttk.Frame(self.main_frame)
        log_frame.pack(expand=True, fill=tk.BOTH, pady=10)
        
        self.log_box = tk.Listbox(log_frame, font=('Helvetica', 12), selectbackground='#282c34', selectforeground='#FF5733', bg='#282c34', fg='#FF5733', bd=0, highlightthickness=0)
        self.log_box.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_box.yview, style="TScrollbar")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_box.config(yscrollcommand=scrollbar.set)
        
        x_scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.log_box.xview, style="TScrollbar")
        x_scrollbar.pack(fill=tk.X)
        self.log_box.config(xscrollcommand=x_scrollbar.set)
        
        self.log_box.bind("<Button-1>", lambda e: "break")
        self.log_box.bind("<B1-Motion>", lambda e: "break")
        self.log_box.bind("<Control-Button-1>", lambda e: "break")
        self.log_box.bind("<Shift-Button-1>", lambda e: "break")
        self.log_box.bind("<<ListboxSelect>>", lambda e: "break")
        
        self.log_box.insert(tk.END, "  Welcome to Auto Writer Server!")
        self.log_box.insert(tk.END, "  Server is Not Running.")
        self.log_box.insert(tk.END, "  Press Start Server Below to Start Server.")

    def setup_start_stop_button(self):
        self.start_stop_button = ttk.Button(self.main_frame, text="Start Server", style='TButton', command=self.on_start_stop_clicked)
        self.start_stop_button.pack(fill=tk.X, pady=(10, 0))

    def set_server_state(self, state: str):
        self._server_state = state
        if state == self.SERVER_STATE_STARTING:
            self.start_stop_button.configure(text="Starting Server", state=tk.DISABLED)
        elif state == self.SERVER_STATE_RUNNING:
            self.start_stop_button.configure(text="Stop Server", state=tk.ACTIVE)
        elif state == self.SERVER_STATE_STOPPING:
            self.start_stop_button.configure(text="Stopping Server", state=tk.DISABLED)
        elif state == self.SERVER_STATE_NOT_RUNNING:
            self.start_stop_button.configure(text="Start Server", state=tk.ACTIVE)
        
    def on_start_stop_clicked(self):
        if self._server_state in {self.SERVER_STATE_STARTING, self.SERVER_STATE_STOPPING}:
            return
        self.start_stop_button.configure(state=tk.DISABLED)
        if self._server_state == self.SERVER_STATE_NOT_RUNNING:
            self.start_stop_signal.emit(True)
        elif self._server_state == self.SERVER_STATE_RUNNING:
            self.start_stop_signal.emit(False)
    
    def on_log_add(self, log: str):
        self.log_box.insert(tk.END, f"  {log}")
        self.log_box.yview(tk.END)