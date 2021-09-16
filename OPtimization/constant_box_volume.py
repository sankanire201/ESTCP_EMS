import numpy as np
from scipy.optimize import minimize

def calcVolume(x):
    length = x[0]
    width =x[1]
    height = x[2]
    volume = length*width*height
    return volume
def calcSurface(x):
    length = x[0]
    width =x[1]
    height = x[2]
    surfaceArea=2*length*width+2*length*height*2*height*width
    return surfaceArea
def objective(x):
    return -calcVolume(x)
def constraint(x):
    return 10-calcSurface(x)

cons =({'type':'ineq','fun':constraint})
lenghtGuess=1
widthGuess=1
HeightGuess=1
x0=np.array([lenghtGuess,widthGuess,HeightGuess])

sol = minimize(objective,x0,method='SLSQP',constraints=cons,options={'disp':True})
xopt=sol.x
volumeOpt=-sol.fun
surfaceAreaOpt=calcSurface(xopt)


