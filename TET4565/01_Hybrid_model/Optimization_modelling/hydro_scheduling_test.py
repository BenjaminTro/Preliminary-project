import pyomo.environ as pyo
import numpy as np
from pyomo.environ import ConcreteModel,Set,RangeSet,Param,Suffix,Reals,NonNegativeReals,NonPositiveReals,Binary,Objective,minimize,maximize,value
from pyomo.core import Constraint,Var,Block,ConstraintList
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition
import matplotlib.pyplot as plt

model = pyo.ConcreteModel()

#Initial costs for plants/market [NOK]
ai={'Hydro1':200, 'Hydro2':500, 'Solar':1000, 'Market':0}
#Variable costs for plants/ market price [NOK/MWh]
bi={'Hydro1':60, 'Hydro2':100, 'Solar':150, 'Market':130}
#Production levels / Purchase from market [MW]
Pmin = {'Hydro1':0, 'Hydro2':0, 'Solar':0, 'Market':0}
Pmax = {'Hydro1':41, 'Hydro2':60, 'Solar':30, 'Market':np.inf}


#Defining periods of 1 hour throughout a day
model.periods = pyo.Set(initialize=[1,2,3,4,5,6,7, 8 , 9 , 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])

#Solar production based on forecast (should come from irradiance data)

Solar_p= {1:0, 2:0, 3:0, 4:0, 5:2, 6:5, 7:8, 8:10, 9:12, 10:15, 11:18, 12:22, 13:25, 14:28, 15:30, 16:30, 17:30, 18:25, 19:20, 
        20:15, 21:10, 22:5, 23:0, 24:0}

#Load demand [MW]
L= {1:30, 2:20, 3:20, 4:30, 5:50, 6:80, 7:50, 8:90, 9:110, 10:150, 11:120, 12:80, 13:70, 14:80, 15:90, 16:160, 17:170, 18:150, 19:120, 20:100, 21:70, 22:60, 23:50, 24:40} 

#Defining the set of plants
model.plants = pyo.Set(initialize=['Hydro1','Hydro2', 'Solar', 'Market']) 

#Variables for each plant and each period
def p_bounds(model,i,j):
    return (Pmin[i],Pmax[i])
model.p = pyo.Var(model.plants,model.periods, bounds=p_bounds)

#Constraint for solar following production plan
def Solar_rule(model,j):
    return  model.p['Solar',j] == Solar_p[j]
model.solar_cons = pyo.Constraint(model.periods, rule=Solar_rule)

#Constraint for production demand
def load_rule(model,j):
    return model.p['Hydro1',j] + model.p['Hydro2',j] + model.p['Solar',j] + model.p['Market',j]== L[j]
model.load_cons = pyo.Constraint(model.periods, rule=load_rule)

#Objective function 
def ObjRule(model):
    return sum(ai[i]+bi[i]*model.p[i,j] for i in model.plants for j in model.periods)
model.obj= pyo.Objective(rule=ObjRule, sense=pyo.minimize)

#defining dual 
model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

#solver 
opt = SolverFactory('gurobi', solver_io="python") 
results = opt.solve(model,tee=True) 

print('\n')

#printing solver
for v in model.component_data_objects(pyo.Var):
  print('%s:   %s'%(str(v), v.value))
  
  
model.display()
model.dual.display()

#appending production values in dictionary
prod={}
for i in model.plants:
    prod[i]=[value(model.p[i, j]) for j in model.periods]

#Plotting stacked plot for production plan     
plt.figure(figsize=(10, 6))
bottom = [0] * len(model.periods)

for plant in model.plants:
    plt.bar(model.periods, prod[plant], label=plant, bottom=bottom)
    bottom = [bottom[i] + prod[plant][i] for i in range(len(model.periods))]

plt.xlabel("Period [h]")
plt.ylabel("Production [MW]")
plt.title("Optimal production plan")
plt.legend()
plt.show()