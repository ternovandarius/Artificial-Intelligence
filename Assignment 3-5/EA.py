import numpy
import random

class EA:
    def __init__(self, size):
        self.__size=size
        self.__values=[]
        for i in range(1, size+1):
            self.__values.append(i)
            
    def individual(self):
        ind = []
        for i in range(0, self.__size*2):
            ind.append(numpy.random.permutation(self.__values))
        return ind
    
    def population(self, popSize):
        return [self.individual() for i in range(popSize)]
    
    def crossover(self, p1, p2):
        child=[]
        for i in range(len(p1)):
            if(random.randint(0,1)==0):
                child.append(p1[i])
            else:
                child.append(p2[i])
        return child
    
    def mutate(self, child, mP):
        if mP>random.uniform(0,1):
            child[random.randint(0, len(child)-1)]=numpy.random.permutation(self.__values)
        return child
    
    def fitness(self, ind):
        score = 0
        for i in range(0, len(ind)-1):
            for j in range(i+1, len(ind)):
                if (ind[i]==ind[j]).all():
                    score+=1
        visited=[]
        for j in range(0, self.__size):
            for i in range(0, len(ind)//2):
                if [ind[i][j],ind[i+len(ind)//2][j]] in visited:
                    score+=1
                else:
                  visited.append([ind[i][j],ind[i+len(ind)//2][j]])
        for j in range(0, self.__size):
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
            for j in range(0, self.__size):
                if ind[i][j] in visited:
                    score+=1
                else:
                    visited.append(ind[i][j])
        for i in range(len(ind)//2, len(ind)):
            visited=[]
            for j in range(0, self.__size):
                if ind[i][j] in visited:
                    score+=1
                else:
                    visited.append(ind[i][j])
        return score
    
    def iteration(self, pop, mP):
      i1=random.randint(0, len(pop)-1)
      i2=random.randint(0, len(pop)-1)
      if(i1!=i2):
        c=self.crossover(pop[i1], pop[i2])
        c=self.mutate(c, mP)
        f1=self.fitness(pop[i1])
        f2=self.fitness(pop[i2])
        fc=self.fitness(c)
        if f1>f2 and f1>fc:
          pop[i1]=c
        if f2>f1 and f2>fc:
          pop[i2]=c
      return pop
    
    def getBest(self, pop):
      minFitness=1000000
      best=[]
      for i in pop:
        currentFitness=self.fitness(i)
        if currentFitness<minFitness:
          minFitness=currentFitness
          best=i
      return best
    
class EAController:
    def __init__(self, size):
        self.__size=size
        self.__EA = EA(size)
        self.__population = []
    
    def control(self, pop, it, mP):
        self.__population = self.__EA.population(pop)
        for i in range(it):
            self.__population=self.__EA.iteration(self.__population, mP)
            
    def getBest(self):
        best = self.__EA.getBest(self.__population)
        bigstr=""
        for i in range(0, len(best)//2):
          strr=""
          for j in range(0, self.__size):
            strr+=str(best[i][j])+", "+str(best[i+len(best)//2][j])+"  "
          strr+="\n"
          bigstr+=strr
        return bigstr