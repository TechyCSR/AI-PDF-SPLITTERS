#!/usr/bin/env python3
"""
AI PDF Splitter Pro - Universal Setup Script
Cross-platform setup and launcher for all operating systems
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

# Colors for cross-platform output
class Colors:
    if platform.system() == "Windows":
        # Windows doesn't support ANSI colors in older versions
        CYAN = GREEN = YELLOW = RED = NC = ""
    else:
        CYAN = '\033[0;36m'
        GREEN = '\033[0;32m'
        YELLOW = '\033[1;33m'
        RED = '\033[0;31m'
        NC = '\033[0m'

def print_status(message):
    print(f"{Colors.CYAN}[INFO]{Colors.NC} {message}")

def print_success(message):
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {message}")

def print_warning(message):
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {message}")

def print_error(message):
    print(f"{Colors.RED}[ERROR]{Colors.NC} {message}")

def check_python():
    """Check if Python 3.8+ is available"""
    print_status("Checking Python installation...")
    
    if sys.version_info < (3, 8):
        print_error(f"Python 3.8+ required, found {sys.version}")
        return False
    
    print_success(f"Python {sys.version.split()[0]} found")
    return True

def create_venv():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path("venv")
    
    if not venv_path.exists():
        print_status("Creating Python virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print_success("Virtual environment created")
        except subprocess.CalledProcessError:
            print_error("Failed to create virtual environment")
            return False
    else:
        print_success("Virtual environment already exists")
    
    return True

def get_venv_python():
    """Get the path to the Python executable in the virtual environment"""
    system = platform.system()
    if system == "Windows":
        return Path("venv") / "Scripts" / "python.exe"
    else:
        return Path("venv") / "bin" / "python"

def install_requirements():
    """Install required packages"""
    print_status("Installing required dependencies...")
    
    venv_python = get_venv_python()
    
    try:
        # Upgrade pip first
        subprocess.run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Install requirements
        subprocess.run([str(venv_python), "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        
        print_success("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error("Failed to install dependencies")
        print(e.stderr.decode() if e.stderr else "Unknown error")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print_status("Creating .env configuration file...")
        
        env_content = """# AI PDF Splitter Pro Configuration
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
"""
        
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        print_success(".env file created")
        return False  # Indicates setup needed
    
    return True  # File already exists

def validate_env_file():
    """Validate .env file has proper API key"""
    env_path = Path(".env")
    
    if not env_path.exists():
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
    
    if "your_api_key_here" in content:
        return False
    
    # Check if GEMINI_API_KEY is set
    for line in content.split('\n'):
        if line.startswith('GEMINI_API_KEY=') and len(line.split('=', 1)[1].strip()) > 10:
            return True
    
    return False

def open_env_file():
    """Open .env file for editing"""
    print_warning("📋 SETUP REQUIRED:")
    print("1. Visit: https://makersuite.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Create a new API key")
    print("4. Copy the key and replace 'your_api_key_here' in the .env file")
    print()
    
    env_path = Path(".env").absolute()
    system = platform.system()
    
    try:
        if system == "Windows":
            os.startfile(str(env_path))
        elif system == "Darwin":  # macOS
            subprocess.run(["open", str(env_path)])
        else:  # Linux
            # Try different editors
            for editor in ["nano", "vim", "gedit", "kate"]:
                if shutil.which(editor):
                    subprocess.run([editor, str(env_path)])
                    break
            else:
                print(f"Please edit {env_path} manually")
    except Exception:
        print(f"Please edit {env_path} manually")

def launch_gui():
    """Launch the GUI application"""
    print_status("🚀 Launching AI PDF Splitter Pro...")
    print_status(f"📁 Project directory: {Path.cwd()}")
    print_status("💻 Starting modern GUI interface...")
    print()
    
    venv_python = get_venv_python()
    
    try:
        subprocess.run([str(venv_python), "ai_pdf_splitter_gui.py"], check=True)
        print_success("Application closed successfully")
    except subprocess.CalledProcessError:
        print_error("Application failed to start")
        return False
    except KeyboardInterrupt:
        print_warning("Application interrupted by user")
    
    return True

def main():
    """Main setup and launch function"""
    print(f"{Colors.CYAN}")
    print("🚀 AI PDF Splitter Pro - Intelligent Document Processing Suite")
    print("================================================================")
    print(f"{Colors.NC}")
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check Python version
    if not check_python():
        return 1
    
    # Create virtual environment
    if not create_venv():
        return 1
    
    # Install requirements
    if not install_requirements():
        return 1
    
    # Create .env file
    env_exists = create_env_file()
    
    # If .env was just created or API key not set, prompt user
    if not env_exists or not validate_env_file():
        open_env_file()
        input("\nPress Enter after updating the .env file with your API key...")
        
        # Re-validate
        if not validate_env_file():
            print_error("API key not properly configured!")
            print("Please edit the .env file and add your Google Gemini API key")
            return 1
    
    print_success("Configuration validated")
    print()
    
    # Launch the application
    if launch_gui():
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
