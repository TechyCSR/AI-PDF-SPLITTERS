#!/usr/bin/env python3
"""
AI PDF Splitter GUI Launcher
Simple script to check dependencies and launch the GUI application
"""

import sys
import subprocess
import importlib.util

def check_dependency(module_name, package_name=None):
    """Check if a Python module is available"""
    if package_name is None:
        package_name = module_name
    
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        return False, package_name
    return True, None

def install_dependency(package_name):
    """Install a Python package using pip"""
    try:
        print(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_install_dependencies():
    """Check and install required dependencies"""
    print("🔍 Checking dependencies...")
    
    dependencies = [
        ("fitz", "PyMuPDF"),
        ("PIL", "Pillow"),
        ("google.generativeai", "google-generativeai"),
        ("dotenv", "python-dotenv"),
    ]
    
    missing_deps = []
    
    for module, package in dependencies:
        available, missing = check_dependency(module, package)
        if not available:
            missing_deps.append(package)
    
    if missing_deps:
        print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        
        # Try to install missing dependencies
        print("\n📦 Attempting to install missing dependencies...")
        for dep in missing_deps:
            if install_dependency(dep):
                print(f"✅ Successfully installed {dep}")
            else:
                print(f"❌ Failed to install {dep}")
                return False
        
        print("\n✅ All dependencies installed successfully!")
    else:
        print("✅ All dependencies are available!")
    
    return True

def check_env_file():
    """Check if .env file exists and has required variables"""
    import os
    
    if not os.path.exists('.env'):
        print("⚠️  .env file not found!")
        print("Please create a .env file with your Gemini API key:")
        print("GEMINI_API_KEY=your_api_key_here")
        print("GEMINI_TEMPERATURE=0.1")
        print("GEMINI_MAX_TOKENS=8192")
        return False
    
    # Check if API key is set
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key == 'your_gemini_api_key_here':
            print("⚠️  Please set your Gemini API key in the .env file")
            return False
        
        print("✅ Environment configuration looks good!")
        return True
        
    except Exception as e:
        print(f"⚠️  Error reading .env file: {e}")
        return False

def main():
    """Main launcher function"""
    print("🚀 AI PDF Splitter GUI Launcher")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    
    # Check and install dependencies
    if not check_and_install_dependencies():
        print("\n❌ Failed to install required dependencies!")
        print("Please install them manually:")
        print("pip install -r requirements_gui.txt")
        sys.exit(1)
    
    # Check environment configuration
    if not check_env_file():
        print("\n⚠️  Environment not configured properly!")
        print("Please check your .env file and try again.")
        sys.exit(1)
    
    print("\n🎯 Launching AI PDF Splitter GUI...")
    
    try:
        # Import and run the GUI
        from ai_pdf_splitter_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ Error importing GUI module: {e}")
        print("Please ensure all files are in the same directory.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
