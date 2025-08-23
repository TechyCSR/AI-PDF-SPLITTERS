#!/bin/bash
# AI PDF Splitter Pro - Cross-Platform Launcher Script
# Automatic setup and launch for Linux/macOS

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$DIR"

echo -e "${CYAN}"
echo "🚀 AI PDF Splitter Pro - Intelligent Document Processing Suite"
echo "================================================================"
echo -e "${NC}"

# Check Python installation
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed!"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_success "Python $PYTHON_VERSION found"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
print_status "Checking dependencies..."
if ! python -c "import fitz, google.generativeai, dotenv, PIL" &> /dev/null; then
    print_status "Installing required dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Dependencies installed successfully"
else
    print_success "All dependencies are already installed"
fi

# Check .env file
if [ ! -f ".env" ]; then
    print_status "Creating .env configuration file..."
    
    cat > .env << 'EOF'
# AI PDF Splitter Pro Configuration
# ================================

# Google Gemini AI API Key
# Get your key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_api_key_here

# AI Model Configuration
GEMINI_TEMPERATURE=0.1
GEMINI_MAX_TOKENS=8192

# Processing Settings
MAX_FILE_SIZE_MB=400
COMPRESSION_TARGET_MB=50
EOF

    print_success ".env file created"
    echo ""
    print_warning "📋 SETUP REQUIRED:"
    echo "1. Visit: https://makersuite.google.com/app/apikey"
    echo "2. Sign in with your Google account"
    echo "3. Create a new API key"
    echo "4. Copy the key and paste it in the .env file"
    echo ""
    print_status "Opening .env file for editing..."
    
    # Try to open with available editors
    if command -v nano &> /dev/null; then
        nano .env
    elif command -v vim &> /dev/null; then
        vim .env
    elif command -v gedit &> /dev/null; then
        gedit .env &
    else
        print_warning "Please edit the .env file manually and replace 'your_api_key_here' with your actual API key"
        read -p "Press Enter when you've updated the .env file..."
    fi
fi

# Validate API key
if grep -q "your_api_key_here" .env; then
    print_error "API key not configured!"
    echo "Please edit the .env file and add your Google Gemini API key"
    echo "Run this script again after updating the API key"
    exit 1
fi

# Check if API key is set
source .env
if [ -z "$GEMINI_API_KEY" ] || [ "$GEMINI_API_KEY" = "your_api_key_here" ]; then
    print_error "GEMINI_API_KEY not set in .env file!"
    exit 1
fi

print_success "Configuration validated"

# Launch the application
echo ""
print_status "🚀 Launching AI PDF Splitter Pro..."
print_status "📁 Project directory: $DIR"
print_status "🐍 Python environment: $(which python)"
print_status "💻 Starting modern GUI interface..."
echo ""

# Launch the GUI
python ai_pdf_splitter_gui.py

