%Patient data
Height = 1.80;
W = 80;
Age = 32;
Sex = 1;
%%%%%%%%%%%%%%

ABSA = (Height * W / 36,2)^1/2;
F = 0.76
lhl = 29.2 + 0.14 * Age
shl = 4.95
aa = log(2) / shl
b = log(2) / lhl
k2 = F * (b - aa) + aa
nk = aa * b / k2
k1 = aa + (b - k2 - nk)
if Sex = 1
	VP = 1.11 * ABSA + 2.04
else
	VP = 1.92 * ABSA + 0.64


VQ = k1 / k2 * VP
mgut = (1/2)
J1plus3 = 0.0093
Km1plus3 = 1.5
J4 = 0.0848
BGthresh = 11.98
Ah = -0.0007
Bh = -0.0247
Ch = 0.0223
Vbg = W * 0.19
k = 0.539
C = 98.1
gamma = (5/3)
d = 1.77
p0 = 0.083
mC = 2.75
mI = 5.8
nI = VP * k1 * (mC / mI)
nkl = W / (C - (1 - gamma) * nI) * (1 / VP)
nC = (gamma - 1) * nI / VQ
FG = 0.0694 * ABSA
Tmax = 2
KM4 = 5
pInitial0 = gamma / C * 18
iaster0 = (pInitial0 - p0) / ((pInitial0 - p0)^d + k^d )^1/d

t=0:.05:50; s=size(t);
for k=1:s(2)
Dvect(k)=2*dose(t(k));
end

plot(t,Dvect)
[t,Y] = ode23('drugRate',[0 50],[0;0]);
plot(t,Y)
xlabel('time(hrs)')
ylabel('Mg ml -1')
