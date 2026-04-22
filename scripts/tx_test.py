import socket
import sys

import numpy as np
from jsonargparse import auto_cli


def send_packet(host, port, packet_list, source_ip, source_port):
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
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind((source_ip, source_port))  # Empty string = all interfaces
        # Connect to the host and port
        # sock.connect((host, port))

        print(sock.getsockname())
        # Send the packet
        for ipn, ipkt in enumerate(packet_list):
            sock.sendto(ipkt, (host, port))
            print(f"Sent {ipn} of {len(packet_list)}")
        # Close the socket
        sock.close()

        return True

    except Exception as e:
        print(f"An error occurred while sending the packet: {e}")
        return False


def test_tx(host: str, port: int, mtu: int = 8000, s_host="192.168.5.10", s_port=60000):
    """Create a numypy array and then put that through the socket created form the address and port with the given MTU. Currently will only send a series of packets with a payload of 75% of the MTU.

    Parameters
    ----------
    host : str
        The address of the location where this will be sent.
    port : int
        The port of the desired location.
    mtu : int
        The MTU setting of the connection
    """

    nsamps = 10000
    nbpnum = 16
    nbypnum = nbpnum // 8
    sc_fa = 2 ** (nbpnum - 1)
    numsppkt = int(0.75 * mtu / nbypnum)

    n = np.arange(nsamps, dtype=float)
    nper = 40.0
    x1 = sc_fa * np.cos(2 * np.pi * n / nper)
    x1[x1 >= sc_fa] = sc_fa - 1
    x1[x1 <= -1 * sc_fa] = -1 * sc_fa
    x1_int = x1.astype(np.int16)
    nnums = len(x1_int)
    n_els = int(np.ceil(nnums / numsppkt))
    pkt_list = []
    for ilist in range(n_els):
        cur_ind = np.arange(ilist * numsppkt, (ilist + 1) * numsppkt)
        cur_ind = cur_ind[cur_ind < nnums]
        pkt_list.append(x1_int[cur_ind])

    if send_packet(host, port, pkt_list, s_host, s_port):
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
