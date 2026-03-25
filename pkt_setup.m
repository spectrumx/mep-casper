function [tspw,tspp,z_bits] = pkt_setup(bit_wrd,mtu,nchans,nbpn,is_comp,hdr_len)

bytpw= bit_wrd/8;%bytes per word
pkt_wrds = mtu/bytpw;

np_ts = is_comp+1;%numbers per time sample, basically if complex this is 2
npw = bit_wrd/nbpn;

tspw = npw/nchans/np_ts;
tspp = tspw*pkt_wrds;
word_lo = mod(hdr_len,bit_wrd);%left over word
z_bits = bit_wrd-word_lo;
