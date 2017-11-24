
t=0:.05:50; s=size(t);
for k=1:s(2)
Dvect(k)=2*dose(t(k));
end

plot(t,Dvect)
[t,Y] = ode23('drugRate',[0 50],[0;0]);
plot(t,Y)
xlabel('time(hrs)')
ylabel('Mg ml -1')
