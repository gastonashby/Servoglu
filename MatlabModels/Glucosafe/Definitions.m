function Yprime=drugRate(t,X)

N= X(1);
BG= X(2);
I= X(3);
Q= X(4);


    function e=e()
        e=0;
        if (N > 8.65)
            e= 0.03245 * mgut;
        else
            e = (0.000433 * (N^2) + 0.0075 * N) * mgut;
        end
    end

    function H=H()
        H=0;
        if (BG <= BGthresh)
            H= Ah * BG + Bh * a( ) + Ch;
        else
            H= Ah * BGthresh + Bh * a( ) + Ch;
        end
    end

    function Pglut1plus3=Pglut1plus3()
        Pglut1plus3 = J1plus3 * BG / ( BG + Km1plus3);
    end

    function Pglut4=Pglut4()
        Pglut4= J4 * BG / ( BG + KM4) * a( );
    end

    function R=R()
        R= max( 0, ( FG * BG - Tmax) / W);
    end

    function E=E()
        E=H( ) - R( ) - Pglut4( ) - Pglut1plus3( );
    end

    function a=a()
        a= i( ) * s ;
    end

    function i=i()
        i=( iaster( ) - iaster0) / ( 1 - iaster0);
    end

    function iaster=iaster()
        iaster=(p() - p0) / ((p() - p0)^ d + k^d)^(1/d) ;
    end

    function p=p()
        p= gamma / C * Q ;
    end


    function U=U()
        U=0;
        if (DiabetesTypeOne == 0)
            U= 42;
        else
            U= 0;
        end
    end

%Patient 93 data
Height = 1.85;
W = 102;
Age = 36;
Sex = 0;
DiabetesTypeOne = 0;
%%%%%%%%%%%%%%%%%%%%%%%

%Treatments

if (t < 60)
    ecf = 0;
    Ex = 110;
    z = 0;
    s = 0.45;
elseif ((t > 60) && (t < 120))
    ecf = 0;
    Ex = 90;
    z = 0;
    s = 0.5;
else
    ecf = 0;
    Ex = 75;
    z = 0;
    s = 0.5;
end
%%%%%%%%%%%%%%%%%


ABSA = (Height * W / 36.2)^(1/2);
F = 0.76;
lhl = 29.2 + 0.14 * Age;
shl = 4.95;
aa = log(2) / shl;
b = log(2) / lhl;
k2 = F * (b - aa) + aa;
nk = aa * b / k2;
k1 = aa + (b - k2 - nk);
if Sex == 1
    VP = 1.11 * ABSA + 2.04;
else
    VP = 1.92 * ABSA + 0.64;
end

VQ = k1 / k2 * VP;
mgut = (1/2);
J1plus3 = 0.0093;
Km1plus3 = 1.5;
J4 = 0.0848;
BGthresh = 11.98;
Ah = -0.0007;
Bh = -0.0247;
Ch = 0.0223;
Vbg = W * 0.19;
k = 0.539;
C = 98.1;
gamma = (5/3);
d = 1.77;
p0 = 0.083;
mC = 2.75;
mI = 5.8;
nI = VP * k1 * (mC / mI);
nkl = W / (C - (1 - gamma) * nI) * (1 / VP);
nC = (gamma - 1) * nI / VQ;
FG = 0.0694 * ABSA;
Tmax = 2;
KM4 = 5;
pInitial0 = gamma / C * 18;
% numerador = (pInitial0 - p0)^d
% denominador1 = (pInitial0 - p0)^d + k^d
% denominador = ((pInitial0 - p0)^d + k^d )^(1/d)
iaster0 = (pInitial0 - p0) / ((pInitial0 - p0)^d + k^d )^(1/d);

fprintf('t: %.5f ', t);
fprintf('e(): %.5f ', e());
fprintf('E(): %.5f ', E());
fprintf('Pglut4(): %.5f ', Pglut4());
fprintf('a(): %.5f ', a());
fprintf('iaster(): %.5f ', iaster());
fprintf('iaster0: %.5f ', iaster0);
fprintf('BG: %.5f \n', BG);


Yprime=[-e() + ecf;
    (e() + z + E()) * W / Vbg;
    -nkl * I - nI / VP * (I - Q) + (Ex + U()) / VP
    -nC * Q + nI / VQ * (I - Q)];


%Yprime=[-a*x(1)+2*dose(t); a*x(1)-b*x(2)];
end
