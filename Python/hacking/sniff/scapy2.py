from scapy.all import sniff, IP, TCP, UDP, Raw
import threading

packet_count = 0
sniffing = False
filter_ip = None
http_only = False

# ----------------------------
# HANDSHAKE TRACKER
# ----------------------------
seen_handshakes = set()


def is_new_handshake(packet):
    """
    Detect new TCP SYN handshake (first connection attempt)
    """
    if packet.haslayer(TCP):
        tcp = packet[TCP]

        # SYN flag = 0x02
        if tcp.flags == 0x02:
            connection_id = (
                packet[IP].src,
                packet[IP].dst,
                tcp.sport,
                tcp.dport,
            )

            if connection_id not in seen_handshakes:
                seen_handshakes.add(connection_id)
                return True

    return False


# ----------------------------
# PACKET PROCESSING
# ----------------------------
def process_packet(packet):

    global packet_count

    if not packet.haslayer(IP):
        return

    # Filter single IP if enabled
    if filter_ip:
        if packet[IP].src != filter_ip and packet[IP].dst != filter_ip:
            return

    # HTTP only (port 80)
    if http_only:
        if not packet.haslayer(TCP):
            return

        tcp = packet[TCP]
        if tcp.sport != 80 and tcp.dport != 80:
            return

    packet_count += 1

    print("\n" + "=" * 50)
    print(f"Packet #{packet_count}")

    source_ip = packet[IP].src
    destination_ip = packet[IP].dst

    print(f"Source IP: {source_ip}")
    print(f"Destination IP: {destination_ip}")

    # Protocol
    if packet.haslayer(TCP):
        print("Protocol: TCP")

        # Detect new handshake
        if is_new_handshake(packet):
            print(">>> NEW TCP HANDSHAKE DETECTED <<<")

    elif packet.haslayer(UDP):
        print("Protocol: UDP")
    else:
        print("Protocol: Other")

    # Payload
    if packet.haslayer(Raw):

        payload = packet[Raw].load

        print("\n--- Payload (Raw Bytes) ---")
        print(payload)

        try:
            decoded = payload.decode(errors="ignore")
            print("\n--- Payload (Readable Text) ---")
            print(decoded)
        except:
            print("Could not decode payload.")

    else:
        print("\nNo payload found.")

    print("=" * 50)


# ----------------------------
# SNIFF THREAD
# ----------------------------
def sniff_thread():
    global sniffing
    sniff(prn=process_packet, store=False, stop_filter=lambda x: not sniffing)


# ----------------------------
# START / STOP FUNCTIONS
# ----------------------------
def start_sniffing():

    global sniffing

    if sniffing:
        print("Already sniffing.")
        return

    sniffing = True
    print("\nStarting sniffing...\n")

    threading.Thread(target=sniff_thread, daemon=True).start()


def stop_sniffing():

    global sniffing

    if not sniffing:
        print("Not currently sniffing.")
        return

    sniffing = False
    print("Stopping sniffing...")


# ----------------------------
# MENU
# ----------------------------
def menu():

    global filter_ip
    global http_only

    while True:

        print("\n===== Packet Sniffer Menu =====")
        print("1. Start Scan (All Traffic)")
        print("2. Stop Scan")
        print("3. Scan Only One IP")
        print("4. Toggle HTTP Only")
        print("5. Exit")

        choice = input("Select option: ")

        if choice == "1":
            filter_ip = None
            start_sniffing()

        elif choice == "2":
            stop_sniffing()

        elif choice == "3":
            ip = input("Enter IP address: ")
            filter_ip = ip
            start_sniffing()

        elif choice == "4":
            http_only = not http_only
            print(f"HTTP Only Mode = {http_only}")

        elif choice == "5":
            stop_sniffing()
            break

        else:
            print("Invalid option.")


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    menu()
