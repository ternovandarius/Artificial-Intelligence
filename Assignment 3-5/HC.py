import itertools
import copy
import numpy
import random

class HC:
    
    def __init__(self, size):
      self.__size=size
      self.__values=[]
      for i in range(1, size+1):
            self.__values.append(i)
      self.__permutations=numpy.array(list(itertools.permutations(self.__values)))
        
      
    def individual(self):
        ind = []
        for i in range(0, self.__size*2):
            ind.append(numpy.random.permutation(self.__values))
        return ind
      
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
      
    def getBest(self, pop):
        minFitness=1000000
        best=[]
        for i in pop:
          currentFitness=self.fitness(i)
          if currentFitness<minFitness:
            minFitness=currentFitness
            best=i
        return best
      
    def iteration(self, ind):
        surrounding = []
        for i in self.__permutations:
            for pos in range(self.__size*2-1):
              newInd=copy.deepcopy(ind)
              newInd[pos]=i
              surrounding.append(newInd)
        best = self.getBest(surrounding)
        if self.fitness(ind)<self.fitness(best):
          return ind
        else:
          return best
      
class HCController:
  
    def __init__(self, size):
      self.__size = size
      self.__HC=HC(size)
      self.__individual=self.__HC.individual()
      
    def control(self, iterations):
        for i in range(iterations):
          newind = self.__HC.iteration(self.__individual)
          if self.__HC.fitness(self.__individual)==self.__HC.fitness(newind):
            break
          else:
            self.__individual=newind
    
    def getBest(self):
        bigstr=""
        for i in range(0, len(self.__individual)//2):
          strr=""
          for j in range(0, self.__size):
            strr+=str(self.__individual[i][j])+", "+str(self.__individual[i+len(self.__individual)//2][j])+"  "
          strr+="\n"
          bigstr+=strr
        return bigstr
      