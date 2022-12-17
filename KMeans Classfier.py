import numpy as np
import pandas as pd
import math
import random

from collections import Counter
from itertools import chain, combinations

dataset = pd.read_csv('Odor_Meter_Results.csv', header = None)
data = dataset.values


def Manhatten (perfume , centroid):
    sum_distances = 0
    for i in range(1, 26):
        sum_distances += abs(perfume[i] - centroid[i - 1])
    return sum_distances

def Eculiden (perfume , centroid):
    squared_distances = 0
    for i in range(1, 26):
        squared_distances += (perfume[i] - centroid[i - 1]) ** 2
    return math.sqrt(squared_distances)

def Distance(Type, perfume, centroid):
    if (Type == 1):
        #print("ecoo")
        disss = Eculiden(perfume, centroid)
    else:
        #print("Manooo")
        disss = Manhatten(perfume, centroid)
    #print("Yaaaaawww", disss)
    return disss
#--------------------------------------------------------------------------------------

def initiate_clusters (number_clusters):
    clusters = []
    for i in range(0, number_clusters):
        clusters.append([])
    return clusters

for i in data:
    for m in range(1, len(i)):
        f = i[m].replace(",","")
        i[m] = float(f)
#--------------------------------------------------------------------------------------

number_clusters = int(input('Enter Number of clusters: '))


Type = int(input("Enter 1 for Eculidean ... 0 for Manhatten: "))


centroids = []

randomNumbers = list(range(0,20)) # list of integers from 1 to 99
                              # adjust this boundaries to fit your needs
random.shuffle(randomNumbers)

for i in range(number_clusters):
    m = randomNumbers[i]
    print(m)
    cen = list(data[m]) # m badal el i
    cen.pop(0)
    centroids.append(cen)

#print("random: ",centroids)

iter_count = 1
Final_clusters = []

for iteration in range( 2, 1000):
    clusters = initiate_clusters(number_clusters)      # [ [], [], [] ]     number of clusters  = 3
    #print("ittt: ", iter_count)
#---------------------------------------------------------------
    for i in range(0, len(data)):
        perfume = data[i]
        #print(perfume[0])
        perfume_distances_centroids = []            # [ Distance 1, Distance 2, Distance 3 ]  if there are  3 centroids
        for c in range(0, len(centroids)):
            centroid = centroids[c]
            dist = Distance(Type, perfume, centroid)
            perfume_distances_centroids.append(dist)
        #print ("menn:   ",perfume_distances_centroids )
        get_Minimum = min(perfume_distances_centroids)              # if Distance 2 is minimum then, add it to the second cluster
        cluster = perfume_distances_centroids.index(get_Minimum)        # [ [], [ it here add ], [], ]
        # print(i, " : ", perfume_distances_centroids, "lll", get_Minimum,"cluster: ",cluster)
        clusters[cluster].append(i)
    Mean = []   # New Centroids
    for i in range(0, len(clusters)):
        denominator = len(clusters[i])
        #print("len of cluster:", denominator)
        clusterr = clusters[i]
        #print(clusterr)
        coordinates = []
        for sec in range(1, len(perfume)):
            numerator = 0
            for i in range(0, len(clusterr)):
                # print(clusterr[i])
                perfume = data[clusterr[i]]
                numerator += perfume[sec]
            coordinates.append(numerator / denominator)
        Mean.append(coordinates)
    #print ("mean: ",Mean)
    #print("cll: ", clusters)
    #for i in range(0 , len(Mean)):
        #print ("mean: ", Mean[i])
    if (Mean == centroids):
        Final_clusters = clusters
        break
    centroids = Mean
    iter_count = iteration


print("stopped at iteration: ",iter_count)
print()


#perfume = list(data [1])
#centroidd = centroids[0]
#sum_distances = 0
#for i in range(1, 26):
 # sum_distances += abs(perfume[i] - centroid[i - 1])
#dist = Eculiden(perfume,centroidd)
#print("pp",sum_distances, dist)


for c in range (0 , len(Final_clusters)):
    print ("Cluster :",c+1)
    #print(Final_clusters[c])   # print el indexes
    m = Final_clusters[c]
    for i in range (0 , len(m)):
        perfume_name = data[m[i]]
        print(perfume_name[0])
    print()
#-------------------------------------------------------------------

#--------------------------------------------------------------------
#for i in centroids:
    #print("len : ", len(i),i)

distances = []
outliers = []
#---------------------------------------------------------------------------------------
for i in range (0, len(Final_clusters)):
    for j in Final_clusters[i]:
        dis = Distance(Type, data[j], centroids [i])
        distances.append(dis)
#print(distances)
distances = sorted(distances)
#print(distances)
#print(len(distances) == len(set(distances)))

#----------------------------------------------------------------------------------------

# Outliers for all Data

percentile = 80
#print("percentt: ",np.percentile(distances, percentile))
for_All_Data_outliers = []
Distances_for_each_cluster = initiate_clusters(number_clusters)
for i in range (0, len(Final_clusters)):
    m = Distances_for_each_cluster[i]
    for j in Final_clusters[i]:
        perfume_ = data[j]
        dis = Distance(Type, data[j], centroids [i])
        m.append(dis)
        if dis > np.percentile(distances, percentile):
            for_All_Data_outliers.append(perfume_[0])
print("For all data Outliers: ")
print (for_All_Data_outliers)
print()

#print(Distances_for_each_cluster)
#----------------------------------------------------------------------------------------

# Outliers for each Cluster

print("Outliers for each Cluster")
for c in range(0, len(Distances_for_each_cluster)):
    print("Cluster :", c + 1)
    # print(Final_clusters[c])   # print el indexes
    m = Distances_for_each_cluster[c]
    m = sorted(m)
    k = Final_clusters[c]
    outlier_for_this_cluster = []
    #print("m : ", m)
    #print("pec: ",np.percentile(m, percentile))
    for i in range(0, len(k)):
        perfume = data[k[i]]
        dis = Distance(Type, data[k[i]],centroids[c])
        if dis > np.percentile(m, percentile):
            outlier_for_this_cluster.append(perfume[0])
            # outlier_for_this_cluster.append(dis)
    print(outlier_for_this_cluster)
    print()









#quantile1, quantile3 = np.percentile(distances,[20,80])

quantile1 = np.percentile(distances, 20, interpolation = "midpoint") # The lower quartile Q1 is calculated.
quantile3 = np.percentile(distances, 80, interpolation = "midpoint") # The upper quartile Q3 is calculated.

#print(quantile1,quantile3)

## Find the IQR

iqr_value = quantile3 - quantile1
#print(iqr_value)

## Find the lower bound value and the higher bound value

lower_bound_val = quantile1 - (1.5 * iqr_value)
upper_bound_val = quantile3 + (1.5 * iqr_value)
#print(lower_bound_val,upper_bound_val)





