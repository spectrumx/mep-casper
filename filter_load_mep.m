% First stage of decimation, this is 3 stages of half band filters that
% bring things down from 1.9 GHz to 250 MHz sampling. This is done to improve
% the dynamic range by doing lots of oversampling from the RFSoC first. 
clk_freq=245760000;

% Down sample for filter set a stage 1. All of the stages are the same
% since the SSR type filtering is being used.
dsa_1 = 2;

a_1 = get_filter_ds_coefs(dsa_1,1,1);
a_2 = get_filter_ds_coefs(dsa_1,1,2);
a_3 = get_filter_ds_coefs(dsa_1,1,3);

%This is for the final stage of decimation. The ds is 

ds0_b_1 = 5;
ds0_b_2 = 5;
ds0_b_3 = 2;

b0_1 = get_filter_ds_coefs(ds0_b_1,2,1);
b0_2 = get_filter_ds_coefs(ds0_b_2,12,2);
b0_3 = get_filter_ds_coefs(ds0_b_3,2,3);


ds1_b_1 = 5;
ds1_b_2 = 5;
ds1_b_3 = 2;

b1_1 = get_filter_ds_coefs(ds1_b_1,2,1);
b1_2 = get_filter_ds_coefs(ds1_b_2,12,2);
b1_3 = get_filter_ds_coefs(ds1_b_3,2,3);


ds_clk_0 = ds0_b_1*ds0_b_2*ds0_b_3;
ds_clk_1 = ds1_b_1*ds1_b_2*ds1_b_3;

sr_0 = floor(clk_freq/ds_clk_0);
sr_1 = floor(clk_freq/ds_clk_1);

dsa_1 = int32(dsa_1);
ds0_b_1 = int32(ds0_b_1);
ds0_b_2 = int32(ds0_b_2);
ds0_b_3 = int32(ds0_b_3);

ds1_b_1 = int32(ds1_b_1);
ds1_b_2 = int32(ds1_b_2);
ds1_b_3 = int32(ds1_b_3);
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
