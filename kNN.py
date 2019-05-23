'''
CPSC427
Team Member 1: Andrew Abbott
Submitted By: Andrew Abbott
GU Username: aabbott
File Name: kNN.py
Program reads in files into a training matrix and then compares files that need classification into another matrix.
Then the program classifies the files needing classification based on the kNN algorithm. Then the program returns
the number of misclassifications and error rate.
To Execute: python prog4.py
Python Version 2.7.10
'''

from kNN import *
from os import listdir
import math


'''
file_lst is the list of file names containing training or test data.  path is
the path from the code to where the data is stored.  train_matrix is an N X 1024
matrix of training/test data where each row is the contents of one of the
training files
pre: the path is specified
post: a matrix is returned that contains all of the files in the specified directory
'''
def make_matrix(path):
    file_lst = listdir(path)
    m = len(file_lst)
    i = 0
    train_matrix = zeros((m,1024), dtype = int)
    for trainFile in file_lst:
        #print('file name: ' + trainFile)
        trainVect = img2vector(trainFile,path)
        train_matrix[i] = trainVect
        i = i + 1
    return train_matrix
'''
Each training, test file is a 32X32 matrix of 0's and 1's.  The goal is to
transform the matrix into a vector, where 32nd position of the vector begins
with the 0th item in the 1st row the matrix. This function and the following
one unpacks a 2-D array into a 1-D array.
pre: file_name contains the name of the file to be transformed, path is specified
post: the contents of the file are returned in a 1x1024 vector are returned
'''
def img2vector(file_name,path):
    file_name = path+file_name
    f = open(file_name, 'r')
    vect = zeros((1,1024)) #store zeros in a 1X1024 vector.
    for i in range(32):
        line = f.readline()
        for j in range(32):
            vect[0, 32*i+j] = int(line[j])
    return vect

'''
file_lst is the list of file names containing training or test data.
Every file name begins with a digit, as in 1_160.txt.  This function and
the following one extracts the initial digit and stores it in a list
pre: path is specified
post: a list of labels containing the labels stripped from the file is returned
'''
def make_labels(path):
    file_lst = listdir(path)
    m = len(file_lst)
    vect = []
    for i in range(m):
        fle = file_lst[i]
        section = class_number(fle)
        vect.append(section)
    return vect

'''
extract the class number from the file name and return it to make_labels
pre: file_name contains the name of the file to extract the class number from
post: the class number has been extracted and returned
'''
def class_number(file_name):
    section = file_name.split('_')
    return int(section[0])

'''
pre: time and m contain integers
post: the current progress is printed to the screen
'''
def timer_function(timer, m):
    #I use this to print a periodic message to the user so that s/he
    #knows that things are progressing well
    timer = timer + .0
    percent = timer / m * 100
    
    print(str(round(percent,2)) + '% complete...\n\n\n\n\n')
    

'''
test all of the files in the test directory
pre: test_path contains the path to the training files, train_matrix is a matrix that contains the the files
that are to be compared against, train_labels contains the corresponding labels to train_matrix, k contains
the desired number of nearest neighbors. 
post: the number of incorrect classifications is printed to the screen 
'''
def test_classifier(test_path, train_matrix, train_labels, k):
    file_lst = listdir(test_path)
    m = len(file_lst)
    test_labels = make_labels(test_path)
    test_matrix = make_matrix(test_path)
    errors = 0
    for i in range(m):
        current_vector = test_matrix[i,:]

        if i % 50 == 0:
            timer_function(i,m)
        if i == m-1:
            print('100% complete...\n\n\n')
      
        response = classify(current_vector,train_matrix,train_labels,k)

        if response != test_labels[i]:
            errors = errors + 1
        
    print ("Total Errors: " + str(errors))
    print ("Error Rate: " + str(float(errors)/float(m)))
         
def main():
    k = 3
    train_path = 'trainingDigits/'
    test_path = 'testDigits/'
   
    train_labels = make_labels(train_path)
    train_matrix = make_matrix(train_path)
    
    test_classifier(test_path,train_matrix,train_labels,k) 
    
main()
