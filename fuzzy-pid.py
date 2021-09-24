from control.matlab import *
import matplotlib.pyplot as plt
import pdb
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy.defuzzify import defuzz
import numpy as np
import pandas as pd
import math

s = tf('s')
# G = 1/(0.8+0.3*s+s**2)
G = 3/(30*s+1)
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

#PD controller
emax = 15*1.25
edotmax = 3*1.25
umax =  50*1.25
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

df = pd.read_csv('fuzzy_table.csv',index_col="e")
columns = df.columns
indices = df.index
rules = []
for c in columns:
    for i in indices:
        print("if e=={} AND e=={} then u={}".format(i,c,df[c][i]))
        rules.append(ctrl.Rule(e[i] & edot[c], u[df[c][i]]))

# rule1 = ctrl.Rule(e['ZO'] & edot['NB'], u['NB'])
# rule2 = ctrl.Rule(e['ZO'] & edot['NM'], u['NM'])
# rule3 = ctrl.Rule(e['ZO'] & edot['NS'], u['NS'])
# rule4 = ctrl.Rule(e['ZO'] & edot['ZO'], u['ZO'])
# rule5 = ctrl.Rule(e['ZO'] & edot['PS'], u['PS'])
# rule6 = ctrl.Rule(e['ZO'] & edot['PM'], u['PM'])
# rule7 = ctrl.Rule(e['ZO'] & edot['PB'], u['PB'])

# rule8 = ctrl.Rule(edot['ZO'] & e['NB'], u['NB'])
# rule9 = ctrl.Rule(edot['ZO'] & e['NM'], u['NM'])
# rule10 = ctrl.Rule(edot['ZO'] & e['NS'], u['NS'])
# rule11 = ctrl.Rule(edot['ZO'] & e['ZO'], u['ZO'])
# rule12 = ctrl.Rule(edot['ZO'] & e['PS'], u['PS'])
# rule13 = ctrl.Rule(edot['ZO'] & e['PM'], u['PM'])
# rule14 = ctrl.Rule(edot['ZO'] & e['PB'], u['PB'])

# rule15 = ctrl.Rule(e['NB'] & edot['PS'], u['NM'])
# rule16 = ctrl.Rule(e['NS'] & edot['PS'], u['ZO'])
# rule17 = ctrl.Rule(e['NS'] & edot['PB'], u['PM'])
# rule18 = ctrl.Rule(e['PS'] & edot['PS'], u['NM'])
# rule19 = ctrl.Rule(e['PS'] & edot['NS'], u['ZO'])
# rule20 = ctrl.Rule(e['PB'] & edot['NS'], u['PM'])

# rule21 = ctrl.Rule(e['NB'] & edot['NB'], u['ZO'])
# rule22 = ctrl.Rule(e['NB'] & edot['NM'], u['ZO'])
# rule23 = ctrl.Rule(e['NB'] & edot['NS'], u['ZO'])
# rule24 = ctrl.Rule(e['NM'] & edot['NB'], u['ZO'])
# rule25 = ctrl.Rule(e['NM'] & edot['NB'], u['ZO'])
# rule26 = ctrl.Rule(e['NM'] & edot['NS'], u['ZO'])
# rule27 = ctrl.Rule(e['NS'] & edot['NB'], u['ZO'])
# rule28 = ctrl.Rule(e['NS'] & edot['NM'], u['ZO'])
# rule29 = ctrl.Rule(e['NS'] & edot['NS'], u['ZO'])
# rule30 = ctrl.Rule(e['PS'] & edot['NM'], u['ZO'])
# rule31 = ctrl.Rule(e['PM'] & edot['NB'], u['ZO'])
# rule32 = ctrl.Rule(e['PM'] & edot['NB'], u['ZO'])
# rule33 = ctrl.Rule(e['PM'] & edot['NS'], u['ZO'])
# rule34 = ctrl.Rule(e['PB'] & edot['NB'], u['ZO'])
# rule35 = ctrl.Rule(e['PB'] & edot['NM'], u['ZO'])
# rule36 = ctrl.Rule(e['NB'] & edot['PM'], u['ZO'])
# rule37 = ctrl.Rule(e['NB'] & edot['PB'], u['ZO'])
# rule38 = ctrl.Rule(e['NM'] & edot['PS'], u['ZO'])
# rule39 = ctrl.Rule(e['NM'] & edot['PM'], u['ZO'])
# rule40 = ctrl.Rule(e['NM'] & edot['PB'], u['ZO'])
# rule41 = ctrl.Rule(e['NS'] & edot['PM'], u['ZO'])
# rule42 = ctrl.Rule(e['PS'] & edot['PS'], u['ZO'])
# rule43 = ctrl.Rule(e['PS'] & edot['PM'], u['ZO'])
# rule44 = ctrl.Rule(e['PS'] & edot['PB'], u['ZO'])
# rule45 = ctrl.Rule(e['PM'] & edot['PS'], u['ZO'])
# rule46 = ctrl.Rule(e['PM'] & edot['PM'], u['ZO'])
# rule47 = ctrl.Rule(e['PM'] & edot['PB'], u['ZO'])
# rule48 = ctrl.Rule(e['PM'] & edot['PS'], u['ZO'])
# rule49 = ctrl.Rule(e['PM'] & edot['PM'], u['ZO'])
# rule50 = ctrl.Rule(e['PM'] & edot['PB'], u['ZO'])

pd_ctrl = ctrl.ControlSystem()
for r in rules:
    pd_ctrl.addrule(r)

pd = ctrl.ControlSystemSimulation(pd_ctrl)

ys = [0]
es = [0] 
dt = 0.1
t = np.arange(0,10,0.1)
r = np.ones_like(t)

for i in range(len(t)):
    ri = r[i]
    yi = ys[-1]
    ei = yi-ri
    elast = es[-1]
    edot_i = ei - elast

    e_level_NB = fuzz.interp_membership(x_e, e["NB"] , ei) 
    e_level_NM = fuzz.interp_membership(x_e, e["NM"] , ei) 
    e_level_NS = fuzz.interp_membership(x_e, e["NS"] , ei) 
    e_level_ZO = fuzz.interp_membership(x_e, e["ZO"] , ei) 
    e_level_PS = fuzz.interp_membership(x_e, e["PS"] , ei) 
    e_level_PM = fuzz.interp_membership(x_e, e["PM"] , ei) 
    e_level_PB = fuzz.interp_membership(x_e, e["PB"] , ei) 

    edot_level_NB = fuzz.interp_membership(x_edot, edot["NB"] , edot_i) 
    edot_level_NM = fuzz.interp_membership(x_edot, edot["NM"] , edot_i) 
    edot_level_NS = fuzz.interp_membership(x_edot, edot["NS"] , edot_i) 
    edot_level_ZO = fuzz.interp_membership(x_edot, edot["ZO"] , edot_i) 
    edot_level_PS = fuzz.interp_membership(x_edot, edot["PS"] , edot_i) 
    edot_level_PM = fuzz.interp_membership(x_edot, edot["PM"] , edot_i) 
    edot_level_PB = fuzz.interp_membership(x_edot, edot["PB"] , edot_i) 

    active_rule1 = np.fmin(qual_level_lo, serv_level_lo)


    pd.input['e'] = ei
    pd.input['edot'] = edot_i 
    pd.compute()
    ui = pd.output['u']
    y_t = lsim(G, [ui,0], [0,dt])
    y_next = y_t[0][0]
    pdb.set_trace()
    ys.append(y_next)
    es.append(ei)

plt.figure()
plt.plot(t,ys[1:])
plt.show()
# pdb.set_trace()