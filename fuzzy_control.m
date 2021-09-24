clear; clc; close all;

fis = mamfis('Name',"PD control");

emax = 15;
edotmax = 6;
umax = 50;

k = emax;
fis = addInput(fis,[-emax emax],'Name',"e");
fis = addMF(fis,"e","trapmf",[-k -k -k*3/4 -k/2],'Name',"NB");
fis = addMF(fis,"e","trimf",[-k*3/4 -k/2 -k/4],'Name',"NM");
fis = addMF(fis,"e","trimf",[-k/2 -k/4 0],'Name',"NS");
fis = addMF(fis,"e","trimf",[-k/4 0 k/4],'Name',"ZO");
fis = addMF(fis,"e","trimf",[0 k/4 k/2],'Name',"PS");
fis = addMF(fis,"e","trimf",[k/4 k/2 k*3/4],'Name',"PM");
fis = addMF(fis,"e","trapmf",[k/2 k*3/4 k k],'Name',"PB");

k = edotmax;
fis = addInput(fis,[-edotmax edotmax],'Name',"edot");
fis = addMF(fis,"edot","trapmf",[-k -k -k*3/4 -k/2],'Name',"NB");
fis = addMF(fis,"edot","trimf",[-k*3/4 -k/2 -k/4],'Name',"NM");
fis = addMF(fis,"edot","trimf",[-k/2 -k/4 0],'Name',"NS");
fis = addMF(fis,"edot","trimf",[-k/4 0 k/4],'Name',"ZO");
fis = addMF(fis,"edot","trimf",[0 k/4 k/2],'Name',"PS");
fis = addMF(fis,"edot","trimf",[k/4 k/2 k*3/4],'Name',"PM");
fis = addMF(fis,"edot","trapmf",[k/2 k*3/4 k k],'Name',"PB");

k = umax;
fis = addOutput(fis,[-umax umax],'Name',"u");
fis = addMF(fis,"u","trapmf",[-k -k -k*3/4 -k/2],'Name',"NB");
fis = addMF(fis,"u","trimf",[-k*3/4 -k/2 -k/4],'Name',"NM");
fis = addMF(fis,"u","trimf",[-k/2 -k/4 0],'Name',"NS");
fis = addMF(fis,"u","trimf",[-k/4 0 k/4],'Name',"ZO");
fis = addMF(fis,"u","trimf",[0 k/4 k/2],'Name',"PS");
fis = addMF(fis,"u","trimf",[k/4 k/2 k*3/4],'Name',"PM");
fis = addMF(fis,"u","trapmf",[k/2 k*3/4 k k],'Name',"PB");

subplot(311);
plotmf(fis,'input',1)
subplot(312);
plotmf(fis,'input',2)
subplot(313);
plotmf(fis,'output',1)

ruleList = [4 1 1 1 1;
            4 2 2 1 1;
            4 3 3 1 1;
            4 4 4 1 1;
            4 5 5 1 1;
            4 6 6 1 1;
            4 7 7 1 1;
            1 4 1 1 1;
            2 4 2 1 1;
            3 4 3 1 1;
            5 4 5 1 1;
            6 4 6 1 1;
            7 4 7 1 1];

fis = addRule(fis,ruleList);

fis.Rules

figure()
gensurf(fis);

s = tf('s');
G = 3/(30*s+1);
figure();
step(G);

dt=0.1;
ts=0:dt:30;
r=ones(length(ts));
ys = [0];
es = [0];
us = [0];
for i=1:length(ts)
    r_i = r(i);
    y_i = ys(end);
    u_i = us(end);
    e_last = es(end);
    e_i = r_i-y_i;
    edot_i = e_last - e_i;
    du = evalfis(fis,[e_i,edot_i]);
    u_i = u_i+du;
    y = lsim(G, [u_i 0], [0 dt]);
    y = y(2);
    ys(end+1) = y;
    es(end+1) = e_i;
    us(end+1) = u_i;
end

figure();
subplot(311);
plot(ts,ys(2:end));
legend('y');
title('y');
subplot(312);
plot(ts,es(2:end));
legend('e');
title('e');
subplot(313);
plot(ts,us(2:end));
legend('u');
title('u');

figure();
plot(ts,ys(2:end),'r');
hold on;
C=pidtune(G,'pi');
step(feedback(G*C,1));
legend('Fuzzy-PI','PI')

big;

