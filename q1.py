from collections import defaultdict
import sys, fileinput
from tree import Tree
import time
#import matplotlib.pyplot as plt
import numpy
from sklearn import linear_model
import math
rules = {}
probability={}
rule_prob={}
invert=defaultdict(list)
total=0
max=0
d=0
freq=''
start=0
pl_X=[]
pl_Y=[]

for line in open("train.trees.pre.unk"):

#with open("train.trees.pre.unk") as trees:
    #one=trees.readline()
    t=Tree.from_str(line)
    #print t
    for node in t.bottomup():
        if node.children==[]:
            continue
        right = ''
        for child in node.children:
            right = right + ' ' + child.label
            right=right.strip()
        if node.label not in rules:
            rules[node.label] = {}
        if right in rules[node.label]:
            rules[node.label][right] += 1
        else:
            rules[node.label][right] = 1
#print rules

for rule in rules:
    for i in rules[rule]:
        total=total+1
for rule in rules:
    for i in rules[rule]:
        #print rule, "--->",i,"#",rules[rule][i]
        if max < int(rules[rule][i]):
            max=rules[rule][i]
#print max

for rule in rules:
    for i in rules[rule]:
        if (rules[rule][i])== max:
            freq=freq+ rule +'---->'+ i+' Occurs '+ str(max) +' times, which is most freuqently occuring rule.'


#print "\n",freq

#print "Total Distinct Rules: ",total


for rule in rules:
    t=0
    for i in rules[rule]:
        t+=rules[rule][i]
    probability[rule]=t
#print probability

for rule in rules:
    for i in rules[rule]:
        #print rules[rule][i],"_____",probability[rule],"_____",math.log(float(rules[rule][i])/float(probability[rule]))
        rule_prob[rule+"-->"+i]=math.log10(float(rules[rule][i])/float(probability[rule]))
#print rule_prob
li=[]
for k in rule_prob:
    #print k
    x=k.split("-->")
    #print x[0], rule_prob[k]
    if x[1] in invert:
        invert[x[1]].append([x[0],rule_prob[k]])
    else:
        invert[x[1]].append([x[0],rule_prob[k]])

#for x in invert:
#    print x,":",invert[x]
#print invert

###PRINT TREE#####
def print_tree(rule, i, j, back,str):
    str+=" "
    if back[i,j][rule][0] == -1:
        str+=('(' + rule + ' ' + back[i,j][rule][1] + ')')
    else:
        str+=('(' + rule)
        str=print_tree(back[i,j][rule][1], i, back[i,j][rule][0], back,str)
        str=print_tree(back[i,j][rule][2], back[i,j][rule][0], j, back,str)
        str+=(')')
    return str
### PARSER ####

for l in fileinput.input():
        li.append(l);


#first=li[0].split()
def parser(first):
    chart = defaultdict(list)
    bp=defaultdict(dict)
    #global d
    #global start
    #global pl_X
    #global pl_Y

    for i in range(1, len(first) + 1): #rows
        for j in range(0, len(first)): #columns
            for k in range(j+1, len(first)+1): # check end of range
                if k-j==i and i==1:
                    if first[k-1] in invert:
                        word = first[j]
                        chart[j, k] = invert[word]
                        for ky in invert[first[j]]:
                            bp[j, k][ky[0]] = [-1, first[j], first[j]]
                    elif first[j] not in invert:
                        word="<unk>"
                        chart[j,k] = invert[word]
                        for ky in invert[word]:
                            bp[j,k][ky[0]] = [-1, first[j], first[j]]
                elif k-j==i and i!=1:
                    for k1 in range(j+1,k):
                        for right in chart[j,k1]:
                            for down in chart[k1,k]:
                                bf=right[0] + " " + down[0]
                                if bf in invert:
                                    for main_val in invert[bf]:
                                        flag=False
                                        for trav in range(len(chart[j,k])):
                                            if chart[j,k][trav][0]==main_val[0]:
                                                flag=True
                                                A=float(main_val[1])+float(right[1])+float(down[1])
                                                B=chart[j,k][trav][1]
                                                if A>B:
                                                    chart[j, k][trav][1]=A
                                                    bp[j,k][main_val[0]]=[k1, right[0],down[0]]
                                        if not flag:
                                            A1=float(main_val[1])+float(right[1])+float(down[1])
                                            chart[j,k].append([main_val[0],A1])
                                            bp[j, k][main_val[0]] = [k1, right[0], down[0]]

    #for z in bp:
     #   print z, ":", bp[z]
    if (0, len(first)) not in bp:
        print ''
        #d=time.time()-start
        #pl_X.append(len(first))
        #pl_Y.append(d)
    else:
        str1 = ''
        print print_tree('TOP', 0, len(first), bp, str1).strip()
        #d = time.time() - start
        #pl_X.append(len(first))
        #pl_Y.append(d)
    #print chart[0,len(first)]
for t in li:
    #start=time.time()
    parser(t.split())
#
# pl_X_log=numpy.log(pl_X)
# pl_Y_log=numpy.log(pl_Y)
# plt.title("Plot of 3rd Question")
# plt.xlabel("Length")
# plt.ylabel("Time")

# k,c=numpy.polyfit(pl_X_log,pl_Y_log,1)
# new_y=pow(pl_X,k)*numpy.exp(c)
#
# print k
#
# plt.loglog(pl_X,new_y)
# plt.show()