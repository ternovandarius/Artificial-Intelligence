import numpy as np
from math import floor

def read_data(split):
    
    #opens file, first reads by line and makes two lists, dependent and independent values
    lines = open("dataset.txt", "r").readlines()
    
    ind = []
    dep = []
    
    for l in lines:
        l=l.strip("\n")
        line = l.split(" ")
        print(line)
        
        if len(line)<6:
            continue
        new_ind = [float(i) for i in line[:-1]]
        new_dep = float(line[-1])
        ind.append(new_ind)
        dep.append(new_dep)
    
    
    #turn the independent array into a matrix
    newer_ind = []
    
    for i in range(len(ind)):
        new_ind=[1]+ind[i]
        newer_ind.append(new_ind)
    
    #turn the arrays into numpy arrays, as they support matrix operations
    last_ind = np.array(newer_ind)
    last_dep = np.array(dep)
    
    #if the split coefficient is 1, the training and test sets are equal
    if split==1:
        return last_ind, last_ind, last_dep, last_dep
    
    #else, return the training and test splits for independent and dependent values
    new_split = floor(len(last_dep)*split)
    return last_ind[:new_split], last_ind[new_split:], last_dep[:new_split], last_dep[new_split:]


def beta(ind, dep):
    #beta=[(ind'*ind)^-1]* ind'*dep, where ind' is the transposition of the ind matrix
    trans_ind = ind.transpose()
    first_multiplication = np.dot(trans_ind, ind)
    second_multiplication = np.dot(trans_ind, dep)
    inv = np.linalg.inv(first_multiplication)
    beta = np.dot(inv, second_multiplication)
    return beta
    
def predict(ind, beta):
    #to predict the value by getting the ind values, we use the computed beta
    #predicted response for a line will be beta[0]+beta[1]*ind[1]+beta[2]*ind[2]+...+beta[n]*ind[n], where n is the length of the ind
    total = 0
    for i in range(len(ind)):
        total += beta[i]*ind[i]
    return total

def analyze(ind, dep, beta):
    total = 0
    for i in range(len(ind)):
        dep_pred = predict(ind[i], beta)
        depp=dep[i]
        print("Ind: "+str(ind[i])+"\nPredicted: "+str(dep_pred)+", actual: "+str(depp)+", error: "+str(float(abs(depp-dep_pred))))
        total+=float(abs(depp-dep_pred))
        
    print("Total error: "+str(total))
        

def main():
    sp = float(input("Enter split."))
    training_ind, test_ind, training_dep, test_dep = read_data(sp)
    b = beta(training_ind, training_dep)
    analyze(test_ind, test_dep, b)
    
    
main()