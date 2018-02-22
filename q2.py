from tree import Tree

rules = {}
terminals={}
total=0
max=0
freq=''
lines=[]

for line in open("train.trees.pre.unk"):

#with open("train.trees.pre.unk") as trees:
    #one=trees.readline()
    t=Tree.from_str(line)
    #print t
    for node in t.bottomup():
        if node.children==[]:
            continue
        counter=0
        right = ''
        for child in node.children:
            counter += 1
            if len(node.children) == 1: # check syntax
                if child.label not in terminals:
                    terminals[child.label] = set()
                terminals[child.label].add(node.label)
            if counter == 1:
                right = right + child.label
            else:
                right = right + ' ' + child.label
        for child in node.children:
            right = right + ' ' + child.label
        if node.label not in rules:
            rules[node.label] = {}
        if right in rules[node.label]:
            rules[node.label][right] += 1
        else:
            rules[node.label][right] = 1

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


print "\n",freq

print "Total Distinct Rules: ",total

for l in open("dev.strings"):
        lines.append(l);

first=lines[0].split()
print first

##parser
table=[0]*len(first)
for j in range(1,len(first)):
    for i in range(0,len(first)+1):
        table[j][i]=[]
print table


