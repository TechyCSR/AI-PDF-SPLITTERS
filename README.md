# 🚀 AI PDF Splitter Pro

**Intelligent Document Processing & Analysis Suite**

A powerful, AI-driven PDF processing tool that automatically analyzes PDFs using Google Gemini AI and splits them into organized sections with a modern, professional GUI interface.

## ✨ Features

### 🎯 Core Functionality
- **📁 Smart File Handling**: Accepts PDFs up to 400MB with automatic compression
- **🤖 AI-Powered Analysis**: Uses Google Gemini AI to intelligently identify document sections
- **✂️ Automated Splitting**: Organizes pages into structured folders with consistent naming
- **📊 Live Progress Tracking**: Real-time processing updates with percentage display
- **💻 Terminal Interface**: Live processing output with timestamps

### 🎨 Modern GUI Interface
- **🖥️ Fixed Medium Window**: 900x700 non-resizable professional layout
- **🔄 Split Layout**: File selector at top, terminal + results at bottom
- **🎭 Cyber Tech Theme**: Dark theme with cyan/green accents
- **📱 Responsive Design**: Clean, organized interface with modern styling
- **🔒 Smart Controls**: Automatic button state management during processing

### 📂 Intelligent Organization
- **📁 Master Folders**: Uses full PDF name as prefix (e.g., "WF_4262_The Paris Library")
- **📂 Sub Folders**: Organized by sections with consistent naming
- **📄 Individual Files**: Section-relative page numbering with full prefix
- **🏷️ Safe Naming**: Automatic sanitization of invalid characters

## 🔧 System Requirements

### Prerequisites
- **Python 3.8+** (3.12 recommended)
- **Operating System**: Windows 10+ or Linux (Ubuntu 20.04+)
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 2GB free space for processing large files
- **Internet**: Required for Google Gemini AI API access

### Dependencies
- `PyMuPDF (fitz)` - PDF manipulation and compression
- `google-generativeai` - Google Gemini AI integration
- `python-dotenv` - Environment variable management
- `Pillow (PIL)` - Image processing for PDF compression
- `tkinter` - GUI framework (usually included with Python)

## 🚀 Quick Start

### 1. Download & Setup
```bash
# Clone or download the project
git clone <repository-url>
cd AI-PDF-SPLITTERS

# Run the automatic setup script
./launch.sh          # Linux/macOS
launch.bat           # Windows
```

### 2. API Configuration
The launch script will automatically:
- Create a Python virtual environment
- Install all required dependencies
- Generate a `.env` configuration file
- Prompt you to add your Google Gemini API key

### 3. Get Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Paste it into the `.env` file when prompted

### 4. Launch Application
After setup, simply run:
```bash
./launch.sh          # Linux/macOS
launch.bat           # Windows
```

## 📋 Usage Guide

### Step 1: Select PDF File
1. Click **"📁 BROWSE"** to select your PDF file
2. Files up to 400MB are supported
3. File information will display automatically

### Step 2: Process Document
1. Click **"⚡ PROCESS"** to begin analysis
2. Watch live progress in the terminal panel
3. Processing includes:
   - File validation and compression (if needed)
   - AI analysis with Google Gemini
   - Intelligent section identification
   - Automated page splitting

### Step 3: Access Results
1. View detailed results in the terminal
2. Click **"📂 OPEN OUTPUT"** to access organized files
3. Use **"🗑️ CLEAR"** to reset for new processing

## 📁 Output Structure

### Example for: `WF_4262_The Paris Library.pdf`

```
📁 WF_4262_The Paris Library/
├── 📂 WF_4262_The Paris Library_Front Cover/
│   └── 📄 WF_4262_The Paris Library_Front Cover_Page_1.pdf
├── 📂 WF_4262_The Paris Library_Chapter 1_Odile/
│   ├── 📄 WF_4262_The Paris Library_Chapter 1_Odile_Page_1.pdf
│   ├── 📄 WF_4262_The Paris Library_Chapter 1_Odile_Page_2.pdf
│   └── 📄 WF_4262_The Paris Library_Chapter 1_Odile_Page_3.pdf
├── 📂 WF_4262_The Paris Library_Chapter 2_Lily/
│   ├── 📄 WF_4262_The Paris Library_Chapter 2_Lily_Page_1.pdf
│   └── 📄 WF_4262_The Paris Library_Chapter 2_Lily_Page_2.pdf
└── 📋 splitting_summary.txt
```

