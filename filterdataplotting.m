function [pxx_db,fvec] = filterdataplotting(indata,winlen,nfft)


ts = indata.TimeInfo.Increment;
fs = 1/ts;
xdata = indata.Data;
kwin = kaiser(winlen,1.7*pi);
noverlap = winlen/4;
fvec = fftfreq(nfft,ts,ts);
[pxx,fvec] = pwelch(xdata,kwin,noverlap,fvec,1/ts);

pxx_db = pow2db(pxx);