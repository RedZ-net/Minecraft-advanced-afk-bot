import os
import time
from minecraft.networking.connection import Connection

# Load from environment variables
SERVER_HOST = os.getenv("MC_SERVER_IP")
SERVER_PORT = int(os.getenv("MC_SERVER_PORT", 25565))
USERNAME = os.getenv("MC_USERNAME")

WAIT_AFTER_JOIN = 3         # Bot stays for 3 seconds
WAIT_BEFORE_REJOIN = 105    # 1 minute 45 seconds

def start_bot():
    while True:
        print("[*] Connecting to server...")
        try:
            conn = Connection(SERVER_HOST, SERVER_PORT, username=USERNAME)
            conn.connect()
            print("[+] Joined server. Staying for 3 seconds...")
            time.sleep(WAIT_AFTER_JOIN)
            conn.disconnect()
            print("[*] Disconnected. Waiting 1 minute 45 seconds before rejoining...")
            time.sleep(WAIT_BEFORE_REJOIN)
        except Exception as e:
            print("[!] Error:", e)
            print("[*] Retrying in 1 minute 45 seconds...")
            time.sleep(WAIT_BEFORE_REJOIN)

if __name__ == '__main__':
    start_bot()
