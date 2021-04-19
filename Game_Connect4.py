# -*- coding: utf-8 -*-

import numpy as np
from random import randint
from collections import Counter


mat=np.zeros((6, 7)).astype(int)
l0, l1, l2,l3, l4, l5, l6 = ([] for i in range(7))

       
def clear():
    global mat
    global l0, l1, l2,l3, l4, l5, l6
    matrix=np.zeros((6, 7)).astype(int)
    l0, l1, l2,l3, l4, l5, l6 = ([] for i in range(7))
    
matrix=np.zeros((6, 7)).astype(int)  
    
def play(player,where,matrix):
    
    if where==0:
        idx=6  if np.count_nonzero(matrix[:,0])==0 else  min(np.nonzero(matrix[:,0])[0])
        matrix[idx-1,where]=player 
         
    elif where==1:
        idx=6  if np.count_nonzero(matrix[:,1])==0 else min(np.nonzero(matrix[:,1])[0]) 
        matrix[idx-1,where]=player 
        
    elif where==2:
        idx=6  if np.count_nonzero(matrix[:,2])==0 else min(np.nonzero(matrix[:,2])[0])
        matrix[idx-1,where]=player 
        
    elif where==3:
        idx=6  if np.count_nonzero(matrix[:,3])==0 else min(np.nonzero(matrix[:,3])[0])
        matrix[idx-1,where]=player 
        
    elif where==4:
        idx=6  if np.count_nonzero(matrix[:,4])==0 else min(np.nonzero(matrix[:,4])[0])
        matrix[idx-1,where]=player  
        
    elif where==5:
        idx=6  if np.count_nonzero(matrix[:,5])==0 else min(np.nonzero(matrix[:,5])[0])
        matrix[idx-1,where]=player    
                
    elif where==6:
        idx=6  if np.count_nonzero(matrix[:,6])==0 else min(np.nonzero(matrix[:,6])[0]) 
        matrix[idx-1,where]=player   
                   
    return (idx,where)  
    
#play(2,4,matrix)
          

def win(mat):    

    #diag1
    for j in range(len(mat.T)-4):
        for i in range(len(mat)-2):
            
            if mat[j,i]==mat[j+1,i+1]==mat[j+2,i+2]==mat[j+3,i+3]==1:
                #print((j,i),(j+1,i+1),(j+2,i+2),(j+3,i+3))
                return 1
            
            if  mat[j,i]==mat[j+1,i+1]==mat[j+2,i+2]==mat[j+3,i+3]==2:
                #print((j,i),(j+1,i+1),(j+2,i+2),(j+3,i+3))
                return 2  
        
    #diag2
   
    for j in range(len(mat.T)-2,2,-1):
        for i in range(len(mat)-2):
            
            if mat[j,i]==mat[j-1,i+1]==mat[j-2,i+2]==mat[j-3,i+3]==1:
                #print((j,i),(j-1,i+1),(j-2,i+2),(j-3,i+3))
                return 1
                
            if mat[j,i]==mat[j-1,i+1]==mat[j-2,i+2]==mat[j-3,i+3]==2:
                #print((j,i),(j-1,i+1),(j-2,i+2),(j-3,i+3))
                return 2
    
            
            
    #horiz       
    for j in range(len(mat.T)-1):
        for i in range(len(mat)-2):        
        
                if mat[j,i]==mat[j,i+1]==mat[j,i+2]==mat[j,i+3]==1: 
                    #print((j,i),(j,i+1),(j,i+2),(j,i+3))
                    return 1
                    
                if mat[j,i]==mat[j,i+1]==mat[j,i+2]==mat[j,i+3]==2:
                    
                    #print((j,i),(j,i+1),(j,i+2),(j,i+3))
                    return 2
                
    #vert   
              
    for j in range(len(mat)-3):
        for i in range(len(mat.T)):   
                if mat[j,i]==mat[j+1,i]==mat[j+2,i]==mat[j+3,i]==1:
                    #print((j,i),(j+1,i),(j+2,i),(j+3,i)) 
                    return 1
                
                if mat[j,i]==mat[j+1,i]==mat[j+2,i]==mat[j+3,i]==2:
                    
                    #print((j,i),(j+1,i),(j+2,i),(j+3,i)) 
                    return 2
                

def test(matrix):
        x=randint(0,6) 
        if np.count_nonzero(matrix[:,x])==6:  
            return test(matrix) 
        else:
            return x   
       


