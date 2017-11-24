% N= X(1)
% BG= X(2)
% I= X(3)
% Q= X(4)
%to:1:tf;
tspan = linspace(0,180, 100);
[t,Y] = ode45('Definitions',tspan ,[0.774 ; 5.1 ; 30 ; 18]);
plot(t,Y(:,2))
%plot(t,Y)
xlabel('time(min)')
%ylabel('mmol/l')
%legend('N(mmol/kg) ','BG(mmol/l)','I(mU/l)','Q(mU/l)')
legend('BG')   
