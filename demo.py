from control.matlab import *
import matplotlib.pyplot as plt
import pdb
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np

s = tf('s')
G = 1/(0.8+0.3*s+s**2)
y, t = step(G)
# plt.plot(t,y)
r = np.ones_like(t)
es = [0]
edots = [0]
for i in range(len(t)):
    ri = r[i]
    yi = y[i]
    ei = yi-ri
    elast = es[-1]
    edot_i = ei - elast
    es.append(ei)
    edots.append(edot_i)

# plt.figure(2)
# plt.plot(t,es[1:])
# plt.figure(3)
# plt.plot(t,edots[1:])
# pdb.set_trace()
# exit()
#PD controller
emax = 1
edotmax = 0.2
umax = 10 
e = ctrl.Antecedent(np.arange(-emax, emax, 0.01), 'e')
edot = ctrl.Antecedent(np.arange(-edotmax, edotmax, 0.001), 'edot')
u = ctrl.Consequent(np.arange(-umax, umax, 0.1), 'u')

k=emax
e["NB"] = fuzz.trapmf(e.universe, [-k,-k, -k*3/4, -k/2])
e["NM"] = fuzz.trimf(e.universe, [-k*3/4, -k/2, -k/4])
e["NS"] = fuzz.trimf(e.universe, [-k/2, -k/4, 0])
e["ZO"] = fuzz.trimf(e.universe, [-k/4, 0, k/4])
e["PS"] = fuzz.trimf(e.universe, [0, k/4, k/2])
e["PM"] = fuzz.trimf(e.universe, [k/4, k/2, k*3/4])
e["PB"] = fuzz.trapmf(e.universe, [k/2, k*3/4, k, k])

k=edotmax
edot["NB"] = fuzz.trapmf(edot.universe, [-k,-k, -k*3/4, -k/2])
edot["NM"] = fuzz.trimf(edot.universe, [-k*3/4, -k/2, -k/4])
edot["NS"] = fuzz.trimf(edot.universe, [-k/2, -k/4, 0])
edot["ZO"] = fuzz.trimf(edot.universe, [-k/4, 0, k/4])
edot["PS"] = fuzz.trimf(edot.universe, [0, k/4, k/2])
edot["PM"] = fuzz.trimf(edot.universe, [k/4, k/2, k*3/4])
edot["PB"] = fuzz.trapmf(edot.universe, [k/2, k*3/4, k, k])

k=umax
u["NB"] = fuzz.trapmf(u.universe, [-k,-k, -k*3/4, -k/2])
u["NM"] = fuzz.trimf(u.universe, [-k*3/4, -k/2, -k/4])
u["NS"] = fuzz.trimf(u.universe, [-k/2, -k/4, 0])
u["ZO"] = fuzz.trimf(u.universe, [-k/4, 0, k/4])
u["PS"] = fuzz.trimf(u.universe, [0, k/4, k/2])
u["PM"] = fuzz.trimf(u.universe, [k/4, k/2, k*3/4])
u["PB"] = fuzz.trapmf(u.universe, [k/2, k*3/4, k, k])

e.view()
edot.view()
u.view()

rule1 = ctrl.Rule(e['ZO'] & edot['NB'], u['NB'])
rule2 = ctrl.Rule(e['ZO'] & edot['NM'], u['NM'])
rule3 = ctrl.Rule(e['ZO'] & edot['NS'], u['NS'])
rule4 = ctrl.Rule(e['ZO'] & edot['ZO'], u['ZO'])
rule5 = ctrl.Rule(e['ZO'] & edot['PS'], u['PS'])
rule6 = ctrl.Rule(e['ZO'] & edot['PM'], u['PM'])
rule7 = ctrl.Rule(e['ZO'] & edot['PB'], u['PB'])

rule8 = ctrl.Rule(edot['ZO'] & e['NB'], u['NB'])
rule9 = ctrl.Rule(edot['ZO'] & e['NM'], u['NM'])
rule10 = ctrl.Rule(edot['ZO'] & e['NS'], u['NS'])
rule11 = ctrl.Rule(edot['ZO'] & e['ZO'], u['ZO'])
rule12 = ctrl.Rule(edot['ZO'] & e['PS'], u['PS'])
rule13 = ctrl.Rule(edot['ZO'] & e['PM'], u['PM'])
rule14 = ctrl.Rule(edot['ZO'] & e['PB'], u['PB'])

