import collections
from collections import defaultdict


consumption=7000
threshhold=5000
priority=defaultdict(list)
priority={2:[['w1',1000],['w2',200],['w3',300]],1:[['w5',100],['w6',200],['w7',300]],3:[['w8',100],['w9',200],['w10',300]]}
#for x,y in priority.items():
##while bool(priority)==True:
##    for y in priority[[min(priority.keys())]]:
##        while bool(y)==True:
##            #print(min(y))
##            del y[y.index(min(y))]
##            print(y)
##del priority[min(priority.keys())]  
##print(priority[max(priority.keys())])
##while bool(priority)==True:
##    for y in priority[max(priority.keys())]:
##        print(y)
####        consumption=y[1]+consumption
####        if consumption >= threshhold:
####            break;
####    if consumption >= threshhold:
####        break;
####    
##    del priority[max(priority.keys())]
##print(consumption)


while bool(priority)==True:
    print(priority[min(priority.keys())])
    for y in priority[min(priority.keys())]:
        consumption=consumption-y[1]
        del y[y.index(min(y))]
        if consumption <= threshhold:
            break;
    if consumption <= threshhold:
       break;
    del priority[min(priority.keys())]



print(consumption) 
