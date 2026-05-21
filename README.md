# mep-casper
CASPER SDR image for the RFSoC 4x2 used by the SpectrumX MEP


## Set up

This repository contains material related to the CASPER based firmware development for the Mobile Experiment Platform (MEP). The following folders in the repository contain the following

* designs
  * These are simulink files that represent firmware design. To build this design a CASPER development environment is required.
* scripts
  * These are mainly python files to run the built firmware to test and run the images.
* firmware
  * Built firmware images. Both the fpg and dtbo files are needed to run an image.

### Configure ARP tables

With rfsoc object (e.g `rfsoc = rec_setup.RFSOC4x2("192.168.20.60")`),
```
ip = "192.168.4.1"  # destination IP address
mac = 0x6c92bf4254ba  # substitute destination MAC address
port = 60000
rfsoc.gbes.gbe0.configure_core(mac, ip, port)
rfsoc.gbes.gbe0.set_single_arp_entry(ip, mac)
```
