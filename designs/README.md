


## Header Control

Every packet needs a header that places information on the signal and recording. For the header to be read into a FIFO before the data is placed in the register, the data rate needs to be such that a header can be sent to the FIFO. Each word read into the FIFO for the 10 Gbe port needs to be 64 bits or 8 bytes. For the header format being used it is required that 8 words (512 bits,64 bytes) be placed in the FIFO first. This requires 8 clock cycles to read in the data to the FIFO.

Since 8 clock cylcles are required the largest sample rate that can be supported is an eigth of the clock rate. There is also an issue with the 

For example, this can be four 16 bit real samples or two 16 complex samples.


## Notes on Errors

This I'm calling a axi4lite_sw_reg_in_we error. This is 

```

-
ERROR: [Synth 8-2032] formal axi4lite_sw_reg_in_we is not declared [/home/jasper/simulink_models/roach_impl2/myproj/myproj.srcs/sources_1/imports/roach_impl2/axi4lite_ic_wrapper.vhdl:126]
INFO: [Synth 8-2810] unit struct ignored due to previous errors [/home/jasper/simulink_models/roach_impl2/myproj/myproj.srcs/sources_1/imports/roach_impl2/axi4lite_ic_wrapper.vhdl:80]
---------------------------------------------------------------------------------
Finished RTL Elaboration : Time (s): cpu = 00:00:01 ; elapsed = 00:00:01 . Memory (MB): peak = 2980.008 ; gain = 242.625 ; free physical = 37725 ; free virtual = 50233
---------------------------------------------------------------------------------
RTL Elaboration failed
INFO: [Common 17-83] Releasing license: Synthesis
11 Infos, 0 Warnings, 0 Critical Warnings and 2 Errors encountered.
synth_design failed
ERROR: [Common 17-69] Command failed: Synthesis failed - please see the console or run log file for details
INFO: [Common 17-206] Exiting Vivado at Wed Jun 12 13:22:37 2024...
[Wed Jun 12 13:22:41 2024] synth_1 finished
WARNING: [Vivado 12-8222] Failed run(s) : 'synth_1'
wait_on_run: Time (s): cpu = 00:04:01 ; elapsed = 00:02:05 . Memory (MB): peak = 2807.926 ; gain = 0.000 ; free physical = 39901 ; free virtual = 52409
# open_run synth_1
ERROR: [Common 17-69] Command failed: Run 'synth_1' failed. Unable to open
INFO: [Common 17-206] Exiting Vivado at Wed Jun 12 13:22:41 2024...
Traceback (most recent call last):
  File "/home/jasper/mlib_devel/jasper_library/exec_flow.py", line 239, in <module>
    backend.compile(cores=opts.jobs, plat=platform,
  File "/home/jasper/mlib_devel/jasper_library/toolflow.py", line 2329, in compile
    raise Exception('Vivado failed!')
Exception: Vivado failed!
Error using jasper (line 23)
Backend build failed! Check log files for more information

```


I'm calling something a top error here. If the build fails after `top: <file_name>` log then the input field to one of the software registers needs to be changed. It needs to be changed from a float to a hex or int.
