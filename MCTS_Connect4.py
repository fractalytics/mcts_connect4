# -*- coding: utf-8 -*-
from anytree import AnyNode, RenderTree,Node, AsciiStyle,search,PreOrderIter,Resolver,PreOrderIter

%run "game_connect4.py"


import time 
from tqdm import tqdm   
import random


def player2_strategie_game(matrix,key_max_result_sim):
            
     
     player2=available_play(matrix)
     #♣player2.remove(key_max_result_sim)
     for i in player2:
        matrix_1=matrix.copy()
        matrix_2=matrix.copy()
        
        play(1,i[1],matrix_1)
             
        if win(matrix_1)==1:
             return i[1]
             break
             
        play(2,i[1],matrix_2)
         
        if win(matrix_2)==2:
             return i[1]
             break
         
     return  random.choice(available_play(matrix))[1]

def MC(matrix,nbsim):
    L=[] 
    Prob_MC = {}
    for z in np.where((matrix != 0).sum(0) != 6)[0]:
        matrix_sel=matrix.copy()
        play(1 if np.count_nonzero(matrix_sel==1)<=np.count_nonzero(matrix_sel==2) else  2 ,z, matrix_sel)
        for k in range(nbsim):
            matrix_tmp=matrix_sel.copy()
            for i in range(np.count_nonzero(matrix_tmp==0)):
               play(1 if np.count_nonzero(matrix_tmp==1)<=np.count_nonzero(matrix_tmp==2) else  2 ,test(matrix_tmp.copy()), matrix_tmp) 
               if win(matrix_tmp)==1: 
                        L.append((z,1)) 
                        break
                    
               if win(matrix_tmp)==2: 
                        L.append((z,2))
                        break
                    
        d=dict(Counter(elem for elem in L))  
        if  nbsim == d[(z,1)] :
            Prob_MC[z]=2
        else:    
            Prob_MC[z]=round(d[(z,1)]/(d[(z,1)]+d[(z,2)]),2)                
                    
        
    return  Prob_MC


def player_turn(matrix):
    
    if (np.count_nonzero(matrix == 1)==np.count_nonzero(matrix == 2)):
        
        return 1
    
    elif(np.count_nonzero(matrix == 1)>np.count_nonzero(matrix == 2)):
        
        return 2
#check all children available to play
def available_play(matrix):
    
    col=np.where(~matrix.all(axis=0))[0].tolist()

    row=np.where((matrix[:,col]!=0).argmax(axis=0)==0, 6, (matrix[:,col]!=0).argmax(axis=0)).tolist() 
    
    av_pl_lst=list(zip(row, col))
    
    if av_pl_lst!=[]:
        
         return list(zip(row, col))
    else:
         return None


def update_tree(game_lst,game_tree):
       
    root_name = game_lst[0][0][0]
    for branch, result  in zip([x for x,_ in game_lst],[x[1] for x in game_lst]):
        parent_node = game_tree
        assert branch[0] == parent_node.name
        for cur_node_name in branch[1:]:
            cur_node = next(
                (node for node in parent_node.children if node.name == cur_node_name),
                None,
            )
           
            
            if cur_node is None:
                cur_node = Node(cur_node_name, parent=parent_node,nb_visit=0,nb_win=0)
                
            parent_node = cur_node
            
        #backpropagation    
        for i in list(cur_node.iter_path_reverse()):
            i.nb_win=i.nb_win+result 
            i.nb_visit=i.nb_visit+1 
        
    return game_tree


def expantion(game_tree,state,available_play):
    node_val={}
    for i in available_play:
        state_tmp=state.copy()
        path=search.findall_by_attr(game_tree ,i)
        state_tmp.append(i)
        
        if path==():
            node_val[i]={"parent":{"nb_win":0,"nb_visit":0},"children":{"nb_win":0,"nb_visit":0}}
             
            
        else:
            for z in range(len(path)):
                
                if [node.name for node in path[z].path]==state_tmp:
                
                    node_val[i]={"parent":{"nb_win":0,"nb_visit":0},"children":{"nb_win":0,"nb_visit":0}}
                    node_val[i]["parent"]={"nb_win":path[z].parent.nb_win,"nb_visit":path[z].parent.nb_visit}
                    node_val[i]["children"]={"nb_win":path[z].nb_win,"nb_visit":path[z].nb_visit}
                    
                
                    

                elif i not in node_val:

                    node_val[i]={"parent":{"nb_win":0,"nb_visit":0},"children":{"nb_win":0,"nb_visit":0}}
                    
    return  node_val

                                 
def UCB1(val):
    ucb1={}
    for i in val.keys():
        if val[i]["children"]["nb_visit"]==0:
            ucb1[i]=np.inf
        else :
            val_ucb1=val[i]["children"]["nb_win"]/val[i]["children"]["nb_visit"]+np.sqrt(2)*np.sqrt(np.log(val[i]["parent"]["nb_visit"])/val[i]["children"]["nb_visit"])
            ucb1[i]=val_ucb1
    return ucb1    


                                    
                                    #######################################################
                                    #                  Simulation                         #
                                    #######################################################



player_1_Win=[]
matrix=np.zeros((6, 7)).astype(int) 
game_tree = Node("root", nb_visit=0,nb_win=0)


nb_iter=10

for k in tqdm(range(nb_iter)):    
    matrix_tmp=np.zeros((6, 7)).astype(int) 
    state=["root"]
    
    while(True):
        
        if win(matrix_tmp) is not None:
            player_1_Win.append(win(matrix_tmp))
            break
            
        if available_play(matrix_tmp) is None:
            break
          
        val_exploration=expantion(game_tree,state,available_play(matrix_tmp))
        result_ucb=UCB1(val_exploration)
        max_value = max(result_ucb.values())
        place_max_val=[k for k,v in result_ucb.items() if v == max_value]
        
        for pmv in place_max_val:
            
            state_to_explore=state.copy()
            matrix_exploration=matrix_tmp.copy()
            p1=play(player_turn(matrix_exploration),pmv[1],matrix_exploration)
            
            state_to_explore.append(pmv)
            g=[]
            while(True):
                           
                place_game=random.choice(available_play(matrix_exploration))
                
                if player_turn(matrix_exploration)==1:
                    state_to_explore.append(place_game)
                
                p2=play(player_turn(matrix_exploration),place_game[1],matrix_exploration)
                           
                if win(matrix_exploration)==1: 
                        g.append((state_to_explore,1))
                        break
                    
                if win(matrix_exploration)==2: 
                        g.append((state_to_explore,0))
                        break 
                    
                if available_play(matrix_exploration) is None:
                        g.append((state_to_explore,0))
                        break
                       
        game_tree = update_tree(g,game_tree)
        
        valeurs=expantion(game_tree,state,available_play(matrix_tmp))
        result_ucb=UCB1(valeurs)

        key_max_result_sim=max(result_ucb, key=result_ucb.get) 
        state.append(key_max_result_sim)
        p4=play(1,key_max_result_sim[1],matrix_tmp)  
        p2=play(2,player2_strategie_game(matrix_tmp,key_max_result_sim),matrix_tmp)
    if k%100==0:
        print(player_1_Win[k-100:k].count(1))    

 
#print tree
        
for pre, fill, node in RenderTree(game_tree):
    print(f"{pre}{node.name} {node.nb_win}/{node.nb_visit}") 
    
    
