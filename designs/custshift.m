function z = custshift(x,y)
% cutshift implements a bit shift given by the parameter y. Basically saves
% from having to make an insane switch system in simulink. Positive y is a
% left shift, negative is a right shift.
%
%  Inputs:
%       x : A single number.
%       y : Number bits to shift x as an int. Positive is left shift,
%       negative is right shift.
%  Outputs: 
%       z : x bit shifted.
    if y==1
        z = xl_lsh(x,1);
    elseif y==2
        z = xl_lsh(x,2);
    elseif y==3
        z = xl_lsh(x,3);
    elseif y==4
        z = xl_lsh(x,4);
    elseif y==5
        z = xl_lsh(x,5);
    elseif y==6
        z = xl_lsh(x,6);
    elseif y==7
        z = xl_lsh(x,7);
    elseif y==8
        z= xl_lsh(x,8);
    elseif y==-1
        z = xl_rsh(x,1);
    elseif y==-2
        z = xl_rsh(x,2);
    elseif y==-3
        z = xl_rsh(x,3);
    elseif y==-4
        z = xl_rsh(x,4);
    elseif y==-5
        z = xl_rsh(x,5);    
    elseif y==-6
        z = xl_rsh(x,6);
    elseif y==-7
        z = xl_rsh(x,7); 
    elseif y==-8
        z = xl_rsh(x,8);    
    elseif y==-9
        z = xl_rsh(x,9);
    elseif y==-10
        z = xl_rsh(x,10);
    elseif y==-11
        z = xl_rsh(x,11);  
    elseif y==-12
        z = xl_rsh(x,12);  
    else
        z=x;
        
    end
 