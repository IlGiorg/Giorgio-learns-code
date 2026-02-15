from scapy.all import sniff, IP, TCP, UDP, Raw


packet_count = 0


def process_packet(packet):
    """Function called whenever a packet is captured"""

    global packet_count
    packet_count += 1

    print("\n" + "=" * 50)
    print(f"Packet #{packet_count}")

    # Check if packet has IP layer
    if packet.haslayer(IP):

        source_ip = packet[IP].src
        destination_ip = packet[IP].dst

        print(f"Source IP: {source_ip}")
        print(f"Destination IP: {destination_ip}")

        # Detect protocol
        if packet.haslayer(TCP):
            print("Protocol: TCP")

        elif packet.haslayer(UDP):
            print("Protocol: UDP")

        else:
            print("Protocol: Other")

    # Display payload if present
    if packet.haslayer(Raw):

        payload = packet[Raw].load

        print("\n--- Payload (Raw Bytes) ---")
        print(payload)

        # Try converting payload to readable text
        try:
            decoded_payload = payload.decode(errors="ignore")

            print("\n--- Payload (Readable Text) ---")
            print(decoded_payload)

        except:
            print("\nCould not decode payload as text.")

    else:
        print("\nNo payload found.")

    print("=" * 50)

def start_sniffing():
    """Start packet capture"""

    print("Starting packet listener...")
    print("Press CTRL + C to stop\n")

    sniff(prn=process_packet, store=False)


if __name__ == "__main__":
    start_sniffing()
