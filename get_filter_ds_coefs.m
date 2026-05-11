function coefs = get_filter_ds_coefs(ds,fset,fstage)
% Determines the filter coefficents given 
%
%  Inputs:
%       ds : Down sampling rate
%       fset : Number bits to shift x as an int. Positive is left shift,
%       negative is right shift.
%  Outputs: 
%      coefs : filter coeffiecents
    if fset==1
        const1 = 5;
        const2 = 10;
        const3 = 21;
    else
        const1 =5;
        const2 = 24;
        const3 = 24;
    end
  
    
    if fstage==1
        Mlen = ds*const1;
    elseif fstage==2
        Mlen = ds*const2;
    else
        Mlen = ds*const3;
    end
    Mlen = Mlen-(1-mod(Mlen,2));
    coefs = fir1(Mlen-1,1/ds,kaiser(Mlen,1.7*pi));
        