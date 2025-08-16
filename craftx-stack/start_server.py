"""
CraftX Server Startup Script
Handles port conflicts and ensures clean server startup
"""
import subprocess
import sys
import time
import psutil
import requests


def kill_process_on_port(port):
    """Kill any process using the specified port"""
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.info['connections']:
                if conn.laddr.port == port:
                    print(
                        f"🔄 Killing process {proc.info['pid']} ({proc.info['name']}) on port {port}")
                    proc.kill()
                    time.sleep(1)
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def check_server_running(port):
    """Check if server is running on port"""
    try:
        response = requests.get(f"http://localhost:{port}/", timeout=2)
        return True
    except:
        return False


def start_server():
    """Start the CraftX server with proper cleanup"""
    print("🚀 CraftX Server Startup")
    print("=" * 40)

    # Check for port conflicts
    ports_to_check = [8000, 8001, 8002]

    for port in ports_to_check:
        if check_server_running(port):
            print(f"⚠️  Port {port} is in use")
            kill_process_on_port(port)

    print("\n🔧 Starting CraftX server...")

    # Start the server
    try:
        subprocess.run([sys.executable, "craftx.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Server startup failed: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True

    return True


if __name__ == "__main__":
    start_server()
