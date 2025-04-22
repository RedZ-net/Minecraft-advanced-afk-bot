import time
import threading
from minecraft.networking.connection import Connection
from minecraft.networking.packets import PositionAndLookPacket
from minecraft.networking.packets import ClientSettingsPacket

# Server configuration
SERVER_HOST = 'your.server.ip'
SERVER_PORT = 25565
USERNAME = 'BotUsername'

# Movement config
MOVE_INTERVAL = 0.1
JOIN_INTERVAL = 105  # 1 min 45 sec

def handle_join(connection):
    print("[+] Joined server!")

    # Send initial settings (to avoid some servers kicking)
    settings = ClientSettingsPacket()
    settings.locale = "en_US"
    settings.view_distance = 8
    settings.chat_mode = 0
    settings.chat_colors = True
    settings.displayed_skin_parts = 0x7f
    settings.main_hand = 1
    connection.write_packet(settings)

    # Start movement thread
    threading.Thread(target=movement_loop, args=(connection,), daemon=True).start()

def movement_loop(connection):
    jump = True
    y = 64  # Default Y level

    # Move forward and jump for 10 sec
    for _ in range(100):
        packet = PositionAndLookPacket()
        packet.x = 0
        packet.y = y + 1 if jump else y
        packet.z = 0
        packet.yaw = 0
        packet.pitch = 0
        packet.on_ground = not jump
        connection.write_packet(packet)
        jump = not jump
        time.sleep(MOVE_INTERVAL)

    # Move backward and jump for 10 sec
    for _ in range(100):
        packet = PositionAndLookPacket()
        packet.x = 0
        packet.y = y + 1 if jump else y
        packet.z = 1  # Backward movement
        packet.yaw = 180
        packet.pitch = 0
        packet.on_ground = not jump
        connection.write_packet(packet)
        jump = not jump
        time.sleep(MOVE_INTERVAL)

def start_bot():
    conn = Connection(SERVER_HOST, SERVER_PORT, username=USERNAME)
    conn.register_packet_listener(handle_join, 'join_game')

    try:
        conn.connect()
        print("[*] Connected.")
        time.sleep(JOIN_INTERVAL)
        conn.disconnect()
        print("[*] Disconnected. Waiting to rejoin...")
        time.sleep(JOIN_INTERVAL)
        start_bot()
    except Exception as e:
        print("[!] Error:", e)
        time.sleep(JOIN_INTERVAL)
        start_bot()

if __name__ == '__main__':
    start_bot()
