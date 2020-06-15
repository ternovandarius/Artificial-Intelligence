from ACO import problem
import matplotlib.pyplot as pyplt

def runAco():
    squareSize=int(input("Square size: "))
    popSize=int(input("Population size: "))
    nrIter=int(input("Nr of iterations: "))
    nrAnts=int(input("Nr of ants: "))
    print("To save time, alpha=1.9, beta=0.9, rho=0.05, q=0.5\n")
    prob = problem()
    prob.loadProblem(squareSize, popSize, nrIter, nrAnts, 1.9, 0.9, 0.05, 0.5)
    print(prob.solveProblem())
    
def runTests():
    squareSize=int(input("Square size: "))
    popSize=int(input("Population size: "))
    nrIter=int(input("Nr of iterations: "))
    nrAnts=int(input("Nr of ants: "))
    print("To save time, alpha=1.9, beta=0.9, rho=0.05, q=0.5\n")
    std_dev=[]
    mean=[]
    for i in range(30):
        prob=problem()
        prob.loadProblem(squareSize, popSize, nrIter, nrAnts, 1.9, 0.9, 0.05, 0.5)
        s1,m1=prob.runTest()
        std_dev.append(s1)
        mean.append(m1)
    std=pyplt.plot(std_dev,color='b', label='Std. Dev')
    mean,=pyplt.plot(mean, color='r', label='Mean')
    pyplt.legend(handles=[std,mean])
    pyplt.show()
    
def main():
    #app = QApplication(sys.argv)
    #ui = QTUI()
    #sys.exit(app.exec_())
    while True:
        x=int(input("1. Run algorithm\n2.Run validation tests"))
        if x==1:
            runAco()
        elif x==2:
            runTests()
        else:
            print("Invalid command!")


main()