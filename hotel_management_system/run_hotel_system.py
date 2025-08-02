#!/usr/bin/env python3
"""
Hotel Management System Launcher
Simple launcher script with error handling and system checks
"""

import sys
import os
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_pyqt5():
    """Check if PyQt5 is installed"""
    try:
        import PyQt5
        print("✅ PyQt5 is installed")
        return True
    except ImportError:
        print("❌ PyQt5 is not installed!")
        print("Please run: pip install PyQt5")
        return False

def check_display():
    """Check if display is available (for GUI)"""
    system = platform.system()
    
    if system == "Linux":
        if not os.environ.get('DISPLAY'):
            print("❌ No display found! GUI applications cannot run.")
            print("This might be a headless server or SSH session without X11 forwarding.")
            print("To run with X11 forwarding: ssh -X username@hostname")
            return False
    
    print("✅ Display environment OK")
    return True

def install_requirements():
    """Install requirements if needed"""
    try:
        print("📦 Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def run_database_test():
    """Run database test"""
    try:
        print("\n🧪 Running database test...")
        subprocess.check_call([sys.executable, "test_database.py"])
        return True
    except subprocess.CalledProcessError:
        print("❌ Database test failed")
        return False

def main():
    """Main launcher function"""
    print("🏨 Hotel Management System Launcher")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ main.py not found! Please run this script from the hotel_management_system directory.")
        sys.exit(1)
    
    # Check PyQt5
    if not check_pyqt5():
        print("\n📦 Attempting to install PyQt5...")
        if not install_requirements():
            sys.exit(1)
    
    # Check display (for GUI)
    if not check_display():
        print("\n🔄 Running database test instead...")
        if run_database_test():
            print("\n✅ Database functionality verified!")
            print("💡 To run the GUI application, use a system with display support.")
        sys.exit(0)
    
    # Run database test first
    print("\n🧪 Testing database functionality...")
    if not run_database_test():
        print("❌ Database test failed. Please check the error messages above.")
        sys.exit(1)
    
    print("\n🚀 Starting Hotel Management System...")
    print("=" * 50)
    
    try:
        # Import and run the main application
        from main import main as run_app
        run_app()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please make sure all required files are present.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Application error: {e}")
        print("Please check the error messages and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
