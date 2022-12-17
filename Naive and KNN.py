import numpy as np
import pandas as pd
import math
import random
import csv

def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return i, x.index(v)

def Sort(sub_li):
    l = len(sub_li)
    for i in range(0, l):
        for j in range(0, l-i-1):
            if (sub_li[j][1] > sub_li[j + 1][1]):
                tempo = sub_li[j]
                sub_li[j]= sub_li[j + 1]
                sub_li[j + 1]= tempo
    return sub_li
def most_frequent(List):
    return max(set(List), key=List.count)

#-----------------------------------------------------------------------
dataset = pd.read_csv('car_dataa.csv')
#dataset = dataset.sample(frac=1).reset_index(drop=True)
size = dataset.shape[0]
ratio = 0.75
slicer = int(ratio * size)
#print("slicer.", slicer)
train = dataset[:slicer]
test = dataset[slicer:]
#------------------------------------------------------------------------
size_Train = train.shape[0]
#print("size: ", size_Train)
Car_Acceptability = train['Car Acceptability']

VV = train['Car Acceptability'].value_counts()
print(VV)
#for val in VV:
   # print(val)
ClassLabel_Values = list(Car_Acceptability.unique())
#print(ClassLabel_Values)
ClassLabel_P = list(train['Car Acceptability'].value_counts().values.tolist())
#print(ClassLabel_P)
ClassLabelCar = list(train['Car Acceptability'].value_counts().reset_index().values.tolist())
#print(ClassLabelCar)
K = []
L = []
for listt in ClassLabelCar:
    K.append(listt[1])
    L.append(listt[0])
#print(L,K)
ClassLabel_Values = L
ClassLabel_P = K
#----------------------------------------------------------------------------------
#print(ClassLabel_Values)
#print(ClassLabel_P)
#d = train[['Buying Price', 'Car Acceptability']]
#print(d.value_counts())
#m = d.value_counts()
#print("ll:" ,m.reset_index().values.tolist())
#print(d.value_counts().high.acc)
#print("nada")



Features = train.keys().tolist()                 # Columns' names
Features = Features[:-1]        # ['Buying Price', 'Maintenance Price', 'Number of Doors', 'Capacity', 'Size of Luggage Boot', 'Car Safety']
ClassLabel = 'Car Acceptability'
Possibilities = dict()          # Naive
KnnMap = dict()                 # KNN
#--------------------------------------Mapping Naive ------------------------------------------
for feat in Features:
    #print("Feature: ",feat)
    d = train[[feat, ClassLabel]]
    knn = dataset[feat].unique()
    #print(d.value_counts())
    m = d.value_counts()
    print (m)
    possbility = m.reset_index().values.tolist()
    #print("henaa",possbility)
    if (feat not in Possibilities):
        Possibilities[feat] = list()
    Possibilities[feat]= possbility

for label in Possibilities:
    #print(label)
    for row in Possibilities[label]:
        #print("Before: ", row)
       # m , n = index_2d(ClassLabelCar, row[1] )            # ['unacc', 'acc', 'vgood', 'good']
        index = ClassLabel_Values.index(row[1])             # [952, 295, 26, 23]
        #print("Lolo:  ",row, "  ", row[1], ClassLabelCar[m][n+1], ClassLabelCar[m][n])
        row[2] = row[2] / ClassLabel_P [index]
        #print("After: ",row)

for p in range(0, len(ClassLabel_P)):
    ClassLabel_P[p] = ClassLabel_P[p] / size_Train
#print(ClassLabel_P)
#------------------------------------Mapping of KNN---------------------------------------
for feat in Features:
    knn = dataset[feat].unique()
    print(knn)
    if (feat not in KnnMap):
        KnnMap[feat] = list()
    KnnMap[feat] = list(knn)

#-------------------------------------------END-------------------------------------------

Actual = []
Predicted = []          # Acurracy for Naive

test = list(test.values)
for row in range(0,len(test)):
    test[row] = test[row].tolist()
    Actual.append(test[row][-1])
    test[row] = test[row][:-1]
    #print(row)
#print(test)
print("------------------------------------------------------------------------")
for row in test:
    Probability = []
    Label = ""
    for label in ClassLabel_Values:
       # print("car accessapility: ",label)
        Product = 1
        P = 0
        #print(row)
        for element in range(0, len(row)):
            for i in Possibilities[Features[element]]:
                if i[0] == row[element] and i[1] == label:
         #           print(i[0],row[element] ,i[1],label)
                    Product = Product * i[2]
                else:
                    Product = Product *0
        #print(Product)
        Product = Product*(ClassLabel_P[ClassLabel_Values.index(label)])
        Probability.append(Product)
    Predicted.append(ClassLabel_Values[Probability.index(max(Probability))])
#print(Predicted)
#print(Actual)



train = list(train.values)
for row in range(0,len(train)):
    train[row] = train[row].tolist()
#print("ooo: ",testtt, "lll: ", type(train[0]))

correct = 0
for i in range (0, len (test)):
    if Actual [i] == Predicted [i]:
        correct = correct+1
print(correct)
print("Acurracy for Naive: ", correct/len(test)*100)
#print("length of actual: ", len(Actual), "length of Predicted: ", len(Predicted))
#print(Actual)


#-------------------------------------------------------------KNN--------------------------------------
#Knn = int(input('Enter Number of KNN: '))
Knn = 4

#for label in KnnMap:
    #print(label, "  :")
    #print(KnnMap[label])
Predicted_KNN =[]
for row in range (0, len(test)):
    t1 = test[row]
    distances = []
    for r in range(0, len(train)):
        l = []
        l.append(r)
        t2 = train[r]
        squared_sum =0
        distance =0
        for i in range (0, len(Features)):
            P = KnnMap[Features[i]]
            #print("Feat, ", P, t1[i], t2[i], P.index(t1[i]), P.index(t2[i]))
            squared_sum += (P.index(t1[i]) - P.index(t2[i])) ** 2
        distance = math.sqrt(squared_sum)
        l.append(distance)
        l.append(t2[len(t2) - 1])
        distances.append(l)
    distances = Sort(distances)
    Frequent = []
    for i in range(0 , Knn):
        Frequent.append(distances[i][2])
    #print("-----")
    #print(Frequent)
    Predicted_KNN.append(most_frequent(Frequent))


print(Predicted_KNN)

#for i in range (0, len(Features)):


#print(k)


correct = 0
for i in range (0, len (test)):
    if Actual [i] == Predicted_KNN [i]:
        correct = correct+1
print(correct)
print("Acrracy for KNN: ", correct/len(test)*100)



