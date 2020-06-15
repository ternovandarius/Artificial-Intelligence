import random

class gradient:

    def __init__(self):
        self.db = []
        
        lines = open("dataset.txt", "r").readlines()
        
        for line in lines:
            if line!="\n":
                actual_line = line.split(" ")
                actual_line[len(actual_line)-1] = actual_line[len(actual_line)-1][:-1]
                actual_actual_line = [float(nr) for nr in actual_line]
                self.db.append(actual_actual_line)
            
        self.weights=[random.randint(-50, 50) for x in range(len(self.db[0]))]
        self.rate=0.001
        
    def solve(self):
        for i in range(1000):
            gradient=[0 for x in range(len(self.db[0]))]
            
            for line in self.db:
                t=line[-1]
                total=self.weights[-1]
                for i in range(len(self.db[0])-1):
                    total+=self.weights[i]*line[i]
                for i in range(len(self.db[0])-1):
                    gradient[i]+=-(2/float(len(self.db)))*line[i]*(t-total)
                gradient[len(self.db[0])-1]+=-(2/float(len(self.db)))*(t-total)
                
            for i in range(len(self.db[0])):
                self.weights[i]-=(self.rate*gradient[i])
            
        print(self.weights)
        
    def get_error(self):
        total = 0
        for line in self.db:
            new=self.weights[-1]
            for i in range(len(self.db[0])-1):
                new+=self.weights[i]*line[i]
            total+= (abs(line[-1]-new)) ** 2
        total=total/float(len(self.db))
        print(total)
    
g = gradient()
g.solve()
g.get_error()

#[2.000226610710134, 4.000352757178584, 3.0004855180478285, -2.0009250926557143, -1.0001215003565913, 2.608959408536604]
#0.1516206071785286

#[1.9996533902401663, 3.999547475822383, 2.9995978843213313, -1.9990306201511496, -0.9999422615952125, 3.4104056959270213]
#0.16892488641893522

#[2.0000513965586757, 4.000106609846267, 3.000214198375307, -2.0003460163495816, -1.000066713116552, 2.85393448975208]
#0.021556760514439922