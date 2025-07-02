#!/usr/bin/env python3
"""
Setup script for AI-Powered YAML CV Editor
Installs dependencies and helps configure OpenAI API key
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def run_command(command, description):
    """Run a command and return success status."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed: {str(e)}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} is not supported. Need Python 3.7+")
        return False

def install_dependencies():
    """Install required Python packages."""
    packages = [
        "flask>=2.0.0",
        "pyyaml>=6.0", 
        "rendercv[full]>=1.14",
        "openai>=1.3.0",
        "requests>=2.28.0"
    ]
    
    print("📦 Installing dependencies...")
    for package in packages:
        success = run_command(f"pip install {package}", f"Installing {package}")
        if not success:
            print(f"⚠️  Failed to install {package}. You may need to install it manually.")
    
    return True

def setup_openai_key():
    """Help user set up OpenAI API key."""
    print("\n🤖 Setting up OpenAI API Key...")
    print("You need an OpenAI API key to use the AI assistant features.")
    print("Visit: https://platform.openai.com/api-keys")
    
    # Check if key is already set
    existing_key = os.getenv('OPENAI_API_KEY')
    if existing_key and existing_key.startswith('sk-'):
        print("✅ OpenAI API key is already configured!")
        return True
    
    print("\nOptions to set your API key:")
    
    if os.name == 'nt':  # Windows
        print("1. Temporary (this session only):")
        print('   set OPENAI_API_KEY=your_api_key_here')
        print("\n2. Permanent (PowerShell):")
        print('   [System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your_api_key_here", "User")')
        print("\n3. Permanent (Command Prompt):")
        print('   setx OPENAI_API_KEY "your_api_key_here"')
    else:  # Linux/Mac
        print("1. Temporary (this session only):")
        print('   export OPENAI_API_KEY=your_api_key_here')
        print("\n2. Permanent (add to ~/.bashrc or ~/.zshrc):")
        print('   echo "export OPENAI_API_KEY=your_api_key_here" >> ~/.bashrc')
    
    print("\n⚠️  Important: Keep your API key secure and never share it!")
    
    # Ask if they want to set it now
    response = input("\nDo you want to set your API key now? (y/n): ").lower().strip()
    if response.startswith('y'):
        api_key = input("Enter your OpenAI API key (sk-...): ").strip()
        if api_key.startswith('sk-'):
            os.environ['OPENAI_API_KEY'] = api_key
            print("✅ API key set for this session!")
            print("⚠️  Remember to set it permanently using the commands above.")
            return True
        else:
            print("❌ Invalid API key format. Should start with 'sk-'")
            return False
    
    return False

def create_sample_cv():
    """Create a sample CV file if it doesn't exist."""
    cv_file = "working_CV.yaml"
    if not os.path.exists(cv_file):
        print(f"📝 Creating sample CV file: {cv_file}")
        # The sample CV will be created by the main app when it starts
        return True
    else:
        print(f"✅ CV file already exists: {cv_file}")
        return True

def main():
    """Main setup function."""
    print("🚀 AI-Powered YAML CV Editor Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Setup failed: Incompatible Python version")
        sys.exit(1)
    
    # Install dependencies
    print("\n📦 Installing Dependencies...")
    install_dependencies()
    
    # Setup OpenAI API key
    api_key_set = setup_openai_key()
    
    # Create sample CV
    print("\n📝 Setting up CV file...")
    create_sample_cv()
    
    # Final instructions
    print("\n" + "=" * 40)
    print("🎉 Setup Complete!")
    print("\nNext steps:")
    print("1. Start the editor: python simple_yaml_editor.py")
    print("2. Open browser to: http://localhost:5000")
    
    if not api_key_set:
        print("\n⚠️  Don't forget to set your OpenAI API key!")
        print("   The AI features won't work without it.")
    
    # Ask if they want to start the editor now
    response = input("\nWould you like to start the editor now? (y/n): ").lower().strip()
    if response.startswith('y'):
        print("\n🚀 Starting the AI-Powered YAML CV Editor...")
        try:
            # Try to open browser
            webbrowser.open('http://localhost:5000')
        except:
            print("⚠️  Could not open browser automatically. Please open manually.")
        
        # Start the editor
        os.system("python simple_yaml_editor.py")
    else:
        print("\n💡 Run 'python simple_yaml_editor.py' when you're ready to start!")

if __name__ == "__main__":
    main() 
