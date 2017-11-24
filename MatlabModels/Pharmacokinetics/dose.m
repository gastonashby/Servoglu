 function H=dose(t)
 H=0;
 for n=0:50
    if(t >= 6*n)&(t < 6*n+.5)
        H=1;
 end
 end