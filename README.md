# mep-casper
CASPER SDR image for the RFSoC 4x2 used by the SpectrumX MEP

## Header Control

Every packet needs a header that places information on the signal and recording. For the header to be read into a FIFO before the data is placed in the register, the data rate needs to be such that a header can be sent to the FIFO. Each word read into the FIFO for the 10 Gbe port needs to be 64 bits or 8 bytes. For the header format being used it is required that 8 words (512 bits,64 bytes) be placed in the FIFO first. This requires 8 clock cycles to read in the data to the FIFO.

Since 8 clock cylcles are required the largest sample rate that can be supported is an eigth of the clock rate. There is also an issue with the 

For example, this can be four 16 bit real samples or two 16 complex samples. 

