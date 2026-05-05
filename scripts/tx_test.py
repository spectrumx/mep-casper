import socket
import sys
from pathlib import Path

import casperfpga
import getmac
import numpy as np
from anyio import create_connected_udp_socket, create_task_group, run
from jsonargparse import auto_cli


async def snapshot(fpga, eth):
    rxsnap = fpga.snapshots[eth.snaps["rx"]]
    rxsnap.arm()
    try:
        rxdat = await rxsnap.read(arm=False, timeout=60)["data"]
        print(len(rxdat))
    except Exception as e:
        print(f"An error occurred trying to read the snapshot: {e}")


async def send_packet(host, port, packet_list, source_ip, source_port):
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
        async with await create_connected_udp_socket(
            remote_host=host,
            remote_port=port,
            local_host=source_ip,
            local_port=source_port,
            reuse_port=True,
        ) as udp:
            for ipn, ipkt in enumerate(packet_list):
                await udp.send(ipkt)
                print(f"Sent {ipn} of {len(packet_list)}")
        # # Create a socket object
        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # sock.bind((source_ip, source_port))  # Empty string = all interfaces
        # # Connect to the host and port
        # # sock.connect((host, port))

        # print(sock.getsockname())
        # # Send the packet
        # for ipn, ipkt in enumerate(packet_list):
        #     sock.sendto(ipkt, (host, port))
        #     print(f"Sent {ipn} of {len(packet_list)}")
        # # Close the socket
        # sock.close()

        return True

    except Exception as e:
        print(f"An error occurred while sending the packet: {e}")
        return False


async def run_test(fab_ip, port, pkt_list, s_host, s_port, fpga, eth):
    async with create_task_group() as tg:
        tg.start_soon(send_packet, fab_ip, port, pkt_list, s_host, s_port)


def send_packets(host, port, packet_list, source_ip, source_port):
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
        # async with await create_connected_udp_socket(
        #     remote_host=host,
        #     remote_port=port,
        #     local_host=source_ip,
        #     local_port=source_port,
        #     reuse_port=True,
        # ) as udp:
        #     for ipn, ipkt in enumerate(packet_list):
        #         await udp.send(ipkt)
        #         print(f"Sent {ipn} of {len(packet_list)}")
        # # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # sock.bind(("ens8191f1np1", source_port))  # Empty string = all interfaces

        # sock.setsockopt(
        #     socket.SOL_SOCKET, socket.SO_BINDTODEVICE, "ens8191f1np1\0".encode("utf-8")
        # )
        sock.bind((source_ip, source_port))
        # Connect to the host and port
        # sock.connect((host, port))

        print(sock.getsockname())
        # Send the packet
        print(f"Sending to {host}:{port}")
        for ipn, ipkt in enumerate(packet_list):
            sock.sendto(ipkt, (host, port))
            print(f"Sent {ipn} of {len(packet_list)}")
        # Close the socket
        sock.close()

        return True

    except Exception as e:
        print(f"An error occurred while sending the packet: {e}")
        return False


def setup_fpga(rfsoc_ip, firmfile):
    if not firmfile:
        firm_path = Path(__file__).parent.resolve().parent.joinpath("firmware")
        firm_list = list(firm_path.glob("rfsoc4x2_tengbeinout*.fpg"))
        firm_list.sort()
        firmfile = str(firm_list[-1])

    fpga = casperfpga.CasperFpga(rfsoc_ip)
    print(f"loading {firmfile}")
    fpga.upload_to_ram_and_program(firmfile)
    eth = fpga.gbes["gbe0"]

    return fpga, eth


def test_tx(
    fab_ip: str,
    port: int,
    mtu: int = 8000,
    s_host="192.168.5.10",
    s_port=10000,
    rfsoc_ip="hay-rfsoc-003.mit.edu",
    firmfile="",
):
    """Create a numypy array and then put that through the socket created form the address and port with the given MTU. Currently will only send a series of packets with a payload of 75% of the MTU.

    Parameters
    ----------
    fab_ip : str
        The address of the 10 Gbe fabric  where packets will be sent.
    port : int
        The port of the desired location.
    mtu : int
        The MTU setting of the connection
    s_host : str
        IP Address of host computer
    s_port : int
        Port of the host computer
    rfsoc_ip : str
        IP of the PS for the RFSoC that's running the casper image.
    firmfile : str
        Firmware file to be uploaded.
    """

    fpga, eth = setup_fpga(rfsoc_ip, firmfile)

    # setup network stuff
    fpga_mac = 0x123456780000
    pc_mac_str = getmac.get_mac_address(interface="ens8191f1np1")
    pc_mac = int(pc_mac_str.replace(":", ""), 16)

    eth.configure_core(fpga_mac, fab_ip, port)
    eth.set_single_arp_entry(fab_ip, fpga_mac)
    eth.set_single_arp_entry(s_host, pc_mac)

    bpw = 64
    iscomp = 0
    nsamps = 10000
    nbpnum = 16  # number of bits per number
    nbypnum = nbpnum // 8  # number of bytes per number
    npypsamp = nbypnum * (1 + iscomp)

    numsppkt = int(0.75 * mtu / npypsamp)

    rmd_bits = numsppkt * nbpnum % bpw

    sc_fa = 2 ** (nbpnum - 1)
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
        pkt_list.append(x1_int[cur_ind].tobytes())
    send_packets(fab_ip, port, pkt_list, s_host, s_port)
    # run(run_test, fab_ip, port, pkt_list, s_host, s_port, fpga, eth)


if __name__ == "__main__":
    import signal

    # handle SIGTERM (getting killed) gracefully by calling sys.exit
    def sigterm_handler(signal, frame):
        print("Killed")
        sys.stdout.flush()
        sys.exit(128 + signal)

    signal.signal(signal.SIGTERM, sigterm_handler)
    auto_cli(test_tx, as_positional=False)
