function Yprime=drugRate(t,x) 
    a=2*log(2); b=log(2)/5;
    Yprime=[-a*x(1)+2*dose(t); a*x(1)-b*x(2)];
end
