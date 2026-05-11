% First stage of decimation, this is 3 stages of half band filters that
% bring things down from 2 GHz to 250 MHz sampling. This is done to deal
% with the 

ds1_1 = 2;

a_1 = get_filter_ds_coefs(ds1_1,1,1);
a_2 = get_filter_ds_coefs(ds1_1,1,2);
a_3 = get_filter_ds_coefs(ds1_1,1,3);
%This is for the final stage of decimation. The ds is 
ds2_1 = 5;
ds2_2 = 5;
ds2_3 = 2;

b_1 = get_filter_ds_coefs(ds2_1,2,1);
b_2 = get_filter_ds_coefs(ds2_2,12,2);
b_3 =get_filter_ds_coefs(ds2_3,2,3);

ds2_1 = int32(ds2_1);
ds2_2 = int32(ds2_2);
ds2_3 = int32(ds2_3);
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
