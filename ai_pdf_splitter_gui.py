#!/usr/bin/env python3
"""
AI PDF Splitter - Modern GUI Application
Integrates PDF compression, AI analysis, and intelligent splitting into one application
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

# Import our modules
from pdf_compressor import check_file_size, compress_pdf
from ai_processor import GeminiPDFProcessor
from pdf_splitter import PDFSplitter

class ModernAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI PDF Splitter - Intelligent Document Processing")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Set app icon and styling
        self.setup_styling()
        
        # Initialize variables
        self.selected_file = tk.StringVar()
        self.processing_queue = queue.Queue()
        self.current_step = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar()
        
        # Create GUI components
        self.create_widgets()
        
        # Start processing thread
        self.processing_thread = None
        self.is_processing = False
        
        # Update processing messages
        self.root.after(100, self.update_processing_messages)
    
    def setup_styling(self):
        """Setup modern styling and colors"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'error': '#e74c3c',
            'light_bg': '#ecf0f1',
            'dark_bg': '#2c3e50',
            'text_light': '#2c3e50',
            'text_dark': '#ffffff'
        }
        
        # Configure styles
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 24, 'bold'), 
                       foreground=self.colors['primary'])
        
        style.configure('Header.TLabel', 
                       font=('Segoe UI', 14, 'bold'), 
                       foreground=self.colors['primary'])
        
        style.configure('Success.TLabel', 
                       font=('Segoe UI', 12), 
                       foreground=self.colors['success'])
        
        style.configure('Warning.TLabel', 
                       font=('Segoe UI', 12), 
                       foreground=self.colors['warning'])
        
        style.configure('Error.TLabel', 
                       font=('Segoe UI', 12), 
                       foreground=self.colors['error'])
        
        style.configure('Modern.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(20, 10))
        
        style.configure('Progress.Horizontal.TProgressbar',
                       troughcolor=self.colors['light_bg'],
                       background=self.colors['secondary'])
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="🤖 AI PDF Splitter", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        subtitle_label = ttk.Label(main_frame, 
                                  text="Intelligent PDF Processing & Analysis", 
                                  font=('Segoe UI', 12),
                                  foreground=self.colors['secondary'])
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 30))
        
        # File Selection Section
        self.create_file_selection_section(main_frame, 2)
        
        # Processing Status Section
        self.create_processing_section(main_frame, 3)
        
        # Progress Section
        self.create_progress_section(main_frame, 4)
        
        # Output Section
        self.create_output_section(main_frame, 5)
        
        # Action Buttons
        self.create_action_buttons(main_frame, 6)
        
        # Status Bar
        self.create_status_bar(main_frame, 7)
    
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
        """Browse and select PDF file"""
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if file_path:
            self.selected_file.set(file_path)
            self.update_file_info(file_path)
            self.clear_output()
    
    def update_file_info(self, file_path):
        """Update file information display"""
        try:
            file_size = os.path.getsize(file_path)
            size_mb = file_size / (1024 * 1024)
            
            if size_mb > 400:
                self.file_info_label.config(
                    text=f"❌ File too large: {size_mb:.1f} MB (max: 400 MB)",
                    foreground=self.colors['error']
                )
                self.process_btn.config(state='disabled')
            else:
                self.file_info_label.config(
                    text=f"✅ File size: {size_mb:.1f} MB - Ready to process",
                    foreground=self.colors['success']
                )
                self.process_btn.config(state='normal')
                
        except Exception as e:
            self.file_info_label.config(
                text=f"❌ Error reading file: {str(e)}",
                foreground=self.colors['error']
            )
            self.process_btn.config(state='disabled')
    
    def start_processing(self):
        """Start the PDF processing workflow"""
        if not self.selected_file.get():
            messagebox.showerror("Error", "Please select a PDF file first!")
            return
        
        if self.is_processing:
            messagebox.showwarning("Warning", "Processing already in progress!")
            return
        
        # Start processing in separate thread
        self.is_processing = True
        self.process_btn.config(state='disabled')
        self.processing_thread = threading.Thread(target=self.process_pdf_workflow)
        self.processing_thread.daemon = True
        self.processing_thread.start()
    
    def process_pdf_workflow(self):
        """Main PDF processing workflow"""
        try:
            pdf_path = self.selected_file.get()
            
            # Step 1: File validation and compression
            self.update_status("Step 1/3: Validating and compressing PDF...", 10)
            self.add_message("🔍 Checking file size and validity...")
            
            is_valid, file_size, error = check_file_size(pdf_path)
            if not is_valid:
                self.add_message(f"❌ File validation failed: {error}")
                return
            
            self.add_message(f"✅ File validated: {file_size:.1f} MB")
            self.update_progress(20)
            
            # Check if compression is needed
            if file_size > 50:
                self.add_message("📦 File size > 50 MB, compressing...")
                compressed_path = pdf_path.replace('.pdf', '_compressed.pdf')
                
                success, final_size, error = compress_pdf(pdf_path, compressed_path, 50)
                if not success:
                    self.add_message(f"❌ Compression failed: {error}")
                    return
                
                self.add_message(f"✅ Compression successful: {final_size:.1f} MB")
                pdf_path = compressed_path
            else:
                self.add_message("✅ File size ≤ 50 MB, no compression needed")
            
            self.update_progress(40)
            
            # Step 2: AI Analysis
            self.update_status("Step 2/3: AI analysis with Gemini...", 50)
            self.add_message("🤖 Initializing Gemini AI processor...")
            
            processor = GeminiPDFProcessor()
            self.add_message("🔍 Analyzing PDF content with AI...")
            
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
            self.is_processing = False
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
                    self.status_bar.config(text=data)
                elif msg_type == 'progress':
                    self.progress_var.set(data)
                    self.progress_label.config(text=f"{data:.0f}%")
                elif msg_type == 'message':
                    self.messages_text.insert(tk.END, f"{data}\n")
                    self.messages_text.see(tk.END)
                    
        except queue.Empty:
            pass
        
        self.root.after(100, self.update_processing_messages)
    
    def show_results(self, analysis_result, output_dir, summary):
        """Display processing results"""
        # Update output text
        output_text = f"""🎯 PROCESSING COMPLETE!

📊 ANALYSIS SUMMARY:
• Total Sections: {len(analysis_result.get('sections', []))}
• Total Pages: {analysis_result.get('metadata', {}).get('total_pages', 'Unknown')}
• File Name: {analysis_result.get('metadata', {}).get('file_name', 'Unknown')}

📁 OUTPUT DIRECTORY:
{output_dir}

📋 SECTIONS FOUND:
"""
        
        for section in analysis_result.get('sections', []):
            output_text += f"• {section.get('title', 'Unknown')} (Pages {section.get('page_range', 'Unknown')})\n"
        
        output_text += f"\n📄 SPLITTING SUMMARY:\n{summary}"
        
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(1.0, output_text)
        
        # Enable output directory button
        self.output_dir_btn.config(state='normal')
        
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
        """Clear output display"""
        self.output_text.delete(1.0, tk.END)
        self.output_dir_btn.config(state='disabled')
        self.messages_text.delete(1.0, tk.END)
        self.progress_var.set(0)
        self.progress_label.config(text="0%")
        self.current_step.set("Ready")
        self.status_bar.config(text="Ready to process PDF files")
    
    def clear_all(self):
        """Clear all inputs and outputs"""
        self.selected_file.set("")
        self.file_info_label.config(text="No file selected", foreground=self.colors['text_light'])
        self.process_btn.config(state='disabled')
        self.clear_output()

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = ModernAIApp(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
