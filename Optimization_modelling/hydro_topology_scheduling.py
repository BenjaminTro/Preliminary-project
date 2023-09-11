import pyomo.environ as pyo
import numpy as np
from pyomo.environ import ConcreteModel,Set,RangeSet,Param,Suffix,Reals,NonNegativeReals,NonPositiveReals,Binary,Objective,minimize,maximize,value
from pyomo.core import Constraint,Var,Block,ConstraintList
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition
import matplotlib.pyplot as plt



""" BASE CASE MODEL """

# Creation of a Concrete Model
model = pyo.ConcreteModel()


#------------------- PARAMETERS -------------------------------------

# Reservoir level limits [Mm^3]
Vstart = {'Upper':420, 'Lower':18}
Vmin = {'Upper':0, 'Lower':4}
Vmax = {'Upper':500, 'Lower':20}

# Discharge [m^3/s]
Qmin = {'Upper':2, 'Lower':4}
Qamax = {'Upper':12, 'Lower':12}
Qbmax = {'Upper':4, 'Lower':5}
Qcmax = {'Upper':100, 'Lower':0}

# Production [MW]
Pmin = {'Upper':12, 'Lower':6}
Pmax = {'Upper':200, 'Lower':200}

# Load [MW]
L = {1:60,2:120,3:90,4:80}

# Inflow [m^3/s]
Q = {'Upper':0.5, 'Lower':30}

# Constants and conversion factors
beta_a = {'Upper':6, 'Lower':1.5} # MW/m^3/s (conversion factor between production and discharge for generator 1 (Upper) and 2 (Lower), segment A)
beta_b = {'Upper':5, 'Lower':1.3} # MW/m^3/s (conversion factor between production and discharge for generator 1 and 2, segment B)


fm3 = 3600/1000000 # Conversion factor between m^3/s and Mm^3/hour. 1h = 3600s and M = 10^6.
l = 6              # Length of each time step (6 hours)
wv = {'Upper':650000, 'Lower':120000 }   # Water value for reservoir 2 given from the "Seasonal Model" to maintain long-term strategy (NOK/Mm^3)


#----------------------- SETS -------------------------------------

# Set of periods
model.periods = pyo.Set(initialize=[1,2,3,4]) 
model.periods_ = pyo.Set(initialize=[2,3,4])   

# Set of reservoirs            
model.reservoirs = pyo.Set(initialize=['Upper','Lower'])     


# -------------- VARIABLES AND THEIR BOUNDS ------------------------


# the variables are defined for each reservoir and each period

def qA_bounds(model,i,j):
    return (0,Qamax[i])
model.qA = pyo.Var(model.reservoirs,model.periods, bounds=qA_bounds) 

def qB_bounds(model,i,j):
    return (0,Qbmax[i])
model.qB = pyo.Var(model.reservoirs,model.periods, bounds=qB_bounds)

def qC_bounds(model,i,j):
    return (0,Qcmax[i])
model.qC = pyo.Var(model.reservoirs,model.periods, bounds=qC_bounds)

def q_bounds(model,i,j):
    return (Qmin[i],np.inf)
model.q = pyo.Var(model.reservoirs,model.periods, bounds=q_bounds)

def v_bounds(model,i,j):
    return (Vmin[i],Vmax[i])
model.v = pyo.Var(model.reservoirs,model.periods, bounds=v_bounds)

def p_bounds(model,i,j):
    return (Pmin[i],Pmax[i])
model.p = pyo.Var(model.reservoirs,model.periods, bounds=p_bounds)

# ----------------- CONSTRAINTS ------------------------

# Discharge
def disch_rule(model,i,j):
    return model.qA[i,j] + model.qB[i,j] + model.qC[i,j] + Qmin[i] == model.q[i,j]
model.disch_cons = pyo.Constraint(model.reservoirs,model.periods, rule=disch_rule)

# Production
def prod_rule(model,i,j):
    return model.qA[i,j]*beta_a[i] + model.qB[i,j]*beta_b[i] + Pmin[i] == model.p[i,j]
model.prod_cons = pyo.Constraint(model.reservoirs,model.periods, rule=prod_rule)

# Load Balance
def load_rule(model,j):
    return model.p['Upper',j] + model.p['Lower',j] == L[j]
model.load_cons = pyo.Constraint(model.periods, rule=load_rule)

# Reservoir Balance
def res_start_rule(model,i):
    if i=='Upper':
        return model.v[i,1] == Vstart[i] + Q[i]*fm3*l - model.q[i,1]*fm3*l
    elif i == 'Lower':
        return model.v[i,1] == Vstart[i] + Q[i]*fm3*l - model.q[i,1]*fm3*l + model.q['Upper',1]*fm3*l
model.res_start_cons = pyo.Constraint(model.reservoirs, rule=res_start_rule)
    
def res_rule(model,i,j):
    if i=='Upper':
        return model.v[i,j] == model.v[i,j-1] + Q[i]*fm3*l - model.q[i,j]*fm3*l
    elif i=='Lower':
        return model.v[i,j] == model.v[i,j-1] + Q[i]*fm3*l - model.q[i,j]*fm3*l + model.q['Upper',j]*fm3*l
model.res_cons = pyo.Constraint(model.reservoirs,model.periods_, rule=res_rule)


# -------------------- OBJECTIVE FUNCTION --------------------------------
    
def ObjRule(model):
    return sum(model.q[i,j]*wv[i]*fm3*l for i in model.reservoirs for j in model.periods)
model.obj= pyo.Objective(rule=ObjRule, sense=pyo.minimize)


# -------------- SOLVING THE SHORT TERM LP PROBLEM -----------------------

model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
opt = SolverFactory('gurobi', solver_io="python") 
results = opt.solve(model,tee=True) 

print('\n')

for v in model.component_data_objects(pyo.Var):
  print('%s:   %s'%(str(v), v.value))
  
model.display()
model.dual.display()

v_upper=[420, 419.9046, 419.58924  ,419.38584000000003 , 419.21844000000004]
v_lower=[18, 18.3006, 18.82116 , 19.22976, 19.602359999999997 ]
p_upper=[29.5, 89.5, 59.5, 49.5]
p_lower=[30.5, 30.5,30.5,30.5]
periods=[0, 1, 2, 3, 4]
PERIODS=[1, 2, 3, 4]

plt.plot(periods, v_upper)
plt.ylabel("Reservoir level [m^3]")
plt.xlabel("Periods (6h)")
plt.show()

plt.plot(periods, v_lower, 'r')
plt.ylabel("Reservoir level [m^3]")
plt.xlabel("Periods (6h)")
plt.show()

plt.plot(PERIODS, p_upper, label=("Upper plant"))
plt.plot(PERIODS, p_lower, label=("Lower plant"))
plt.legend(loc='upper left')
plt.ylim(0,90)
plt.ylabel("Power production [MW]")
plt.xlabel("Periods (6h)")
plt.show()