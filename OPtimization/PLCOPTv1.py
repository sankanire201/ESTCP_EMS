
import numpy as np
from scipy.optimize import minimize

consuption = [10,20,190,40]

def objective(x):
    return (consuption[0]*x[0]+consuption[1]*x[1]+consuption[2]*x[2]+consuption[3]*x[3])-320
    
def constraint1(x):
    return (x[0]+x[1]+x[2]+x[3])-1


cons =({'type':'ineq','fun':constraint1})
b=(0.1,2.5)
bnds=(b,b,b,b)

x0=[.5,.2,.2,.1]
sol = minimize(objective,x0,method='SLSQP',bounds=bnds,constraints=cons,options={'disp':True})
xopt=sol.x
print(xopt)
