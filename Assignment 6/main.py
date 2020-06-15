from math import floor
from statistics import mean
import random

def read_data():
    db = []
    lines = open("DECISION/balance-scale.data", "r").readlines()
        
    for line in lines:
        actual_line = line.split(",")
        actual_line[len(actual_line)-1] = actual_line[len(actual_line)-1][0]
        for i in range(1, len(actual_line)):
            actual_line[i]=float(actual_line[i])
        db.append(actual_line)
        
    return db

def split_data(db, p):
    #if p is 1, then the training and test sets are equal
    if p==1:
        return db, db
    #if not, we shuffle the set and make the split
    actual_split = floor(p*len(db))
    random.shuffle(db)
    train=db[:actual_split]
    test=db[actual_split:]
    return train, test

def unique_vals(rows, col):
    #finds unique values for a column
    return set([row[col] for row in rows])

def class_counts(rows):
    #counts each class in set
    counts = {}
    for i in rows:
        label=i[0]
        if label not in counts:
            counts[label]=0
        counts[label]+=1
    return counts

class Question:
    
    def __init__(self, col, val):
        self.column=col
        self.value=val
        
    def match(self, c):
        val = c[self.column]
        if isinstance(val, int) or isinstance(val, float):
            return val>=self.value
        else:
            return val==self.value
        
    
def partition(rows, question):
    true=[]
    false=[]
    for row in rows:
        if question.match(row):
            true.append(row)
        else:
            false.append(row)
    return true, false

def gini(rows):
    counts = class_counts(rows)
    impurity=1
    for cl in counts:
        prob = counts[cl] / float(len(rows))
        impurity-=prob**2
    return impurity

def info_gain(left, right, current_uncertainty):
    p=float(len(left))/(len(left) + len(right))
    return current_uncertainty-p*gini(left) - (1-p)*gini(right)

def best_split(rows):
    best_gain=0
    best_question=None
    current_uncertainty = gini(rows)
    
    for col in range(1, 5):
            
        values = unique_vals(rows, col)
    
        for val in values:
            q = Question(col, val)
            
            true, false = partition(rows, q)
            
            if len(true)!=0 and len(false)!=0:
                gain = info_gain(true, false, current_uncertainty)
                
                if gain>=best_gain:
                    best_gain = gain
                    best_question=q
                    
    return best_gain, best_question

class Decision_Node:
    """A Decision Node asks a question.
    This holds a reference to the question, and to the two child nodes.
    """

    def __init__(self,
                 question,
                 true_branch,
                 false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch
        
class Leaf_Node:
    def __init__ (self, prediction):
        self.prediction = prediction
        
        
def build_tree(data):
    #entropy is 0, we return a leaf node with the label remaining
    if len(set(i[0] for i in data))==1:
        return Leaf_Node(data[0][0])
    #try partitioning dataset on each unique attribute
    gain, question = best_split(data)
    #gain==0 => no questions left to answer
    if gain==0:
        counts = class_counts(data)
        return Leaf_Node(max(counts, key = counts.get))
    
    #if gain is not 0, make true and false branch and return a decision node containing the question and the branches
    true, false = partition(data, question)
    
    true_tree = build_tree(true)
    false_tree = build_tree(false)
    return Decision_Node(question, true_tree, false_tree)
    
def classify(inst, node):
    if isinstance(node, Leaf_Node):
        return node.prediction
    
    if node.question.match(inst):
        return classify(inst, node.true_branch)
    else:
        return classify(inst, node.false_branch)
    
def test_tree(tree, test):
    track = []
    for i in test:
        real = i[0]
        predicted = classify(i, tree)
        track.append(bool(real==predicted))
    print("Accuracy: " + str(float(track.count(True))/len(track)))
    return track.count(True)/len(track)
        
def main():
    p = float(input("Insert split (accuracy between 0 and 1, split*length will go into training)."))
    data = read_data()
    accs = []
    for i in range(100):
        train, test = split_data(data, p)
        tree = build_tree(train)
        accs.append(test_tree(tree, test))
    print("Average accuracy in 100 test runs: " + str(mean(accs)))
    
main()