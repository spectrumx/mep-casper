import socket
import sys

import numpy as np
from jsonargparse import auto_cli


def send_packet(host, port, packet_list):
    """
    Send a packet to a specified host and port using a socket.

    Parameters
    ----------
    host : str
        The host to send the packet to.
    port : int
        The port to send the packet to.
    packet : bytes
        The packet to send.

    Returns:
    : bool
       True if the packet was sent successfully, False otherwise.
    """
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the host and port
        sock.connect((host, port))

        # Send the packet
        for ipn, ipkt in enumerate(packet_list):
            sock.sendall(ipkt)
            print(f"Sent {ipn} of {len(packet_list)}")
        # Close the socket
        sock.close()

        return True

    except Exception as e:
        print(f"An error occurred while sending the packet: {e}")
        return False


def test_tx(host: str, port: int, mtu: int = 8000):

    # Usage example

    packet = b"Hello, server!"
    nsamps = 10000
    nbpnum = 16
    nbypnum = nbpnum // 8
    sc_fa = 2 ** (nbpnum - 1)

    n = np.arange(nsamps, dtype=float)
    nper = 10.0
    x1 = sc_fa * np.cos(2 * np.pi * n / nper)
    x1_int = x1.astype(np.int16)
    if send_packet(host, port, packet):
        print("Packet sent successfully.")
    else:
        print("Failed to send packet.")


if __name__ == "__main__":
    import signal

    # handle SIGTERM (getting killed) gracefully by calling sys.exit
    def sigterm_handler(signal, frame):
        print("Killed")
        sys.stdout.flush()
        sys.exit(128 + signal)

    signal.signal(signal.SIGTERM, sigterm_handler)
    auto_cli(test_tx, as_positional=False)
