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
e = ctrl.Antecedent(np.arange(-1, 1, 0.01), 'e')
edot = ctrl.Antecedent(np.arange(-0.2, 0.2, 0.001), 'edot')
u = ctrl.Consequent(np.arange(-1, 1, 0.01), 'u')

e["NB"] = fuzz.trapmf(e.universe, [-1,-1, -.75, -.50])
e["NS"] = fuzz.trimf(e.universe, [-.5, -.25, 0])
e["ZO"] = fuzz.trimf(e.universe, [-.25, 0, .25])
e["PS"] = fuzz.trimf(e.universe, [0, .25, .5])
e["PB"] = fuzz.trapmf(e.universe, [.5, .75, 1, 1])

edot["NB"] = fuzz.trapmf(edot.universe, [-.2,-.2, -.15, -.1])
edot["NS"] = fuzz.trimf(edot.universe, [-.1, -.05, 0])
edot["ZO"] = fuzz.trimf(edot.universe, [-.05, 0, .05])
edot["PS"] = fuzz.trimf(edot.universe, [0, .05, .1])
edot["PB"] = fuzz.trapmf(edot.universe, [.1, .15, .2, .2])

u["NB"] = fuzz.trapmf(u.universe, [-1,-1, -.75, -.5])
u["NS"] = fuzz.trimf(u.universe, [-.5, -.25, 0])
u["ZO"] = fuzz.trimf(u.universe, [-.25, 0, .25])
u["PS"] = fuzz.trimf(u.universe, [0, .25, .5])
u["PB"] = fuzz.trapmf(u.universe, [.5, .75, 1, 1])

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
rule25 = ctrl.Rule(e['NM'] & edot['NB'], u['ZO'])
rule26 = ctrl.Rule(e['NM'] & edot['NS'], u['ZO'])
rule27 = ctrl.Rule(e['NS'] & edot['NB'], u['ZO'])
rule28 = ctrl.Rule(e['NS'] & edot['NM'], u['ZO'])
rule29 = ctrl.Rule(e['NS'] & edot['NS'], u['ZO'])
rule30 = ctrl.Rule(e['PS'] & edot['NM'], u['ZO'])
rule31 = ctrl.Rule(e['PM'] & edot['NB'], u['ZO'])
rule32 = ctrl.Rule(e['PM'] & edot['NB'], u['ZO'])
rule33 = ctrl.Rule(e['PM'] & edot['NS'], u['ZO'])
rule34 = ctrl.Rule(e['PB'] & edot['NB'], u['ZO'])
rule35 = ctrl.Rule(e['PB'] & edot['NM'], u['ZO'])
rule36 = ctrl.Rule(e['NB'] & edot['PM'], u['ZO'])
rule37 = ctrl.Rule(e['NB'] & edot['PB'], u['ZO'])
rule38 = ctrl.Rule(e['NM'] & edot['PS'], u['ZO'])
rule39 = ctrl.Rule(e['NM'] & edot['PM'], u['ZO'])
rule40 = ctrl.Rule(e['NM'] & edot['PB'], u['ZO'])
rule41 = ctrl.Rule(e['NS'] & edot['PM'], u['ZO'])
rule42 = ctrl.Rule(e['PS'] & edot['PS'], u['ZO'])
rule43 = ctrl.Rule(e['PS'] & edot['PM'], u['ZO'])
rule44 = ctrl.Rule(e['PS'] & edot['PB'], u['ZO'])
rule45 = ctrl.Rule(e['PM'] & edot['PS'], u['ZO'])
rule46 = ctrl.Rule(e['PM'] & edot['PM'], u['ZO'])
rule47 = ctrl.Rule(e['PM'] & edot['PB'], u['ZO'])
rule48 = ctrl.Rule(e['PM'] & edot['PS'], u['ZO'])
rule49 = ctrl.Rule(e['PM'] & edot['PM'], u['ZO'])
rule50 = ctrl.Rule(e['PM'] & edot['PB'], u['ZO'])

pd_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7,
                              rule8, rule9, rule10, rule11, rule12, rule13, rule14,
                              rule15, rule16, rule17, rule18, rule19, rule20,
                              rule21, rule22, rule23, rule24, rule25, rule26,
                              rule27, rule28, rule29, rule30, rule31, rule32,
                              rule32, rule33, rule34, rule35, rule36, rule37,
                              rule38, rule39, rule40, rule41, rule42, rule43,
                              rule44, rule45, rule46, rule47, rule48, rule49,
                              rule50])

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
    pd.input['e'] = ei
    pd.input['edot'] = edot_i 
    pd.compute()
    ui = pd.output['u']
    y_t = lsim(G, [ui,0], [0,dt])
    y_next = y_t[0][0]
    # pdb.set_trace()
    ys.append(y_next)
    es.append(ei)

plt.figure()
plt.plot(t,ys[1:])
plt.show()
pdb.set_trace()