from math import sqrt
import copy
import numpy
from random import randint

class matrix:
    def __init__(self, vals, n):
        self.vals=vals
        self.n=n
    
    def fitness(self):
        score = 0
        
        #line check
        for i in range(self.n):
            l=[]
            for j in range(self.n):
                l.append(self.vals[i][j])
            score+=len(l)-len(set(l))
        
        #column check
        for i in range(self.n):
            l=[]
            for j in range(self.n, self.n*2):
                l.append(self.vals[j][i])
            score+=len(l)-len(set(l))
        
        #check all pairs are different
        l=[]
        for i in range(self.n):
            j=self.n+i
            for k in range(self.n):
                l.append((self.vals[i][k], self.vals[j][k]))
        score+=len(l)-len(set(l))
        
        if (self.n * (self.n - 1)) * self.n - score <1:
            return 1
        return (self.n * (self.n - 1)) * self.n - score
    
    def __str__(self):
        msg=""
        n=len(self.vals)//2
        for i in range(n):
            j=n+i
            line=""
            for k in range(n):
                line+=" "+str(self.vals[i][k])+", "+str(self.vals[j][k])+" "
            line+="\n"
            msg+=line
        return msg
    
    def __eq__(self, o):
        for i in range(len(self.vals)):
            if self.vals[i]!=o.vals[i]:
                return False
        return True

class ant:
    
    def __init__(self, size, pop):
        self.size=size    #n from "nXn matrix"
        self.popSize=len(pop)
        self.pop=pop
        self.path=[randint(0, self.size*self.size - 1)]     #this chooses a random individual for the path start
        
    def nextValidMoves(self):
        next = []
        for i in range(self.size**2):
            if (i not in self.path):    #valid moves in path are those that aren't already in the path
                next.append(i)
        return next
    
    def calcMoveDistance(self, a):
        #puts move "a" in the path and checks the distance to the finish point
        newAnt = ant(self.size, self.pop)
        newAnt.path = self.path.copy()
        newAnt.path.append(a)
        return (self.size**2 - len(newAnt.nextValidMoves()))
    
    def addMove(self, trace, alpha, beta):
        posArr = [0 for i in range(self.size**2)]
        
        #if no more valid next moves, exit
        nextValidMoves = self.nextValidMoves()
        if len(nextValidMoves) == 0:
            return False
        
        #for each valid next move, we calculate the move distance
        for p in nextValidMoves:
            posArr[p] = self.calcMoveDistance(p)
            
        #formula
        posArr = [(posArr[i] ** beta) * (trace[self.path[-1]][i] ** alpha) for i in range(len(posArr))]
        
        #take the best possible next move, put it in path
        posArr = [[i, posArr[i]] for i in range(len(posArr))]
        posArr = max(posArr, key=lambda a: a[1])
        self.path.append(posArr[0])


    def getBest(self):
        #returns the best fitness of an individual from its path
        bestFit=self.pop[self.path[0]//self.size][int(self.path[0]%self.size)].fitness();
        for p in self.path:
          fit=self.pop[p//self.size][int(p%self.size)].fitness();
          if fit>bestFit:
              bestFit=fit
        return bestFit
        

class controller:
    
    def __init__(self):
        self.__values=[] #only used for creating permutations
        self.__pop=[] #a list of matrixes, which is the table the ants will move in
        self.__trace=[]
        
    def loadParameters(self, size, popSize, iterations, nrAnts, alpha, beta, rho, q):
        self.__size=size
        for i in range(1, size+1):
            self.__values.append(i)
        self.__popSize=popSize
        self.__iterations=iterations
        for i in range(int(sqrt(self.__popSize))):
            line=[]
            for j in range(int(sqrt(self.__popSize))):
                matr=[]
                for i in range(2*self.__size):
                    perm=numpy.random.permutation(self.__values)
                    perm=tuple(perm)
                    matr.append(perm)
                ind=matrix(matr, self.__size)
                line.append(ind)
            self.__pop.append(line)
        self.__nrAnts=nrAnts
        self.__alpha=alpha
        self.__beta=beta
        self.__rho=rho
        self.__q=q
        #for every individual, there's a matrix showing the pheromone trail between it and the others
        self.__trace=[[1 for i in range(popSize)] for j in range(self.__popSize)]
        
        
    def iteration(self):
        #create ant population
        antPop=[ant(self.__size, self.__pop) for i in range(self.__nrAnts)]
        #make the ants move around the board
        for i in range(self.__popSize):
            for j in antPop:
                j.addMove(self.__trace, self.__alpha, self.__beta)
        #update trace with all pheromones from ants
        newTrace=[1.0/antPop[i].getBest() for i in range(len(antPop))]
        for i in range(self.__popSize):
            for j in range(self.__popSize):
                self.__trace[i][j] = (1-self.__rho) * self.__trace[i][j]
        #update each individual's place in the trace
        for i in range(len(antPop)):
            for j in range(len(antPop[i].path) - 1):
                x=antPop[i].path[j]
                y=antPop[i].path[j+1]
                self.__trace[x][y]=self.__trace[x][y]+newTrace[i]
        
        #get ant with best fitness
        best=[[antPop[i].getBest(), i] for i in range(len(antPop))]
        best=max(best)
        #return its path
        return antPop[best[1]].path
        
    def runAlg(self):
        bestSol=[]
        
        #runs as many iterations as we told it, takes the longest path
        for i in range(self.__iterations):
            newSol=self.iteration()
            if len(newSol)>len(bestSol):
                bestSol=copy.deepcopy(newSol)
                
        bestFit=0
        euler=[]
        #checks best fitness from the longest path
        for sol in bestSol: 
            f = self.__pop[sol//int(sqrt(self.__popSize))][sol%int(sqrt(self.__popSize))].fitness()
            if f>bestFit:
                bestFit=f
                euler=self.__pop[sol//int(sqrt(self.__popSize))][sol%int(sqrt(self.__popSize))]
                
        return euler
    
    def runTest(self):
        #for each path given from an iteration, do the fitness of all individuals and return mean and std deviation
        fitnesses=[]
        for i in range(self.__iterations):
            newSol=self.iteration()
            for j in newSol:
                fitnesses.append(self.__pop[j//int(sqrt(self.__popSize))][j%int(sqrt(self.__popSize))].fitness())
        return (numpy.std(fitnesses), numpy.mean(fitnesses))

class problem:
    
    def __init__(self):
        self.__size=0
    
    def loadProblem(self, size=3, popSize=50, iterations=100, nrAnts=3, alpha = 1.9, beta=0.9, rho=0.05, q=0.5):
        self.__size=size
        self.__popSize=popSize
        self.__iterations=iterations
        self.__nrAnts=nrAnts
        self.__alpha=alpha
        self.__beta=beta
        self.__rho=rho
        self.__q=q
        
    def solveProblem(self):
        cont = controller()
        cont.loadParameters(self.__size, self.__popSize, self.__iterations, self.__nrAnts, self.__alpha, self.__beta, self.__rho, self.__q)
        return cont.runAlg()
    
    def runTest(self):
        cont = controller()
        cont.loadParameters(self.__size, self.__popSize, self.__iterations, self.__nrAnts, self.__alpha, self.__beta, self.__rho, self.__q)
        return cont.runTest()