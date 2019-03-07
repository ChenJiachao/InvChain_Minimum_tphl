import subprocess
import numpy as np
import shutil
import re
p=subprocess.Popen(["hspice","InvChain.sp"], stdout=subprocess.PIPE)
output,err = p.communicate()
print(" *** Running hspice InvChain.sp command ***\n", output)
Data = np.recfromcsv("InvChain.mt0.csv",comments="$",skip_header=3)
print(Data["tphl_inv"])
tphl_prev = Data["tphl_inv"]
f = open('InvChain.sp', 'r')
f1 = open('InvChain1.sp','w')
for line in f:
    if line == '.param fan = 1\n':
        line = '.param fan = 2\n'
    f1.write(line)
f.close()
f1.close()

p=subprocess.Popen(["hspice","InvChain.sp"], stdout=subprocess.PIPE)
output,err = p.communicate()
print(" *** Running hspice InvChain.sp command ***\n", output)

Data = np.recfromcsv("InvChain.mt0.csv",comments="$",skip_header=3)
print(Data["tphl_inv"])
tphl_next = Data["tphl_inv"]

value=[]

for a in range(1,10,2):
    index = a
    for b in range(2,6,1):
        beta = b
        if index == a :
            f = open('InvChain.sp', 'r')
            f1 = open('InvChain1.sp','w')

            for line in f:
                match = re.search(r'^X',line)
                if match:
                    f1.write('')
                else:
                    f1.write(line)
                match = re.search(r'Cload', line)
                if match:
                    line = 'Xinv1 a 2 inv M='+str(beta)+'\n'
                    f1.write(line)
                    for j in np.arange(1,index-1,1):
                        line = 'Xinv'+str(j+1)+' '+str(j+1)+' '+str(j+2)+' inv M='+str(beta**(j+1))+'\n'
                        f1.write(line)
                    line = 'Xinv'+str(index)+' '+str(index)+' z inv M='+str(beta**index)+'\n'
                    f1.write(line)
            f.close()
            f1.close()

            shutil.copyfile('InvChain1.sp', 'InvChain.sp')
            p = subprocess.Popen(["hspice", "InvChain.sp"], stdout=subprocess.PIPE)
            output, err = p.communicate()
            print(" *** Running hspice InvChain.sp command ***\n", output)

            Data = np.recfromcsv("InvChain.mt0.csv", comments="$", skip_header=3)
            tphl_prev = tphl_next
            tphl_next = Data["tphl_inv"]
            value.append([tphl_next,a,b])


# This is where I begin to find the minimum tphl in the value

value=np.asarray(value)
colum=value[:,0]
min_num=min(colum)
index_num=[i for i, j in enumerate(colum) if j == min_num]

first=int(value[index_num,1])
sec=int(value[index_num,2])

index = first
beta = sec
#rewrite the InvChain file
if index == index :
    f = open('InvChain.sp', 'r')
    f1 = open('InvChain1.sp','w')

    for line in f:
        match = re.search(r'^X',line)
        if match:
            f1.write('')
        else:
            f1.write(line)
        match = re.search(r'Cload', line)
        if match:
            line = 'Xinv1 a 2 inv M='+str(beta)+'\n'
            f1.write(line)
            for j in np.arange(1,index-1,1):
                line = 'Xinv'+str(j+1)+' '+str(j+1)+' '+str(j+2)+' inv M='+str(beta**(j+1))+'\n'
                f1.write(line)
            line = 'Xinv'+str(index)+' '+str(index)+' z inv M='+str(beta**index)+'\n'
            f1.write(line)
    f.close()
    f1.close()

    shutil.copyfile('InvChain1.sp', 'InvChain.sp')

    p=subprocess.Popen(["hspice","InvChain.sp"], stdout=subprocess.PIPE)
    output,err = p.communicate()
    print(" *** Running hspice InvChain.sp command ***\n", output)

    Data = np.recfromcsv("InvChain.mt0.csv",comments="$",skip_header=3)
    print(Data["tphl_inv"])
    tphl_prev = tphl_next
    tphl_next = Data["tphl_inv"]

print(colum)
