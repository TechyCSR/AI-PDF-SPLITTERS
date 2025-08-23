#!/usr/bin/env python3
"""
AI PDF Splitter - Ultra-Modern 3D Professional GUI
Advanced UI/UX with 3D effects, gradients, and professional design
Cross-platform compatible for Windows and Linux
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import json
import time
from pathlib import Path
import queue
import webbrowser
import math

# Import our modules
from pdf_compressor import check_file_size, compress_pdf
from ai_processor import GeminiPDFProcessor
from pdf_splitter import PDFSplitter

class UltraModernAIApp:
    def __init__(self, root):
        self.root = root
        # Fixed medium size window
        self.root.geometry("900x700")
        self.root.resizable(False, False)  # Fixed size only
        
        # Modern window styling
        self.setup_window_properties()
        
        # Advanced color scheme and styling
        self.setup_advanced_styling()
        
        # Initialize variables
        self.selected_file = tk.StringVar()
        self.processing_queue = queue.Queue()
        self.processing = False
        self.output_directory = ""
        self.current_step = tk.StringVar(value="Ready to Process")
        self.progress_var = tk.DoubleVar()
        self.animation_frame = 0
        
        # Create modern GUI components
        self.create_modern_widgets()
        
        # Start processing thread and animations
        self.processing_thread = None
        self.processing = False
        
        # Start update loops
        self.root.after(50, self.update_processing_messages)
        self.root.after(100, self.animate_ui_elements)
    
    def setup_window_properties(self):
        """Setup modern window properties and behavior"""
        # Center window on screen
        self.center_window()
        
        # Set window properties for proper taskbar appearance
        self.root.configure(bg='#0a0a0a')
        self.root.resizable(False, False)  # Fixed size window
        
        # Ensure proper window management
        self.root.wm_attributes('-topmost', False)  # Don't stay on top
        
        # Set window class for proper taskbar grouping
        try:
            self.root.wm_class("AI PDF Splitter Pro", "AI PDF Splitter Pro")
        except:
            pass
        
        # Set window title and icon
        self.root.title("AI PDF Splitter Pro - Intelligent Document Processing Suite")
        
        # Bind window events
        self.root.bind('<Configure>', self.on_window_resize)
    
    def center_window(self):
        """Center window on screen with modern positioning"""
        self.root.update_idletasks()
        width = 900
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def on_window_resize(self, event):
        """Handle window resize events"""
        if event.widget == self.root:
            # Update responsive elements
            pass
    
    def setup_advanced_styling(self):
        """Setup techy cyber styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Techy cyber color palette  
        self.colors = {
            # Core backgrounds
            'bg_primary': '#0d1117',      # GitHub dark
            'bg_secondary': '#161b22',    # Panel background
            'bg_tertiary': '#21262d',     # Card background
            'bg_terminal': '#0a0e13',     # Terminal background
            
            # Accent colors
            'accent_cyan': '#00ffff',     # Bright cyan
            'accent_green': '#00ff41',    # Matrix green
            'accent_purple': '#7c3aed',   # Electric purple
            'accent_orange': '#ff6b35',   # Tech orange
            
            # Text colors
            'text_primary': '#f0f6fc',    # Bright white
            'text_secondary': '#8b949e',  # Muted gray
            'text_terminal': '#00ff41',   # Terminal green
            'text_accent': '#00ffff',     # Cyan accent
            
            # States
            'border': '#30363d',          # Subtle border
            'hover': '#262c36',           # Hover state
            'progress': '#00ffff',        # Progress cyan
            'success': '#00ff41',         # Success green
            'warning': '#ff6b35',         # Warning orange
            'error': '#ff4757',           # Error red
            'disabled': '#484f58',        # Disabled state
        }
        
        # Configure cyber progress bar style
        style.configure('Cyber.Horizontal.TProgressbar',
                       background=self.colors['progress'],
                       troughcolor=self.colors['bg_tertiary'],
                       borderwidth=0,
                       lightcolor=self.colors['progress'],
                       darkcolor=self.colors['progress'])
        
        # Configure ultra-modern styles
        self.configure_modern_styles(style)
    
    def configure_modern_styles(self, style):
        """Configure all modern UI styles"""
        # Modern title style
        style.configure('UltraTitle.TLabel',
                       font=('Inter', 32, 'bold'),
                       foreground=self.colors['text_primary'],
                       background=self.colors['bg_primary'])
        
        # Subtitle style
        style.configure('Subtitle.TLabel',
                       font=('Inter', 14),
                       foreground=self.colors['text_secondary'],
                       background=self.colors['bg_primary'])
        
        # Section headers
        style.configure('SectionHeader.TLabel',
                       font=('Inter', 16, 'bold'),
                       foreground=self.colors['accent_cyan'],
                       background=self.colors['bg_secondary'])
        
        # Modern buttons with 3D effect
        style.configure('Modern3D.TButton',
                       font=('Inter', 11, 'bold'),
                       foreground=self.colors['text_primary'],
                       background=self.colors['accent_cyan'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(25, 12))
        
        style.map('Modern3D.TButton',
                 background=[('active', self.colors['hover']),
                            ('pressed', self.colors['accent_purple'])])
        
        # Glass effect buttons
        style.configure('Glass.TButton',
                       font=('Inter', 10, 'bold'),
                       foreground=self.colors['text_primary'],
                       background=self.colors['bg_tertiary'],
                       borderwidth=1,
                       relief='flat',
                       padding=(20, 10))
        
        # Modern progress bar
        style.configure('Ultra.Horizontal.TProgressbar',
                       background=self.colors['accent_cyan'],
                       troughcolor=self.colors['bg_tertiary'],
                       borderwidth=0,
                       lightcolor=self.colors['accent_cyan'],
                       darkcolor=self.colors['accent_cyan'])
        
        # Modern entry fields
        style.configure('Modern.TEntry',
                       font=('Inter', 11),
                       foreground=self.colors['text_primary'],
                       background=self.colors['bg_tertiary'],
                       borderwidth=1,
                       insertcolor=self.colors['accent_cyan'])
        
        # Modern frame styles
        style.configure('Card.TFrame',
                       background=self.colors['bg_tertiary'],
                       borderwidth=1,
                       relief='flat')
        
        style.configure('Glass.TFrame',
                       background=self.colors['bg_tertiary'],
                       borderwidth=1,
                       relief='flat')
    
    def create_modern_widgets(self):
        """Create techy split-layout GUI with terminal and controls"""
        # Main container
        self.main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # Configure grid for split layout
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.rowconfigure(0, weight=0)  # Top area (file selector)
        self.main_container.rowconfigure(1, weight=1)  # Bottom area (terminal + results)
        
        # Create top file selector area
        self.create_file_selector_area()
        
        # Create bottom split area (terminal + results)
        self.create_split_terminal_area()
    
    def create_file_selector_area(self):
        """Create compact file selector area at top"""
        # File selector frame
        file_frame = tk.Frame(self.main_container, 
                             bg=self.colors['bg_secondary'],
                             relief='solid',
                             bd=1)
        file_frame.grid(row=0, column=0, sticky='ew', pady=(0, 4))
        file_frame.columnconfigure(1, weight=1)
        
        # Title label
        title_label = tk.Label(file_frame,
                              text="🚀 AI PDF SPLITTER PRO",
                              font=('Consolas', 14, 'bold'),
                              bg=self.colors['bg_secondary'],
                              fg=self.colors['accent_cyan'])
        title_label.grid(row=0, column=0, columnspan=3, pady=(8, 4))
        
        # File path display
        self.file_path_var = tk.StringVar(value="No file selected")
        file_display = tk.Label(file_frame,
                               textvariable=self.file_path_var,
                               font=('Consolas', 9),
                               bg=self.colors['bg_tertiary'],
                               fg=self.colors['text_secondary'],
                               relief='sunken',
                               bd=1,
                               anchor='w',
                               padx=8)
        file_display.grid(row=1, column=0, columnspan=2, sticky='ew', padx=8, pady=4)
        
        # Browse button
        self.browse_btn = tk.Button(file_frame,
                                   text="📁 BROWSE",
                                   font=('Consolas', 9, 'bold'),
                                   bg=self.colors['accent_purple'],
                                   fg=self.colors['text_primary'],
                                   activebackground=self.colors['hover'],
                                   relief='flat',
                                   bd=0,
                                   padx=15,
                                   command=self.browse_file)
        self.browse_btn.grid(row=1, column=2, padx=(4, 8), pady=4)
        
        # Progress and control row
        progress_frame = tk.Frame(file_frame, bg=self.colors['bg_secondary'])
        progress_frame.grid(row=2, column=0, columnspan=3, sticky='ew', padx=8, pady=(0, 8))
        progress_frame.columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame,
                                           variable=self.progress_var,
                                           maximum=100,
                                           style='Cyber.Horizontal.TProgressbar')
        self.progress_bar.grid(row=0, column=0, sticky='ew', padx=(0, 8))
        
        # Progress percentage label
        self.progress_label = tk.Label(progress_frame,
                                      text="0%",
                                      font=('Consolas', 9, 'bold'),
                                      bg=self.colors['bg_secondary'],
                                      fg=self.colors['accent_cyan'],
                                      width=5)
        self.progress_label.grid(row=0, column=1)
        
        # Process button
        self.process_btn = tk.Button(progress_frame,
                                    text="⚡ PROCESS",
                                    font=('Consolas', 10, 'bold'),
                                    bg=self.colors['accent_green'],
                                    fg=self.colors['bg_primary'],
                                    activebackground=self.colors['success'],
                                    relief='flat',
                                    bd=0,
                                    padx=15,
                                    state=tk.DISABLED,
                                    command=self.start_processing)
        self.process_btn.grid(row=0, column=2, padx=(8, 0))
    
    def create_split_terminal_area(self):
        """Create split area with terminal and results"""
        # Split container
        split_frame = tk.Frame(self.main_container, bg=self.colors['bg_primary'])
        split_frame.grid(row=1, column=0, sticky='nsew')
        split_frame.columnconfigure(0, weight=1)
        split_frame.columnconfigure(1, weight=1)
        split_frame.rowconfigure(0, weight=1)
        
        # Left panel - Terminal
        self.create_terminal_panel(split_frame)
        
        # Right panel - Results
        self.create_results_panel(split_frame)
    
    def create_terminal_panel(self, parent):
        """Create terminal-like processing display"""
        # Terminal frame
        terminal_frame = tk.Frame(parent,
                                 bg=self.colors['bg_terminal'],
                                 relief='solid',
                                 bd=1)
        terminal_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 2))
        
        # Terminal header
        term_header = tk.Frame(terminal_frame, bg=self.colors['bg_secondary'], height=25)
        term_header.pack(fill='x')
        term_header.pack_propagate(False)
        
        tk.Label(term_header,
                text="💻 PROCESSING TERMINAL",
                font=('Consolas', 10, 'bold'),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_terminal']).pack(pady=4)
        
        # Terminal text area
        term_container = tk.Frame(terminal_frame, bg=self.colors['bg_terminal'])
        term_container.pack(fill='both', expand=True, padx=4, pady=4)
        
        # Scrollable text widget
        self.terminal_text = tk.Text(term_container,
                                    bg=self.colors['bg_terminal'],
                                    fg=self.colors['text_terminal'],
                                    font=('Consolas', 9),
                                    relief='flat',
                                    bd=0,
                                    wrap='word',
                                    state='disabled')
        
        # Scrollbar for terminal
        terminal_scroll = tk.Scrollbar(term_container, orient='vertical', command=self.terminal_text.yview)
        self.terminal_text.configure(yscrollcommand=terminal_scroll.set)
        
        self.terminal_text.pack(side='left', fill='both', expand=True)
        terminal_scroll.pack(side='right', fill='y')
        
        # Add initial terminal prompt
        self.terminal_print("🚀 AI PDF Splitter Pro v2.0")
        self.terminal_print("💡 Ready to process PDF files...")
        self.terminal_print("📋 Select a PDF file to begin")
        self.terminal_print("-" * 40)
    
    def create_results_panel(self, parent):
        """Create results display panel"""
        # Results frame
        results_frame = tk.Frame(parent,
                                bg=self.colors['bg_secondary'],
                                relief='solid',
                                bd=1)
        results_frame.grid(row=0, column=1, sticky='nsew', padx=(2, 0))
        
        # Results header
        results_header = tk.Frame(results_frame, bg=self.colors['bg_tertiary'], height=25)
        results_header.pack(fill='x')
        results_header.pack_propagate(False)
        
        tk.Label(results_header,
                text="📊 RESULTS & OUTPUT",
                font=('Consolas', 10, 'bold'),
                bg=self.colors['bg_tertiary'],
                fg=self.colors['accent_orange']).pack(pady=4)
        
        # Results content
        results_content = tk.Frame(results_frame, bg=self.colors['bg_secondary'])
        results_content.pack(fill='both', expand=True, padx=8, pady=8)
        
        # File info section
        info_frame = tk.LabelFrame(results_content,
                                  text="📄 FILE INFO",
                                  font=('Consolas', 9, 'bold'),
                                  bg=self.colors['bg_secondary'],
                                  fg=self.colors['text_accent'],
                                  relief='solid',
                                  bd=1)
        info_frame.pack(fill='x', pady=(0, 8))
        
        self.file_info_text = tk.Text(info_frame,
                                     height=6,
                                     bg=self.colors['bg_tertiary'],
                                     fg=self.colors['text_secondary'],
                                     font=('Consolas', 8),
                                     relief='flat',
                                     bd=0,
                                     state='disabled')
        self.file_info_text.pack(fill='x', padx=4, pady=4)
        
        # Status section
        status_frame = tk.LabelFrame(results_content,
                                    text="⚡ STATUS",
                                    font=('Consolas', 9, 'bold'),
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_accent'],
                                    relief='solid',
                                    bd=1)
        status_frame.pack(fill='x', pady=(0, 8))
        
        self.status_label = tk.Label(status_frame,
                                    text="Ready",
                                    font=('Consolas', 9),
                                    bg=self.colors['bg_tertiary'],
                                    fg=self.colors['text_secondary'],
                                    relief='sunken',
                                    bd=1,
                                    padx=8,
                                    pady=4)
        self.status_label.pack(fill='x', padx=4, pady=4)
        
        # Action buttons
        button_frame = tk.Frame(results_content, bg=self.colors['bg_secondary'])
        button_frame.pack(fill='x', side='bottom')
        
        self.open_output_btn = tk.Button(button_frame,
                                        text="📂 OPEN OUTPUT",
                                        font=('Consolas', 9, 'bold'),
                                        bg=self.colors['accent_orange'],
                                        fg=self.colors['text_primary'],
                                        relief='flat',
                                        bd=0,
                                        padx=10,
                                        state=tk.DISABLED,
                                        command=self.open_output_directory)
        self.open_output_btn.pack(side='left', padx=(0, 4))
        
        self.clear_btn = tk.Button(button_frame,
                                  text="🗑️ CLEAR",
                                  font=('Consolas', 9, 'bold'),
                                  bg=self.colors['error'],
                                  fg=self.colors['text_primary'],
                                  relief='flat',
                                  bd=0,
                                  padx=10,
                                  command=self.clear_all)
        self.clear_btn.pack(side='right')
    
    def terminal_print(self, message):
        """Print message to terminal with timestamp"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}\n"
        
        self.terminal_text.config(state='normal')
        self.terminal_text.insert('end', formatted_msg)
        self.terminal_text.see('end')
        self.terminal_text.config(state='disabled')
        self.root.update_idletasks()
    
    def update_progress_status(self, percentage, status_text):
        """Update progress bar and status"""
        self.progress_var.set(percentage)
        self.progress_label.config(text=f"{percentage}%")
        self.status_label.config(text=status_text)
        self.root.update_idletasks()
    
    def processing_complete(self, success):
        """Handle processing completion and reset UI to ready state"""
        self.processing = False
        
        if success:
            self.progress_var.set(100)
            self.progress_label.config(text="100%")
            self.status_label.config(text="✅ Complete")
            self.open_output_btn.config(state=tk.NORMAL)
            self.terminal_print("=" * 40)
            self.terminal_print("🎉 PROCESSING COMPLETED SUCCESSFULLY!")
            self.terminal_print("📁 Ready for new file processing!")
            self.terminal_print("=" * 40)
        else:
            self.status_label.config(text="❌ Failed")
            self.terminal_print("=" * 40)
            self.terminal_print("💥 PROCESSING FAILED!")
            self.terminal_print("🔄 Ready to try again or select new file!")
            self.terminal_print("=" * 40)
        
        # Always re-enable browse button
        self.browse_btn.config(state=tk.NORMAL)
        
        # Reset process button text and enable only if file is selected
        self.process_btn.config(text="⚡ PROCESS")
        if self.selected_file.get():
            self.process_btn.config(state=tk.NORMAL)
            self.terminal_print("✅ Ready to process again!")
        else:
            self.process_btn.config(state=tk.DISABLED)
            self.terminal_print("📁 Select a PDF file to continue")
    
    def clear_output(self):
        """Clear output displays"""
        self.status_label.config(text="Ready")
        self.progress_var.set(0)
        self.progress_label.config(text="0%")
        self.open_output_btn.config(state=tk.DISABLED)
    
    def clear_all(self):
        """Clear all data and reset interface"""
        if hasattr(self, 'processing') and self.processing:
            self.terminal_print("⚠️ Cannot clear while processing!")
            return
            
        self.selected_file.set("")
        self.file_path_var.set("No file selected")
        
        # Clear file info
        self.file_info_text.config(state='normal')
        self.file_info_text.delete(1.0, 'end')
        self.file_info_text.config(state='disabled')
        
        # Clear terminal
        self.terminal_text.config(state='normal')
        self.terminal_text.delete(1.0, 'end')
        self.terminal_text.config(state='disabled')
        
        # Add fresh terminal prompt
        self.terminal_print("🚀 AI PDF Splitter Pro v2.0")
        self.terminal_print("💡 Ready to process PDF files...")
        self.terminal_print("📋 Select a PDF file to begin")
        self.terminal_print("-" * 40)
        
        self.process_btn.config(state=tk.DISABLED, text="⚡ PROCESS")
        self.clear_output()
    
    def open_output_directory(self):
        """Open the output directory in file manager"""
        if hasattr(self, 'output_directory') and self.output_directory:
            import subprocess
            import platform
            try:
                if platform.system() == 'Windows':
                    subprocess.run(['explorer', self.output_directory])
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.run(['open', self.output_directory])
                else:  # Linux
                    subprocess.run(['xdg-open', self.output_directory])
                self.terminal_print(f"📂 Opened: {self.output_directory}")
            except Exception as e:
                self.terminal_print(f"❌ Could not open directory: {str(e)}")
        else:
            self.terminal_print("❌ No output directory available")

    def create_modern_header(self):
        """Create ultra-modern header with gradient effect"""
        header_frame = tk.Frame(self.main_container, 
                               bg=self.colors['bg_secondary'], 
                               height=100)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title container
        title_container = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        title_container.pack(expand=True, fill=tk.BOTH, padx=30, pady=20)
        
        # AI Icon and Title
        icon_title_frame = tk.Frame(title_container, bg=self.colors['bg_secondary'])
        icon_title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Modern AI Icon
        ai_icon = tk.Label(icon_title_frame, 
                          text="🚀", 
                          font=('Segoe UI Emoji', 32),
                          bg=self.colors['bg_secondary'],
                          fg=self.colors['accent_cyan'])
        ai_icon.pack(side=tk.LEFT, padx=(0, 15))
        
        # Title text
        title_text_frame = tk.Frame(icon_title_frame, bg=self.colors['bg_secondary'])
        title_text_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        main_title = tk.Label(title_text_frame,
                             text="AI PDF SPLITTER PRO",
                             font=('Inter', 24, 'bold'),
                             fg=self.colors['text_primary'],
                             bg=self.colors['bg_secondary'])
        main_title.pack(anchor=tk.W)
        
        subtitle = tk.Label(title_text_frame,
                           text="Advanced Document Intelligence • 3D Interface",
                           font=('Inter', 11),
                           fg=self.colors['text_secondary'],
                           bg=self.colors['bg_secondary'])
        subtitle.pack(anchor=tk.W)
        
        # Status indicator
        self.status_indicator = tk.Label(title_container,
                                        text="● READY",
                                        font=('Inter', 10, 'bold'),
                                        fg=self.colors['accent_green'],
                                        bg=self.colors['bg_secondary'])
        self.status_indicator.pack(side=tk.RIGHT, anchor=tk.E)
    
    def create_main_content_area(self):
        """Create main content area with modern card-based layout"""
        # Content frame with padding
        self.content_frame = tk.Frame(self.main_container, bg=self.colors['bg_primary'])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Create modern sections
        self.create_file_selection_card()
        self.create_processing_dashboard()
        self.create_results_panel()
    
    def create_file_selection_card(self):
        """Create modern file selection card with 3D effects"""
        # Main card container
        card_frame = self.create_glass_card(self.content_frame, "📁 File Selection")
        
        # File selection area
        file_area = tk.Frame(card_frame, bg=self.colors['bg_tertiary'])
        file_area.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Drag and drop area
        self.drop_area = tk.Frame(file_area, 
                                 bg=self.colors['bg_tertiary'],
                                 relief=tk.RAISED,
                                 bd=2,
                                 height=120)
        self.drop_area.pack(fill=tk.X, pady=(0, 15))
        self.drop_area.pack_propagate(False)
        
        # Drop area content
        drop_content = tk.Frame(self.drop_area, bg=self.colors['bg_tertiary'])
        drop_content.pack(expand=True)
        
        drop_icon = tk.Label(drop_content,
                           text="📎",
                           font=('Segoe UI Emoji', 24),
                           fg=self.colors['accent_cyan'],
                           bg=self.colors['bg_tertiary'])
        drop_icon.pack(pady=(15, 5))
        
        drop_text = tk.Label(drop_content,
                           text="Drag & Drop PDF File Here or click Browse",
                           font=('Inter', 11),
                           fg=self.colors['text_secondary'],
                           bg=self.colors['bg_tertiary'])
        drop_text.pack()
        
        # File path display
        self.file_path_var = tk.StringVar(value="No file selected")
        path_label = tk.Label(file_area,
                             textvariable=self.file_path_var,
                             font=('Inter', 9),
                             fg=self.colors['text_secondary'],
                             bg=self.colors['bg_tertiary'],
                             anchor=tk.W)
        path_label.pack(fill=tk.X, pady=(0, 10))
        
        # File info frame
        self.file_info_frame = tk.Frame(file_area, bg=self.colors['bg_tertiary'])
        self.file_info_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Action buttons
        button_frame = tk.Frame(file_area, bg=self.colors['bg_tertiary'])
        button_frame.pack(fill=tk.X)
        
        # Browse button
        self.browse_btn = tk.Button(button_frame,
                                   text="🔍 Browse Files",
                                   font=('Inter', 10, 'bold'),
                                   fg=self.colors['text_primary'],
                                   bg=self.colors['accent_cyan'],
                                   activebackground=self.colors['accent_purple'],
                                   bd=0,
                                   pady=10,
                                   cursor='hand2',
                                   command=self.browse_file)
        self.browse_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Process button
        self.process_btn = tk.Button(button_frame,
                                    text="🚀 START PROCESSING",
                                    font=('Inter', 11, 'bold'),
                                    fg=self.colors['text_primary'],
                                    bg=self.colors['accent_green'],
                                    activebackground=self.colors['success'],
                                    bd=0,
                                    pady=12,
                                    cursor='hand2',
                                    state=tk.DISABLED,
                                    command=self.start_processing)
        self.process_btn.pack(side=tk.RIGHT)
    
    def create_processing_dashboard(self):
        """Create modern processing dashboard"""
        # Processing card
        card_frame = self.create_glass_card(self.content_frame, "⚙️ Processing Dashboard")
        
        # Progress section
        progress_area = tk.Frame(card_frame, bg=self.colors['bg_tertiary'])
        progress_area.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Progress bar with modern styling
        progress_container = tk.Frame(progress_area, bg=self.colors['bg_tertiary'])
        progress_container.pack(fill=tk.X, pady=(0, 10))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_container,
                                           variable=self.progress_var,
                                           maximum=100,
                                           style='Ultra.Horizontal.TProgressbar',
                                           length=400)
        self.progress_bar.pack(fill=tk.X)
        
        # Progress info
        progress_info = tk.Frame(progress_area, bg=self.colors['bg_tertiary'])
        progress_info.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_label = tk.Label(progress_info,
                                      text="0%",
                                      font=('Inter', 12, 'bold'),
                                      fg=self.colors['accent_cyan'],
                                      bg=self.colors['bg_tertiary'])
        self.progress_label.pack(side=tk.LEFT)
        
        self.step_label = tk.Label(progress_info,
                                  textvariable=self.current_step,
                                  font=('Inter', 10),
                                  fg=self.colors['text_secondary'],
                                  bg=self.colors['bg_tertiary'])
        self.step_label.pack(side=tk.RIGHT)
        
        # Messages area
        messages_label = tk.Label(progress_area,
                                 text="Processing Messages:",
                                 font=('Inter', 11, 'bold'),
                                 fg=self.colors['text_primary'],
                                 bg=self.colors['bg_tertiary'],
                                 anchor=tk.W)
        messages_label.pack(fill=tk.X, pady=(0, 5))
        
        # Messages text with modern scrollbar
        self.messages_text = scrolledtext.ScrolledText(progress_area,
                                                      height=8,
                                                      font=('Consolas', 9),
                                                      wrap=tk.WORD,
                                                      bg=self.colors['bg_tertiary'],
                                                      fg=self.colors['text_primary'],
                                                      insertbackground=self.colors['accent_cyan'],
                                                      selectbackground=self.colors['accent_cyan'],
                                                      selectforeground=self.colors['text_primary'])
        self.messages_text.pack(fill=tk.X)
    
    def create_glass_card(self, parent, title):
        """Create a glass-effect card with modern styling"""
        # Card container with shadow effect
        card_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        card_container.pack(fill=tk.X, pady=(0, 20))
        
        # Main card with modern styling
        card_frame = tk.Frame(card_container,
                             bg=self.colors['bg_tertiary'],
                             relief=tk.FLAT,
                             bd=1)
        card_frame.pack(fill=tk.X)
        
        # Card header
        header_frame = tk.Frame(card_frame, bg=self.colors['bg_secondary'], height=45)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Title with icon
        title_label = tk.Label(header_frame,
                              text=title,
                              font=('Inter', 13, 'bold'),
                              fg=self.colors['accent_cyan'],
                              bg=self.colors['bg_secondary'])
        title_label.pack(side=tk.LEFT, padx=20, pady=12)
        
        # Decorative accent line
        accent_line = tk.Frame(card_frame, bg=self.colors['accent_cyan'], height=2)
        accent_line.pack(fill=tk.X)
        
        return card_frame
    
    def create_modern_footer(self):
        """Create modern footer with status and controls"""
        footer_frame = tk.Frame(self.main_container, 
                               bg=self.colors['bg_secondary'], 
                               height=60)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        # Footer content
        footer_content = tk.Frame(footer_frame, bg=self.colors['bg_secondary'])
        footer_content.pack(expand=True, fill=tk.BOTH, padx=30, pady=15)
        
        # Status text
        self.status_label = tk.Label(footer_content,
                                    textvariable=self.current_step,
                                    font=('Inter', 10),
                                    fg=self.colors['text_secondary'],
                                    bg=self.colors['bg_secondary'])
        self.status_label.pack(side=tk.LEFT)
        
        # Exit button
        exit_btn = tk.Button(footer_content,
                            text="❌ Exit",
                            font=('Inter', 9, 'bold'),
                            fg=self.colors['text_primary'],
                            bg=self.colors['error'],
                            activebackground=self.colors['error'],
                            bd=0,
                            pady=8,
                            padx=15,
                            cursor='hand2',
                            command=self.root.quit)
        exit_btn.pack(side=tk.RIGHT)
    
    def animate_ui_elements(self):
        """Add subtle animations to UI elements"""
        self.animation_frame += 1
        
        # Animate status indicator
        if hasattr(self, 'status_indicator'):
            if self.processing:
                colors = [self.colors['accent_cyan'], self.colors['accent_purple'], self.colors['accent_green']]
                color_index = (self.animation_frame // 10) % len(colors)
                self.status_indicator.config(fg=colors[color_index])
                self.status_indicator.config(text="● PROCESSING")
            else:
                self.status_indicator.config(fg=self.colors['accent_green'])
                self.status_indicator.config(text="● READY")
        
        # Continue animation loop
        self.root.after(100, self.animate_ui_elements)
    
    def clear_selection(self):
        """Clear file selection"""
        self.selected_file.set("")
        self.file_path_var.set("No file selected")
        self.process_btn.config(state=tk.DISABLED)
        self.clear_file_info()
    
    def clear_file_info(self):
        """Clear file info display"""
        if hasattr(self, 'file_info_text'):
            self.file_info_text.config(state='normal')
            self.file_info_text.delete(1.0, 'end')
            self.file_info_text.config(state='disabled')
    
    def create_file_selection_section(self, parent, row):
        """Create file selection section"""
        # Section header
        file_header = ttk.Label(parent, text="📁 Select PDF File", style='Header.TLabel')
        file_header.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(20, 10))
        
        # File path display
        file_frame = ttk.Frame(parent)
        file_frame.grid(row=row+1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        file_frame.columnconfigure(1, weight=1)
        
        # Browse button
        browse_btn = ttk.Button(file_frame, 
                               text="Browse Files", 
                               style='Modern.TButton',
                               command=self.browse_file)
        browse_btn.grid(row=0, column=0, padx=(0, 10))
        
        # File path entry
        file_entry = ttk.Entry(file_frame, 
                              textvariable=self.selected_file, 
                              font=('Segoe UI', 10),
                              state='readonly')
        file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # File info
        self.file_info_label = ttk.Label(file_frame, 
                                        text="No file selected", 
                                        font=('Segoe UI', 9),
                                        foreground=self.colors['text_light'])
        self.file_info_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
    
    def create_processing_section(self, parent, row):
        """Create processing status section"""
        # Section header
        process_header = ttk.Label(parent, text="⚙️ Processing Status", style='Header.TLabel')
        process_header.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(20, 10))
        
        # Status frame
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=row+1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        status_frame.columnconfigure(1, weight=1)
        
        # Current step
        ttk.Label(status_frame, text="Current Step:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky=tk.W)
        self.step_label = ttk.Label(status_frame, 
                                   textvariable=self.current_step, 
                                   font=('Segoe UI', 10),
                                   foreground=self.colors['secondary'])
        self.step_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Processing messages
        ttk.Label(status_frame, text="Messages:", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        # Messages text area
        self.messages_text = scrolledtext.ScrolledText(status_frame, 
                                                      height=6, 
                                                      font=('Consolas', 9),
                                                      wrap=tk.WORD,
                                                      bg=self.colors['light_bg'])
        self.messages_text.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
    
    def create_progress_section(self, parent, row):
        """Create progress section"""
        # Section header
        progress_header = ttk.Label(parent, text="📊 Progress", style='Header.TLabel')
        progress_header.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(20, 10))
        
        # Progress frame
        progress_frame = ttk.Frame(parent)
        progress_frame.grid(row=row+1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        progress_frame.columnconfigure(1, weight=1)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_frame, 
                                           variable=self.progress_var,
                                           maximum=100,
                                           style='Progress.Horizontal.TProgressbar')
        self.progress_bar.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Progress percentage
        self.progress_label = ttk.Label(progress_frame, 
                                       text="0%", 
                                       font=('Segoe UI', 10),
                                       foreground=self.colors['secondary'])
        self.progress_label.grid(row=1, column=0, columnspan=2)
    
    def create_output_section(self, parent, row):
        """Create output section"""
        # Section header
        output_header = ttk.Label(parent, text="📤 Output Results", style='Header.TLabel')
        output_header.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(20, 10))
        
        # Output frame
        output_frame = ttk.Frame(parent)
        output_frame.grid(row=row+1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        output_frame.columnconfigure(1, weight=1)
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(output_frame, 
                                                    height=8, 
                                                    font=('Consolas', 9),
                                                    wrap=tk.WORD,
                                                    bg=self.colors['light_bg'])
        self.output_text.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Output directory button
        self.output_dir_btn = ttk.Button(output_frame, 
                                        text="📁 Open Output Directory", 
                                        style='Modern.TButton',
                                        command=self.open_output_directory,
                                        state='disabled')
        self.output_dir_btn.grid(row=1, column=0, columnspan=2, pady=(10, 0))
    
    def create_action_buttons(self, parent, row):
        """Create action buttons"""
        # Button frame
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row, column=0, columnspan=3, pady=(20, 0))
        
        # Process button
        self.process_btn = ttk.Button(button_frame, 
                                     text="🚀 Start Processing", 
                                     style='Modern.TButton',
                                     command=self.start_processing)
        self.process_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Clear button
        clear_btn = ttk.Button(button_frame, 
                              text="🗑️ Clear", 
                              style='Modern.TButton',
                              command=self.clear_all)
        clear_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Exit button
        exit_btn = ttk.Button(button_frame, 
                             text="❌ Exit", 
                             style='Modern.TButton',
                             command=self.root.quit)
        exit_btn.grid(row=0, column=2)
    
    def create_status_bar(self, parent, row):
        """Create status bar"""
        self.status_bar = ttk.Label(parent, 
                                   text="Ready to process PDF files", 
                                   relief=tk.SUNKEN, 
                                   anchor=tk.W,
                                   font=('Segoe UI', 9))
        self.status_bar.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 0))
    
    def browse_file(self):
        """Browse and select PDF file with cyber interface"""
        if self.processing:
            self.terminal_print("⚠️ Cannot select file while processing!")
            return
            
        file_path = filedialog.askopenfilename(
            title="Select PDF File - AI PDF Splitter Pro",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if file_path:
            self.selected_file.set(file_path)
            filename = os.path.basename(file_path)
            self.file_path_var.set(filename)
            self.terminal_print(f"📁 Selected: {filename}")
            self.update_file_info(file_path)
            self.clear_output()
    
    def update_file_info(self, file_path):
        """Update file information display with cyber styling"""
        try:
            file_size = os.path.getsize(file_path)
            size_mb = file_size / (1024 * 1024)
            
            # Update file info text widget
            self.file_info_text.config(state='normal')
            self.file_info_text.delete(1.0, 'end')
            
            info_text = f"📄 File: {os.path.basename(file_path)}\n"
            info_text += f"📏 Size: {size_mb:.2f} MB\n"
            info_text += f"📂 Path: {file_path}\n"
            
            if size_mb > 400:
                info_text += "❌ Error: File too large (max 400MB)\n"
                self.process_btn.config(state=tk.DISABLED)
                self.terminal_print(f"❌ File too large: {size_mb:.1f}MB (max 400MB)")
            else:
                info_text += "✅ Status: Ready for processing\n" 
                self.process_btn.config(state=tk.NORMAL)
                self.terminal_print(f"✅ File ready: {size_mb:.1f}MB")
                
            self.file_info_text.insert(1.0, info_text)
            self.file_info_text.config(state='disabled')
            
        except Exception as e:
            self.terminal_print(f"❌ Error reading file: {str(e)}")
            self.process_btn.config(state=tk.DISABLED)
    
    def start_processing(self):
        """Start the PDF processing workflow with cyber styling"""
        if not self.selected_file.get():
            self.terminal_print("❌ No file selected!")
            return
        
        if hasattr(self, 'processing') and self.processing:
            self.terminal_print("⚠️ Processing already in progress!")
            return
        
        # Disable controls during processing
        self.processing = True
        self.process_btn.config(state=tk.DISABLED, text="🔄 PROCESSING...")
        self.browse_btn.config(state=tk.DISABLED)
        
        # Reset progress
        self.progress_var.set(0)
        self.progress_label.config(text="0%")
        self.status_label.config(text="Processing...")
        
        # Clear previous output
        self.clear_output()
        
        self.terminal_print("🚀 Starting PDF processing workflow...")
        self.terminal_print("=" * 40)
        
        # Start processing thread
        thread = threading.Thread(target=self.process_pdf_workflow)
        thread.daemon = True
        thread.start()
    
    def process_pdf_workflow(self):
        """Main PDF processing workflow"""
        try:
            pdf_path = self.selected_file.get()
            
            # Step 1: File validation and compression
            self.update_progress_status(10, "Validating file...")
            self.terminal_print("🔍 Checking file size and validity...")
            
            is_valid, file_size, error = check_file_size(pdf_path)
            if not is_valid:
                self.terminal_print(f"❌ File validation failed: {error}")
                self.processing_complete(False)
                return
            
            self.terminal_print(f"✅ File validated: {file_size:.1f} MB")
            self.update_progress_status(20, "File validated")
            
            # Check if compression is needed
            if file_size > 50:
                self.terminal_print("📦 File size > 50 MB, compressing...")
                self.update_progress_status(30, "Compressing...")
                compressed_path = pdf_path.replace('.pdf', '_compressed.pdf')
                
                success, final_size, error = compress_pdf(pdf_path, compressed_path, 50)
                if not success:
                    self.terminal_print(f"❌ Compression failed: {error}")
                    self.processing_complete(False)
                    return
                
                self.terminal_print(f"✅ Compression successful: {final_size:.1f} MB")
                pdf_path = compressed_path
            else:
                self.terminal_print("✅ File size ≤ 50 MB, no compression needed")
            
            self.update_progress_status(40, "File ready for AI analysis")
            
            # Step 2: AI Analysis
            self.update_progress_status(50, "Starting AI analysis...")
            self.terminal_print("🤖 Initializing Gemini AI processor...")
            
            processor = GeminiPDFProcessor()
            self.terminal_print("🔍 Analyzing PDF content with AI...")
            
            analysis_result = processor.analyze_pdf_with_gemini(pdf_path)
            if not analysis_result:
                self.add_message("❌ AI analysis failed")
                return
            
            self.add_message(f"✅ AI analysis complete: {len(analysis_result.get('sections', []))} sections found")
            self.update_progress(70)
            
            # Save analysis result
            analysis_file = pdf_path.replace('.pdf', '_analysis.json')
            with open(analysis_file, 'w') as f:
                json.dump(analysis_result, f, indent=2)
            
            self.add_message(f"💾 Analysis saved to: {os.path.basename(analysis_file)}")
            
            # Step 3: PDF Splitting
            self.update_status("Step 3/3: Splitting PDF into sections...", 80)
            self.add_message("✂️ Splitting PDF into individual pages...")
            
            splitter = PDFSplitter()
            
            # Load AI analysis
            if not splitter.load_ai_analysis(analysis_file):
                self.add_message("❌ Failed to load AI analysis")
                return
            
            # Open PDF
            if not splitter.open_pdf(pdf_path):
                self.add_message("❌ Failed to open PDF")
                return
            
            output_dir = f"./output_{int(time.time())}"
            
            success, summary = splitter.split_pdf(output_dir, verbose=True)
            if not success:
                self.add_message(f"❌ PDF splitting failed: {summary}")
                return
            
            self.add_message("✅ PDF splitting complete!")
            self.update_progress(100)
            
            # Final success
            self.update_status("✅ Processing Complete!", 100)
            self.add_message("🎉 All steps completed successfully!")
            
            # Show results
            self.show_results(analysis_result, output_dir, summary)
            
        except Exception as e:
            self.add_message(f"❌ Unexpected error: {str(e)}")
            self.update_status("❌ Processing Failed", 0)
        finally:
            self.processing = False
            self.process_btn.config(state='normal')
    
    def update_status(self, message, progress):
        """Update status and progress"""
        self.processing_queue.put(('status', message))
        self.processing_queue.put(('progress', progress))
    
    def update_progress(self, value):
        """Update progress bar"""
        self.processing_queue.put(('progress', value))
    
    def add_message(self, message):
        """Add message to processing log"""
        self.processing_queue.put(('message', message))
    
    def update_processing_messages(self):
        """Update processing messages from queue"""
        try:
            while True:
                msg_type, data = self.processing_queue.get_nowait()
                
                if msg_type == 'status':
                    self.current_step.set(data)
                    if hasattr(self, 'status_label'):
                        self.status_label.config(text=data)
                elif msg_type == 'progress':
                    self.progress_var.set(data)
                    self.progress_label.config(text=f"{data:.0f}%")
                elif msg_type == 'message':
                    self.terminal_print(str(data))
                    
        except queue.Empty:
            pass
        
        self.root.after(100, self.update_processing_messages)
    
    def show_results(self, analysis_result, output_dir, summary):
        """Display processing results"""
        # Print results to terminal
        self.terminal_print("🎯 PROCESSING COMPLETE!")
        self.terminal_print("")
        self.terminal_print("📊 ANALYSIS SUMMARY:")
        self.terminal_print(f"• Total Sections: {len(analysis_result.get('sections', []))}")
        self.terminal_print(f"• Total Pages: {analysis_result.get('metadata', {}).get('total_pages', 'Unknown')}")
        self.terminal_print(f"• File Name: {analysis_result.get('metadata', {}).get('file_name', 'Unknown')}")
        self.terminal_print("")
        self.terminal_print("📁 OUTPUT DIRECTORY:")
        self.terminal_print(output_dir)
        self.terminal_print("")
        self.terminal_print("📋 SECTIONS FOUND:")
        
        for section in analysis_result.get('sections', []):
            self.terminal_print(f"• {section.get('title', 'Unknown')} (Pages {section.get('page_range', 'Unknown')})")
        
        self.terminal_print("")
        self.terminal_print("📄 SPLITTING SUMMARY:")
        self.terminal_print(summary)
        
        # Enable output directory button
        if hasattr(self, 'open_output_btn'):
            self.open_output_btn.config(state=tk.NORMAL)
        
        # Store output directory for later use
        self.output_directory = output_dir
        
        # Show success message
        messagebox.showinfo("Success", f"PDF processing complete!\n\nOutput saved to:\n{output_dir}")
    
    def open_output_directory(self):
        """Open output directory in file manager"""
        if hasattr(self, 'output_directory') and os.path.exists(self.output_directory):
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(self.output_directory)
                elif os.name == 'posix':  # macOS and Linux
                    os.system(f'xdg-open "{self.output_directory}"')
            except Exception as e:
                messagebox.showerror("Error", f"Could not open directory: {str(e)}")
    
    def clear_output(self):
        """Clear output displays"""
        self.status_label.config(text="Ready")
        self.progress_var.set(0)
        self.progress_label.config(text="0%")
        if hasattr(self, 'open_output_btn'):
            self.open_output_btn.config(state=tk.DISABLED)

def main():
    """Main application entry point with proper window initialization"""
    # Create root window
    root = tk.Tk()
    
    # Set window properties before creating app
    root.withdraw()  # Hide initially for smooth startup
    
    # Create the ultra-modern app
    app = UltraModernAIApp(root)
    
    # Show window properly as a main application window
    root.deiconify()
    root.lift()
    root.attributes('-topmost', True)  # Bring to front initially
    root.after(100, lambda: root.attributes('-topmost', False))  # Then allow normal behavior
    
    # Focus the window
    root.focus_set()
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