rule15 = ctrl.Rule(e['NB'] & edot['PS'], u['NM'])
rule16 = ctrl.Rule(e['NS'] & edot['PS'], u['ZO'])
rule17 = ctrl.Rule(e['NS'] & edot['PB'], u['PM'])
rule18 = ctrl.Rule(e['PS'] & edot['PS'], u['NM'])
rule19 = ctrl.Rule(e['PS'] & edot['NS'], u['ZO'])
rule20 = ctrl.Rule(e['PB'] & edot['NS'], u['PM'])

rule21 = ctrl.Rule(e['NB'] & edot['NB'], u['ZO'])
rule22 = ctrl.Rule(e['NB'] & edot['NM'], u['ZO'])
rule23 = ctrl.Rule(e['NB'] & edot['NS'], u['ZO'])
rule24 = ctrl.Rule(e['NM'] & edot['NB'], u['ZO'])
rule25 = ctrl.Rule(e['NM'] & edot['NS'], u['ZO'])
rule26 = ctrl.Rule(e['NS'] & edot['NB'], u['ZO'])
rule27 = ctrl.Rule(e['NS'] & edot['NM'], u['ZO'])
rule28 = ctrl.Rule(e['NS'] & edot['NS'], u['ZO'])
rule29 = ctrl.Rule(e['PS'] & edot['NM'], u['ZO'])
rule30 = ctrl.Rule(e['PM'] & edot['NB'], u['ZO'])
rule31 = ctrl.Rule(e['PM'] & edot['NB'], u['ZO'])
rule32 = ctrl.Rule(e['PM'] & edot['NS'], u['ZO'])
rule33 = ctrl.Rule(e['PB'] & edot['NB'], u['ZO'])
rule34 = ctrl.Rule(e['PB'] & edot['NM'], u['ZO'])
rule35 = ctrl.Rule(e['NB'] & edot['PM'], u['ZO'])
rule36 = ctrl.Rule(e['NB'] & edot['PB'], u['ZO'])
rule37 = ctrl.Rule(e['NM'] & edot['PS'], u['ZO'])
rule38 = ctrl.Rule(e['NM'] & edot['PM'], u['ZO'])
rule39 = ctrl.Rule(e['NM'] & edot['PB'], u['ZO'])
rule40 = ctrl.Rule(e['NS'] & edot['PM'], u['ZO'])
rule41 = ctrl.Rule(e['PS'] & edot['PS'], u['ZO'])
rule42 = ctrl.Rule(e['PS'] & edot['PM'], u['ZO'])
rule43 = ctrl.Rule(e['PS'] & edot['PB'], u['ZO'])
rule44 = ctrl.Rule(e['PM'] & edot['PS'], u['ZO'])
rule45 = ctrl.Rule(e['PM'] & edot['PM'], u['ZO'])
rule46 = ctrl.Rule(e['PM'] & edot['PB'], u['ZO'])
rule47 = ctrl.Rule(e['PM'] & edot['PS'], u['ZO'])
rule48 = ctrl.Rule(e['PM'] & edot['PM'], u['ZO'])
rule49 = ctrl.Rule(e['PM'] & edot['PB'], u['ZO'])

pd_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7,
                              rule8, rule9, rule10, rule11, rule12, rule13, rule14,
                              rule15, rule16, rule17, rule18, rule19, rule20,
                              rule21, rule22, rule23, rule24, rule25, rule26,
                              rule27, rule28, rule29, rule30, rule31, rule32,
                              rule32, rule33, rule34, rule35, rule36, rule37,
                              rule38, rule39, rule40, rule41, rule42, rule43,
                              rule44, rule45, rule46, rule47, rule48, rule49])

pd = ctrl.ControlSystemSimulation(pd_ctrl)

ys = [0, 0]
us = [0]
dt = 0.1
tmax = 5
t = np.arange(0,tmax,dt)
r = np.ones_like(t)
for i in range(len(t)):
    ri = r[i]
    yi = ys[-1]
    ei = ri-yi
    dei = yi-ys[-2]
    pd.input['e'] = ei
    pd.input['edot'] = dei 
    pd.compute()
    dui = pd.output['u']
    ui = us[-1] + dui
    print(ei,dei,ui,yi)
    yout, _, _ = lsim(G, [ui,ui], [0,dt], yi)
    y_next = yout[1]
    ys.append(y_next)
    us.append(ui)
    # pdb.set_trace()

# pdb.set_trace()
plt.figure()
plt.plot(t,ys[2:])
plt.figure()
plt.plot(t,us[1:])
plt.show()