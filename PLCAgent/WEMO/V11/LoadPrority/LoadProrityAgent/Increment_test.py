import collections
from collections import defaultdict


consumption=0
threshhold=100
priority=defaultdict(list)
priority={2:[['w1',100],['w2',200],['w3',300]],1:[['w5',100],['w6',200],['w7',300]],3:[['w8',100],['w9',200],['w10',300]]}
#for x,y in priority.items():
for x,y in priority.items():
    print(y)

while bool(priority)==True:
    for y in priority[max(priority.keys())]:
        print(y)
        consumption=y[1]+consumption
        if consumption >= threshhold:
            break;
    if consumption >= threshhold:
        break;
    
    del priority[max(priority.keys())]
print(consumption)
