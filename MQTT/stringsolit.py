
topic = "devices/building540/WeMo_cc_2/Wp-60-L/all"
x=topic.split('/')
result = topic.find('building540')
#41390 soc
#41140 single phase  devices/acquisition/loads/building3/Wp-57-L
##new_topic=""
##for y in x:
##    
##    if y =='devices':
##        new_topic=str(y)+'/'+'acquisition/'
##    elif y=='all':
##        new_topic=new_topic+str(y)
##    else:
##        new_topic=new_topic+str(y)+'/'

new_topic='devices/acquisition'+x[1]
print(x[-2])
