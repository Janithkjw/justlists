#!/usr/bin/env python3
"""
Workshop Inventory Management System Launcher
Automatically starts the Flask server and opens the web browser
"""

import sys
import os
import threading
import time
import webbrowser
import socket
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# Import the Flask app
from app import app, init_db

def find_free_port():
    """Find a free port to run the Flask app"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def open_browser(port):
    """Open the web browser after a delay"""
    time.sleep(2)  # Wait for Flask to start
    url = f'http://localhost:{port}'
    print(f"Opening browser at: {url}")
    webbrowser.open(url)

def main():
    """Main launcher function"""
    print("=" * 60)
    print("🏭 WORKSHOP INVENTORY MANAGEMENT SYSTEM")
    print("=" * 60)
    print("Starting the application...")
    
    # Initialize the database
    try:
        print("📊 Initializing database...")
        init_db()
        print("✅ Database ready!")
    except Exception as e:
        print(f"❌ Database error: {e}")
        input("Press Enter to exit...")
        return
    
    # Find a free port
    port = 5000
    try:
        # Test if port 5000 is available
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(('localhost', port))
            if result == 0:
                print(f"⚠️  Port {port} is busy, finding alternative...")
                port = find_free_port()
                print(f"📡 Using port {port}")
            else:
                print(f"📡 Using default port {port}")
    except Exception as e:
        print(f"⚠️  Port check failed: {e}")
        port = find_free_port()
        print(f"📡 Using port {port}")
    
    # Start browser in a separate thread
    browser_thread = threading.Thread(target=open_browser, args=(port,))
    browser_thread.daemon = True
    browser_thread.start()
    
    print(f"🚀 Starting web server on http://localhost:{port}")
    print("🌐 Browser will open automatically...")
    print("\n" + "=" * 60)
    print("📝 DEFAULT LOGIN CREDENTIALS:")
    print("   Username: admin")
    print("   Password: admin123")
    print("=" * 60)
    print("\n⚠️  To stop the server, press Ctrl+C")
    print("🔒 Remember to change the default password!")
    
    try:
        # Run the Flask app
        app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        input("Press Enter to exit...")
    finally:
        print("👋 Goodbye!")

if __name__ == '__main__':
    main()