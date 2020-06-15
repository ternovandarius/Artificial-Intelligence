from random import *
import numpy
import copy

class particle:


    def __init__(self, size):
        self.values=[]
        self.size=size
        for i in range(1, size+1):
            self.values.append(i)
        self.position = []
        for i in range(0, size*2):
            self.position.append(numpy.random.permutation(self.values))
        self.evaluate()
        self.velocity = [ 0 for i in range(size*2)]
        self.bestPosition=self.position.copy()
        self.bestFitness=self.fitness


    def evaluate(self):
        self.fitness=self.fit(self.position)
    
    def fit(self, ind):
        score = 0
        for i in range(0, len(ind)-1):
            for j in range(i+1, len(ind)):
                if (ind[i]==ind[j]).all():
                    score+=1
        visited=[]
        for j in range(0, self.size):
            for i in range(0, len(ind)//2):
                if [ind[i][j],ind[i+len(ind)//2][j]] in visited:
                    score+=1
                else:
                  visited.append([ind[i][j],ind[i+len(ind)//2][j]])
        for j in range(0, self.size):
            visited1=[]
            visited2=[]
            for i in range(0, len(ind)//2):
                if ind[i][j] in visited1:
                    score+=1
                else:
                    visited1.append(ind[i][j])
            for i in range(len(ind)//2, len(ind)):
                if ind[i][j] in visited2:
                    score+=1
                else:
                    visited2.append(ind[i][j])
        for i in range(0, len(ind)//2):
            visited=[]
            for j in range(0, self.size):
                if ind[i][j] in visited:
                    score+=1
                else:
                    visited.append(ind[i][j])
        for i in range(len(ind)//2, len(ind)):
            visited=[]
            for j in range(0, self.size):
                if ind[i][j] in visited:
                    score+=1
                else:
                    visited.append(ind[i][j])
        return score

    def stringified(self):
        bigstr=""
        l = len(self.position)
        for i in range(l//2):
            strr=""
            for j in range(self.size):
                strr+=str(self.position[i][j])+","+str(self.position[i+l//2][j])+" "
            strr+="\n"
            bigstr+=strr
        return bigstr


class PSOController:
    
    def __init__(self, size, pop):
        self.population=[]
        self.getPopulation(size, pop)
    
    def getPopulation(self, size, pop):
        for i in range(pop):
            self.population.append(particle(size))
    
    def selectNeighbors(self, nSize):
        if nSize>len(self.population):
            nSize=len(self.population)

        neighbors = []
        for i in range(len(self.population)):
            localNeighbor = []
            for j in range(nSize):
                x = randint(0, len(self.population) - 1)
                while (x in localNeighbor):
                    x = randint(0, len(self.population) - 1)
                localNeighbor.append(x)
            neighbors.append(localNeighbor.copy())
        return neighbors
    
    def iteration(self, neighbors, c1, c2, w):
        bestNeighbors = []
        # determine the best neighbor for each particle
        for i in range(len(self.population)):
            bestNeighbors.append(neighbors[i][0])
            for j in range(1, len(neighbors[i])):
                if self.population[bestNeighbors[i]].fitness > self.population[neighbors[i][j]].fitness:
                    bestNeighbors[i] = neighbors[i][j]

        for i in range(len(self.population)):
            for j in range(len(self.population[0].velocity)):
                newVelocity = w * self.population[i].velocity[j]
                for k in range(len(self.population[0].position[0])):
                    newVelocity = newVelocity + c1 * random() * (self.population[bestNeighbors[i]].position[j][k] - self.population[i].position[j][k])
                    newVelocity = newVelocity + c2 * random() * (self.population[i].bestPosition[j][k] - self.population[i].position[j][k])
                self.population[i].velocity[j] = newVelocity

        for i in range(len(self.population)):
            newPosition = []
            for j in range(len(self.population[0].velocity)):
                newPosition.append(self.population[i].position[j])
            self.population[i].position = newPosition
            self.population[i].evaluate()
    
    def control(self, size, pop, iter, w, c1, c2):
        nSize=50
        neighborhood=self.selectNeighbors(nSize)
        for i in range(iter):
            self.iteration(neighborhood, c1, c2, w/ (i+1))
        best = self.population[0]
        for i in self.population:
            if i.fitness < best.fitness:
                best = i
        return best.stringified()