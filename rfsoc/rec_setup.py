# !python
import time
from pathlib import Path

import casperfpga
import numpy as np
import paho.mqtt.client as mqtt
import schedule


class RFSOC4x2(casperfpga.CasperFpga):
    def __init__(self, rfsoc_addr):
        """
        Parameters
        ----------
        rfsoc_addr : str
            Address of the rfsoc, make sure if IP its a string
        """
        super().__init__(host=rfsoc_addr)

    def start_up(
        self,
        fpgfile,
        pps_sync=False,
        reflock=False,
        log_func=print,
        clk_files=None,
        cold_start=True,
        des_ip="192.168.5.10",
        des_port=60000,
    ):
        """Start the RFSoC given the write host name, fpga file and clock file. The clockfiles determine if it will be locked to a reference frequency.

        Parameters
        ----------
        fpgfile : str
            Basically bit file. Give it a .fpg file name and make theres a file with the same stem but .dtbo suffix.
        pps_sync : bool
            Runs the set time  function if set to true.
        reflock : bool
            Determines what clock file will be uploaded
        log_func : func
            A function to output logging.
        clk_file : str
            This can be used to over ride the clock file choice.
        cold_start : bool
            This will load the clock file and then reload the firmware. The clock files needs to reloaded to the ADCs after each start.

        """

        # This is the default clock files in the 4x2.
        if clk_files is None:
            clk_files = [
                "rfsoc4x2_LMX_REF_245M76_OUT_491M52.txt",
                "rfsoc4x2_PL_122M88_REF_245M76.txt",
            ]

        log_func(f"Uploading FPGA image {fpgfile}")
        if not self.upload_to_ram_and_program(fpgfile):
            raise RuntimeError("Failed to upload FPGA image")
        # time.sleep(10)
        # Start the ADC clocks on the RFSoC
        if cold_start:
            # if starting up from cold
            log_func("Running from cold start, uploading adc clock file")
            rfdc = self.adcs["rfdc"]

            c = rfdc.show_clk_files()

            for iclk_file in clk_files:
                if iclk_file not in c:
                    clk_list = "\n".join(c)
                    raise ValueError(
                        f"{iclk_file} not listed as one of the following: \n{clk_list}"
                    )
            log_func(f"Loading clock file {clk_files}")
            if not rfdc.progpll("lmx", clk_files[0]):
                raise RuntimeError("Failed to load lmx clock file")
            if not rfdc.progpll("lmk", clk_files[1]):
                raise RuntimeError("Failed to load lmk clock file.")

            # time.sleep(5)
            log_func("Initializing rfdc driver")
            if not rfdc.init():
                raise RuntimeError("Failed to initialize rfdc driver")
            # time.sleep(5)
            num_tries = 3
            for k_try in range(num_tries):
                log_func("Checking ADC/DAC status")
                try:
                    adc_status = rfdc.status()
                except Exception:
                    if k_try + 1 >= num_tries:
                        raise
                else:
                    log_func(f"ADC/DAC status: {adc_status}")

            # HACK need to reupload program again because clock file is causing issues with packets
            if not self.upload_to_ram_and_program(fpgfile):
                raise RuntimeError("Failed to upload FPGA image")

        # time.sleep(5)
        self.write_int("word_per_pkt", 1000)
        log_func("Setting IP and port.")
        self.set_rec_addr(ip_out=des_ip, port_out=des_port, log_func=log_func)
        log_func("Setting time at PPS edge")
        utc_time = self.set_time(log_func)
        if pps_sync or reflock:
            hold_time = 5
            time.sleep(hold_time)
            log_func("Checking PPS Avaliblilty")
            pps_time, clcktime, clockcyles = self.get_times()
            clockutcdiff = clcktime - utc_time
            pps_diff = pps_time - utc_time
            pps_fail = pps_diff < 3 or pps_diff > 50
            if pps_sync and pps_fail:
                log_func(
                    f"Check PPS, does not seem to sync, with this difference in seconds: {pps_diff}"
                )
            elif pps_sync:
                log_func("PPS found ")

            if reflock:
                log_func("Used clock file fo ref lock")

    def get_times(self):
        """Get the current times in the program.

        Returns
        -------
        pps_time : int
            UTC time in seconds according to a pps count with original utc input.
        clock_time : int
            UTC time in seconds according to a clock sycle counter added to the utc input.
        clockcycles : int
            Remander clock cycles from the clock time counter.
        """

        pps_time = self.read_int("timefrompps")
        # writes a time check bool to freeze the current local clock cycles to a buffer
        self.write_int("time_check", 1)
        time.sleep(1)
        clocktime = self.read_int("localclocksec")
        clockcycles = self.read_int("localclockcycles")
        time.sleep(1)
        self.write_int("time_check", 0)
        return pps_time, clocktime, clockcycles

    def stop_packets(self):
        """Stops the packets being transmitted.

        HACK Does not stop the ADCs in the current design.

        Parameters
        ----------
        zcu208 : casperfpga obj
            This is the object that CASPER uses to upload commands to the FPGA.
        """
        self.write_int("rst", 3)

    def set_freq(self, desired_freq, log_func=print, set_the_time=False):
        """Sets the center frequency of desired channel

        Parameters
        ----------

        desired_freq : float
            Desired center frequency in Hz
        """

        clk_freq_Hz = 245.76e6
        rot1 = 2**19
        p_inc_dec = desired_freq * rot1 // clk_freq_Hz
        freq_actual = p_inc_dec * clk_freq_Hz / rot1
        self.write_int("pinc_dec", int(p_inc_dec))
        log_func(
            f"Center frequency asked for {desired_freq} Hz \nActual Tuned frquency: {freq_actual} Hz"
        )
        if set_the_time:
            _ = self.set_time(log_func)

    def set_time(self, log_func=print):
        """Sets time to the second using pps."""
        utc_time = time.time()
        utc_int = int(utc_time)
        # Hold till we get 2 seconds out
        while time.time() < utc_int + 2:
            pass
        # Write the next utc time This will start everything
        self.write_int("UTC", utc_int + 3)
        timestr = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(utc_int))
        log_func(f"Set pps to {timestr}")
        return utc_int + 3

    def restart_packets(self, log_func=print):
        """Restarts the packets and updates the utc time.

        Parameters
        ----------
        log_func : func
            Function for logging.
        """
        self.write_int("rst", 0)
        log_func("Restarting packets.")
        _ = self.set_time(log_func)

    def set_bitshift(self, bs_int, log_func=print):
        """Set the bitshift for one of the channels on the rfsoc.

        Parameters
        ----------
        bs_int : int
            Desired bitshift, negative is right shift, positive is left shift.
        log_func : func
            The logging function.

        """
        assert -12 <= bs_int <= 8, f"Bit shift must be between -12 and 8, got: {bs_int}"
        self.write_int("bitshift0", bs_int)
        log_func(f"Bit shift for set to {bs_int}")

    def set_rec_addr(self, ip_out, port_out, log_func=print):
        """Set the address of the output data.

        Parameters
        ----------
        ip_port : str
            The ip address for the output
        port_out : int
            The port out.
        log_func : func
            The logging function.
        """
        val = 2 ** np.array([24, 16, 8, 0])
        ippint = sum(np.array([int(i) for i in ip_out.split(".")]) * val)
        self.write_int("des_ip", ippint)
        log_func(f"Destination IP address set to: {ip_out}")
        self.write_int("des_port", port_out)
        log_func(f"Destination Port set to: {port_out}")

    def better_clock_est(self, nsecs=20, slptime=1):
        """Clock estimation method from Russ, will take some time to run.

        Parameters
        ----------
        nsecs : int
            Number of seconds to run the estimation.
        slptime : float
            Time between reading the sys_clkcounter.

        Returns
        -------
        clk_MHz : float
            The clock estimate in MHz.
        """
        s = []
        t = []
        for i in range(0, nsecs):
            s.append(self.read_uint("sys_clkcounter"))
            t.append(time.perf_counter())
            time.sleep(slptime)
        d = np.diff(s)
        d[d < 0] += 2**32

        clk_MHz = sum(d) / (t[-1] - t[0]) / 1e6 / slptime
        return clk_MHz


def rfsoc_rx_sched(rf_addr="hay-rfsoc-003.mit.edu"):
    """This is running a simple start up of the RFSoC firmware and schedules the time to set every hour to avoid drift between different systems."""
    # rf_addr = "10.112.0.25"
    # Address for system on desk

    fname_rel = Path(__file__).absolute().parent / "firmware"
    flist = list(fname_rel.glob("single_chan_rx*.fpg"))
    flist.sort()
    # use the newest firmware
    fnamepath = flist[-1]
    rfsoc = RFSOC4x2(rf_addr)
    rfsoc.start_up(str(fnamepath), pps_sync=True, reflock=True, cold_start=True)
    rfsoc.set_freq(desired_freq=100000000)
    schedule.every().hour.at("59:57").do(rfsoc.set_time)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    rf_addr = "hay-rfsoc-003.mit.edu"
    rfsoc_rx_sched(rf_addr)
