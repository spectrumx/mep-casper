#!python
#

import casperfpga
import numpy as np


def setupfpga(rfsocadd="hay-rfsoc-003.mit.edu", ip_pc="192.168.5.10", port_pc=60000):
    fpga = casperfpga.CasperFpga("hay-rfsoc-003.mit.edu")
    fpga.upload_to_ram_and_program("rfsoc4x2_tengbe_2026-02-03_1636.fpg")
    val = 2 ** np.array([24, 16, 8, 0])
    ippint = sum(np.array([int(i) for i in ip_pc.split(".")]) * val)
    fpga.write_int("dest_ip", ippint)
    fpga.write_int("dest_port", port_pc)
    fpga.write_int("rst", 3)
    fpga.write_int("rst", 0)

    fpga.write_int("pkt_sim_enable", 0)
    fpga.write_int("pkt_sim_payload_len", 50)
    fpga.write_int("pkt_sim_period", 100000000)
    fpga.write_int("pkt_sim_enable", 1)
    return fpga
