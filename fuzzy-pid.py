from control.matlab import *
import matplotlib.pyplot as plt
import pdb
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy.defuzzify import defuzz
import numpy as np
import math

#PI controller
emax = 15
edotmax = 3
umax =  50
width = lambda x: 10**int(math.log10(x)-3) # 100 division

x_e = np.arange(-emax, emax, width(emax))
x_edot = np.arange(-edotmax, edotmax, width(edotmax))
x_u = np.arange(-umax, umax, width(umax))
e = ctrl.Antecedent(x_e, 'e')
edot = ctrl.Antecedent(x_edot, 'edot')
u = ctrl.Consequent(x_u, 'u')

k = emax
e["NB"] = fuzz.trapmf(e.universe, [-k,-k, -k*3/4, -k/2])
e["NM"] = fuzz.trimf(e.universe, [-k*3/4, -k/2, -k/4])
e["NS"] = fuzz.trimf(e.universe, [-k/2, -k/4, 0])
e["ZO"] = fuzz.trimf(e.universe, [-k/4, 0, k/4])
e["PS"] = fuzz.trimf(e.universe, [0, k/4, k/2])
e["PM"] = fuzz.trimf(e.universe, [k/4, k/2, k*3/4])
e["PB"] = fuzz.trapmf(e.universe, [k/2, k*3/4, k, k])

k = edotmax
edot["NB"] = fuzz.trapmf(edot.universe, [-k,-k, -k*3/4, -k/2])
edot["NM"] = fuzz.trimf(edot.universe, [-k*3/4, -k/2, -k/4])
edot["NS"] = fuzz.trimf(edot.universe, [-k/2, -k/4, 0])
edot["ZO"] = fuzz.trimf(edot.universe, [-k/4, 0, k/4])
edot["PS"] = fuzz.trimf(edot.universe, [0, k/4, k/2])
edot["PM"] = fuzz.trimf(edot.universe, [k/4, k/2, k*3/4])
edot["PB"] = fuzz.trapmf(edot.universe, [k/2, k*3/4, k, k])

k = umax
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
rule11 = ctrl.Rule(edot['ZO'] & e['PS'], u['PS'])
rule12 = ctrl.Rule(edot['ZO'] & e['PM'], u['PM'])
rule13 = ctrl.Rule(edot['ZO'] & e['PB'], u['PB'])

pd_ctrl = ctrl.ControlSystem()

pd_ctrl.addrule(rule1)
pd_ctrl.addrule(rule2)
pd_ctrl.addrule(rule3)
pd_ctrl.addrule(rule4)
pd_ctrl.addrule(rule5)
pd_ctrl.addrule(rule6)
pd_ctrl.addrule(rule7)
pd_ctrl.addrule(rule8)
pd_ctrl.addrule(rule9)
pd_ctrl.addrule(rule10)
pd_ctrl.addrule(rule11)
pd_ctrl.addrule(rule12)
pd_ctrl.addrule(rule13)

pd = ctrl.ControlSystemSimulation(pd_ctrl)

s = tf('s')
G = 3/(30*s+1)
# y, t = step(G)
us = [0]
ys = [0]
es = [0] 
dt = 0.1
t = np.arange(0,30,0.1)
r = np.ones_like(t)

for i in range(len(t)):
    ri = r[i]
    yi = ys[-1]
    ui = us[-1]
    ei = ri-yi
    elast = es[-1]
    edot_i = elast - ei
    pd.input['e'] = ei
    pd.input['edot'] = edot_i 
    pd.compute()
    du = pd.output['u']
    ui = ui + du
    y_t = lsim(G, [ui,0], [0,dt])
    y_next = y_t[0][1]
    print(du, ui,y_next)
    ys.append(y_next)
    es.append(ei)
    us.append(ui)

plt.figure()
plt.plot(t,ys[1:])
plt.show()