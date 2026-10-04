#!/usr/bin/env python3
"""
Eliva Quick Start Script
Run this to verify your setup before deployment
"""

import os
import sys
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print('='*60)

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path("D:/eliva/.env")

    if not env_path.exists():
        return False, "Missing .env file"

    required_vars = [
        'ANTHROPIC_API_KEY',
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN',
        'TWILIO_PHONE_NUMBER',
        'MY_NAME'
    ]

    with open(env_path, 'r') as f:
        content = f.read()

    missing = []
    for var in required_vars:
        if var not in content or f"{var}=your-" in content or f"{var}=change-" in content:
            missing.append(var)

    if missing:
        return False, f"Missing or unconfigured: {', '.join(missing)}"

    return True, "All required variables configured"

def check_dependencies():
    """Check if all required packages are installed"""
    required = ['anthropic', 'flask', 'twilio', 'dotenv']
    missing = []

    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)

    if missing:
        return False, f"Missing packages: {', '.join(missing)}"

    return True, "All dependencies installed"

def check_knowledge_base():
    """Check if knowledge base is configured"""
    kb_path = Path("D:/eliva/knowledge/user_profile.json")

    if not kb_path.exists():
        return False, "Knowledge base not initialized"

    return True, "Knowledge base exists"

def main():
    print_header("🚀 Eliva Setup Verification")
    print("\nChecking your Eliva setup before deployment...\n")

    checks = [
        ("Environment Configuration", check_env_file),
        ("Python Dependencies", check_dependencies),
        ("Knowledge Base", check_knowledge_base),
    ]

    all_passed = True

    for name, check_func in checks:
        print(f"Checking {name}...", end=" ")
        passed, message = check_func()

        if passed:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
            all_passed = False

    print("\n" + "="*60)

    if all_passed:
        print("\n🎉 All checks passed! You're ready to deploy.\n")
        print("Next steps:")
        print("  1. Start Eliva locally: python run.py")
        print("  2. Create public URL: python run.py --tunnel")
        print("  3. Configure Twilio webhooks (see REAL_LIFE_SETUP.md)")
        print("  4. Test by calling your Twilio number")
        print("\nFor detailed instructions, see: REAL_LIFE_SETUP.md")
    else:
        print("\n⚠️  Some checks failed. Fix the issues above before deploying.\n")
        print("Quick fixes:")
        print("  • Missing .env? Copy .env.example to .env and fill in values")
        print("  • Missing packages? Run: pip install -r requirements.txt")
        print("  • Missing knowledge base? Run: python setup_wizard.py")
        print("\nFor help, see: REAL_LIFE_SETUP.md")

    print("="*60 + "\n")

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
