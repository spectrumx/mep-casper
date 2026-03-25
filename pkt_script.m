% For full builds
bit_wrd = 64; %bits per word for packets
is_comp = 1;% Complex
np_ts = is_comp+1;%numbers per time sample, basically if complex this is 2
nchans = 8;% number of channels

nbpn = 16;%bits per number
npw = bit_wrd/nbpn;
pkt_wrds = 64;

tspw8 = npw/nchans/np_ts;
tspp8 = tspw8*pkt_wrds;
% Single channel simulations
pkt_wrds1 = 64;
tspw1 = npw/np_ts;
tspp1 = tspw1*pkt_wrds1;