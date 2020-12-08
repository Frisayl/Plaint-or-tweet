from StableNaiveBayes import StableNaiveBayes
import numpy as np

'''
Naive Bayes where:
each feature Xi has domain in {0,1,2,...}
and each y is in {0,1}
'''
class MultinomialNaiveBayes(StableNaiveBayes):
    def __init__(self):
        # Dataset dimension
        self.m = 0
        # Number of training examples where y=1
        self.count_y_1 = 0 
        # Number of training examples where y=0
        self.count_y_0 = 0 

        # 1D vector -> [p_y0, p_y1]
        self.th1 = [] 

        # 2D vector -> [[px0_given_y0, px1_given_y0, px2_given_y0, ... ], 
        #              [px0_given_y1, px1_given_y1, px2_given_y1, ... ]]]
        self.th2 = [[],[]] 
                    

    # X and y must be numpy arrays
    # each row of X is a training example
    # Trains the two model parameter types:
    # theta1[i] -> N(yi)/m
    # theta2[i][j] -> N(xj, yi)/N(yi)
    def train(self, X, y):

        self.m += len(y)
        self.count_y_1 += np.count_nonzero(y) #nonzero == 1

        # Training theta1
        self.th1.append(p_y(0))
        self.th1.append(p_y(1))

        # Number multinomial values
        mul_num = np.max(X) + 1


        # Initializing theta2
        for i in range(mul_num):
            self.th2[0].append(0) 
            self.th2[1].append(0) 

        # Training theta2
        for i in range(len(X)):
            for j in range(X.shape[1]):
                # Obtaining N(xj, yi)
                self.th2[y[i]][X[i][j]] += 1
        for j in range(mul_num):
            self.th2[0][j] = (self.th2[0][j] + 1) / (self.count_y_0 + mul_num) # Applying Laplace smoothing
            self.th2[1][j] = (self.th2[1][j] + 1) / (self.count_y_1 + mul_num) # same here
    

    def p_y(self, y):
        p1 = (self.count_y_1 + 1) / (self.m + 2) #+1/+2 are due to Laplace smoothing
        return p1 if y == 1 else (1 - p1)


    # Makes a prediction, given the features vector X.
    # The model has to be previously trained.
    def predict(self, X):
        y0 = self.th1[0] * np.product([self.th2[0][j] for j in range(len(X))])
        y1 = self.th1[1] * np.product([self.th2[1][j] for j in range(len(X))])
        return 0 if y0 > y1 else 1
        