% First stage of decimation, this is 3 stages of half band filters that
% bring things down from 2 GHz to 250 MHz sampling. This is done to deal
% with the 
ds1 = 2;
M1 = ds1*5;
M1 = M1-(1-mod(M1,2));
M2 = ds1*10;
M2 = M2-(1-mod(M2,2));
M3 = ds1*21;
M3 = M3-(1-mod(M3,2));

a_1 = fir1(M1-1,1/ds1,kaiser(M1,1.7*pi));
a_2 = fir1(M2-1,1/ds1,kaiser(M2,1.7*pi));
a_3 = fir1(M3-1,1/ds1,kaiser(M3,1.7*pi));
%This is for the final stage of decimation. The ds is 
ds = 5;
N1 = ds*5;
N1 = N1-(1-mod(N1,2));
N2 = ds*24;
N2 = N2- (1-mod(N2,2));
N3 = N2;
N3 = N3- (1-mod(N3,2));

b_1 = fir1(N1,1/ds,kaiser(N1+1,1.7*pi));
b_2 = fir1(N2,1/ds,kaiser(N2+1,1.7*pi));
b_3 = fir1(N3,1/ds,kaiser(N3+1,1.7*pi));



% For full builds
bit_wrd = 512;
nbps = 16;
spw = bit_wrd/nbps;
pkt_wrds = 64;
tspw8 = spw/8/2;
tspp8 = tspw8*pkt_wrds;
% Single channel simulations
pkt_wrds1 = 64;
tspw1 = spw/1/2;
tspp1 = tspw1*pkt_wrds1;