## ⚙️ Configuration

### Environment Variables (.env)
```env
# Google Gemini AI Configuration
GEMINI_API_KEY=your_api_key_here
GEMINI_TEMPERATURE=0.1
GEMINI_MAX_TOKENS=8192
```

### Processing Settings
- **Maximum File Size**: 400MB input limit
- **Compression Target**: ~50MB for AI analysis
- **AI Model**: Google Gemini Pro
- **Output Format**: Individual PDF pages
- **Naming Convention**: Consistent prefix-based system

## 🛠️ Advanced Usage

### Manual Installation
If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv

# Activate environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your API key

# Launch GUI
python ai_pdf_splitter_gui.py
```

### Command Line Interface
Each component can be used independently:

```bash
# Step 1: Compress PDF
python pdf_compressor.py input.pdf

# Step 2: AI Analysis
python ai_processor.py input_compressed.pdf

# Step 3: Split PDF
python pdf_splitter.py input.pdf analysis.json output_directory
```

## 🐛 Troubleshooting

### Common Issues

**1. "ModuleNotFoundError" during startup**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**2. "API key not found" error**
```bash
# Check .env file exists and contains valid key
cat .env  # Linux/macOS
type .env # Windows

# Verify API key format (should start with 'AI')
```

**3. "File too large" error**
- Maximum input size is 400MB
- For larger files, use external PDF compression first
- Consider splitting large documents manually

**4. GUI doesn't start**
```bash
# Check Python version (3.8+ required)
python --version

# Verify tkinter installation
python -c "import tkinter"

# Try launching manually
python ai_pdf_splitter_gui.py
```

### Performance Tips
- **Large Files**: Files over 100MB may take longer to process
- **Internet Speed**: AI analysis requires stable internet connection
- **Memory Usage**: Close other applications for large file processing
- **Storage Space**: Ensure 2x file size available for temporary files

## 🔒 Privacy & Security

- **Local Processing**: PDF compression and splitting happen locally
- **AI Analysis**: Only PDF content is sent to Google Gemini (secure HTTPS)
- **No Data Storage**: No files are permanently stored by Google
- **API Key Security**: Store your API key securely in `.env` file

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the terminal output for error messages
3. Ensure your API key is valid and has sufficient quota
4. Verify your internet connection for AI analysis

## 🔮 Future Features

- [ ] Batch processing for multiple PDFs
- [ ] Custom AI prompts for specialized document types
- [ ] OCR integration for scanned documents
- [ ] Cloud storage integration
- [ ] Advanced filtering and search capabilities

---

## 👨‍💻 Author

**Built with ❤️ by [@TechyCSR](https://techycsr.me/)**

🌐 **Portfolio**: [techycsr.me](https://techycsr.me/)  
💼 **Professional**: AI/ML Developer & Software Engineer  
🚀 **Passion**: Creating intelligent solutions for document processing  

---

### 🎯 About This Project

This AI PDF Splitter Pro represents the intersection of **artificial intelligence** and **practical document management**. Built using cutting-edge AI technology from Google Gemini, it demonstrates how modern AI can solve real-world productivity challenges.

**Key Technologies:**
- 🤖 **Google Gemini AI** - Advanced document analysis
- 🐍 **Python 3.8+** - Core development platform  
- 🖥️ **Tkinter** - Modern GUI framework
- 📄 **PyMuPDF** - PDF processing engine
- 🎨 **Modern UI/UX** - Professional interface design

---

*© 2024 TechyCSR. All rights reserved. Made with ❤️ for intelligent document processing.*