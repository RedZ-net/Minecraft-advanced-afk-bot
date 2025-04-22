import os
import time
import threading
from minecraft.networking.connection import Connection
from minecraft.networking.packets.play.serverbound import (
    ClientSettingsPacket,
    PlayerPositionAndLookPacket,
)
from minecraft.networking.packets.play.clientbound import JoinGamePacket

# Load from environment variables
SERVER_HOST = os.getenv("MC_SERVER_IP")
SERVER_PORT = int(os.getenv("MC_SERVER_PORT", 25565))
USERNAME = os.getenv("MC_USERNAME")
MINECRAFT_VERSION = os.getenv("MC_VERSION", "1.16.5")

WAIT_AFTER_JOIN = 3         # Stay on server for 3 seconds
WAIT_BEFORE_REJOIN = 105    # 1 minute 45 seconds before rejoining
MOVE_INTERVAL = 0.1         # Movement timing

def handle_join(join_packet, connection):
    print("[+] Joined server!")

    settings = ClientSettingsPacket()
    settings.locale = "en_US"
    settings.view_distance = 8
    settings.chat_mode = 0
    settings.chat_colors = True
    settings.displayed_skin_parts = 0x7F
    settings.main_hand = 1
    connection.write_packet(settings)

    threading.Thread(target=movement_loop, args=(connection,), daemon=True).start()

def movement_loop(connection):
    jump = True
    y = 64

    for _ in range(30):
        packet = PlayerPositionAndLookPacket()
        packet.x = 0
        packet.y = y + 1 if jump else y
        packet.z = 0
        packet.yaw = 0
        packet.pitch = 0
        packet.on_ground = not jump
        connection.write_packet(packet)
        jump = not jump
        time.sleep(MOVE_INTERVAL)

    for _ in range(30):
        packet = PlayerPositionAndLookPacket()
        packet.x = 0
        packet.y = y + 1 if jump else y
        packet.z = -1
        packet.yaw = 180
        packet.pitch = 0
        packet.on_ground = not jump
        connection.write_packet(packet)
        jump = not jump
        time.sleep(MOVE_INTERVAL)

def start_bot():
    while True:
        print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT} as {USERNAME} with version {MINECRAFT_VERSION}...")
        try:
            conn = Connection(SERVER_HOST, SERVER_PORT, username=USERNAME, version=MINECRAFT_VERSION)
            conn.register_packet_listener(handle_join, JoinGamePacket)
            conn.connect()
            print("[+] Successfully joined the server.")
            time.sleep(WAIT_AFTER_JOIN)
            conn.disconnect()
            print("[*] Left server. Waiting 1 minute 45 seconds before rejoining...")
            time.sleep(WAIT_BEFORE_REJOIN)
        except Exception as e:
            print("[!] Error occurred:", e)
            print("[*] Retrying in 1 minute 45 seconds...")
            time.sleep(WAIT_BEFORE_REJOIN)

if __name__ == '__main__':
    start_bot()
