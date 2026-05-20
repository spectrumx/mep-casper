# Setup and Install

md5 checksums
6180cef277ed84a6098e7ca9455b46e5  tcpborphserver3
c54b30b0cbe82f8dbb95fa138ee62dfb  librfdc.so.8.1

0. Kill any running instances of `tcpborphserver`

  `ps aux | grep borph`

  note the PID of the running tcpborphserver

  `kill -9 <PID>`

1. Install librfdc.so.8.1

  In the CASPER RFSoC4x2 Linux image, either replace `librfdc.so.1.1` at
  `/opt/local/lib` with this library, or copy `librfdc.so.8.1` to `/opt/local/lib`
  and update the `librfdc.so.1` symbolic link to point to this new library.

  `mv librfdc.so.8.1 /opt/local/lib/librfdc.so.1.1`

  or

  ```
  mv librfdc.so.8.1 /opt/local/lib/
  cd /opt/local/lib
  rm librfdc.so.1
  ln -s librfdc.so.8.1 librfdc.so.1
  ```

2. Install the new tcpborphserver, `tcpborphserver_v8.1`

  Replace the existing one at `/home/casper/bin/` renaming `tcpborphserver_v8.1`
  to `tcpborphserver3`  e.g.,

  `mv tcpborphserver_v8.1 /home/casper/bin/tcpborphserver3`

  make sure that tbs has the proper permissions to execute

  `chmod +x /home/casper/bin/tcpborphserver3`

3. Reboot the board

4. Start a telnet or netcat session with the platform (replace the board's ip address)

  `nc 192.168.2.100 7147`

5. Check the version of the library using the `?rfdc-driver-ver` command.
   Version 8.1 is expected to be returned

  ```
  #version-connect katcp-library v0.2.0-295-g5b314db-dirty 2024-01-11T03:34:31
  ##version-connect katcp-protocol 5.0-M
  ##version-connect kernel 5.4.0-xilinx-v2020.2
  ##1\_SMP\_Mon\_Aug\_15\_19:08:58\_UTC\_2022
  ?rfdc-driver-ver
  #rfdc-driver-ver version:\_8.100000
  !rfdc-driver-ver ok
  ```
