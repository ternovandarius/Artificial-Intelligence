import numpy as np
from math import floor
import statistics
import matplotlib as mp

def read_data(split, hidden):
    
    #opens file, first reads by line and makes two lists, dependent and independent values
    lines = open("dataset.txt", "r").readlines()
    
    ind = []
    dep = []
    
    for l in lines:
        l=l.strip("\n")
        line = l.split(" ")
        
        if len(line)<6:
            continue
        l = [[float(i)] for i in line]
        #last value is kept for the dep list
        new_ind = l[:-1]
        new_dep = l[-1]
        ind.append(np.array(new_ind))
        dep.append(np.array(new_dep))
    

    
    #turn the arrays into numpy arrays, as they support matrix operations
    last_ind = np.array(ind)
    last_dep = np.array(dep)
    
    #if the split coefficient is 1, the training and test sets are equal
    if split==1:
        return last_ind, last_ind, last_dep, last_dep
    
    #else, return the training and test splits for independent and dependent values
    new_split = floor(len(last_dep)*split)
    layers = [last_ind[0].shape[0], hidden, last_dep[0].shape[0]]
    return layers, last_ind[:new_split], last_ind[new_split:], last_dep[:new_split], last_dep[new_split:]

def activation(x):
    #identity function f(x) = x
    return x

def deriv_activ(x):
    #derivate of f(x)=x => f'(x)=1
    return 1

class ANN:
    
    def __init__(self, layers, rate, coef):
        self.layers = layers
        self.rate = rate
        self.coef = coef
        
        self.w1 = np.random.rand(layers[0], layers[1])
        self.w2 = np.random.rand(layers[1], layers[2])
        
        self.b1 = np.random.rand(layers[1])
        self.b2 = np.random.rand(layers[2])
        
        self.layer1 = None
        
        self.loss=[]
        self.iters=[]
        
    def feed_forward(self, inputt):
        #takes values from input layer and passes them through algorithm
        #activation(w2 * activation(w1 * inputt + b1) + b2)
        self.layer1 = activation(np.dot(inputt, self.w1)+ self.b1)
        return activation(np.dot(self.layer1, self.w2) + self.b2)
    
    def back_propag(self, ind, dep, pred):
        #updates weights based on the error
        back1= (dep-pred) * deriv_activ(pred)
        back2= np.dot(2*back1, self.w2.T) * deriv_activ(self.layer1)
        back2_w2 = np.dot(self.layer1.T, 2*back1)
        back1_w1 = np.dot(ind.T, back2)
        
        self.w1 += self.rate * back1_w1 * (1/self.coef)
        self.w2 += self.rate * back2_w2 * (1/self.coef)
        
    def train(self, ind, dep, iters):
        pos = 0
        for i in range(iters):
            x = ind[pos].T
            y = dep[pos].T
            y_exp = self.feed_forward(x)
            self.back_propag(x, y, y_exp)
            self.loss.append(np.sum((np.square(y_exp - y))/2))
            self.iters.append(i)
            pos = (pos+1)%(len(ind))
            
    def test(self, ind, dep):
        pos = 0 
        err = []
        while (pos<len(ind)):
            x = ind[pos].T
            y = dep[pos].T
            current_error = np.sum((np.square(self.feed_forward(x[0]) - y[0]))/2)
            err.append(current_error)
            pos+=1
        print(statistics.mean(err))
    

def main():
    sp = float(input("Enter split."))
    hidden_neurons = 6
    layer, training_ind, test_ind, training_dep, test_dep = read_data(sp, hidden_neurons)

    iterations = 1000
    rate = 0.0001
    coef = 10
    
    neural = ANN(layer, rate, coef)
    neural.train(training_ind, training_dep, iterations)
    neural.test(test_ind, test_dep)
    
    mp.pyplot.plot(neural.iters, neural.loss)
    mp.pyplot.show()
    
main()