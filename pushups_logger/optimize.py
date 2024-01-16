
import scipy.optimize as sco
import pandas as pd
import copy
import numpy as np




# DataBase=pd.read_csv('TDLOG_exercises_2.csv',index_col=0)
DataBase=pd.read_sql_table('Workout_table','sqlite:///Workout_excel.sqlite3',index_col=0)


T_max1=60*120*2
T_repos1=60
# # 2 types de return: pour freq=1, 2 et 3 on a le mois. Sinon on a que la semaine
def remplace(L,i,j=None): #On fait les exercices i à j le jour de liste d'exo L
    if j is None:
        L[i]=1
    else:
        L[i:j+1]=[1]*(j-i+1)
def repartition_jours (freq,muscle,cardio):
    assert(muscle or cardio)
    assert(1<=freq<=7)
    alpha=[0]*12
    L=[0]*freq
    for i in range (0,freq):
        L[i]=copy.deepcopy(alpha)
    card=[0]*12
    card[0]=1
    
    if (cardio and  muscle==False):  #cas trivial où on ne fait que du cardio
        alpha=[0]*12 #la repartition journalière de nos poids
        alpha[0]=1
        L=[alpha]*freq*4
        return(L)
    if (freq ==1 or freq ==2):
        L=[0]*4
        for i in range (0,4):
            L[i]=copy.deepcopy(alpha)
        if cardio:
            remplace(L[0],0) #on fait cardio le premier jour
            remplace(L[1],3,6) #on fait dos et bras
            remplace(L[2],1,2) #on fait epaules...
            remplace(L[2],7,8) #abs et pec
            remplace(L[3],9,11) #jambes
            if freq != 1:
                L=L+L
        else:
            remplace(L[0],3,5) #on fait bras
            remplace(L[1],6,7) #dos et pec
            remplace(L[2],1,2) #epaules...
            remplace(L[2],8)   #et abdos
            remplace(L[3],9,11) # jambes
            if freq != 1:
                L=L+L

    if freq == 3:
        remplace(L[0],6,7) #pec et dos
        remplace(L[1],1,2) #epaules
        remplace(L[1],8)  # abdos
        remplace(L[1],3,5) #bras
        remplace(L[2],9,11) #jambes
        L=L*4 
        #on remplace une session par semaine par du cardio
        if cardio:
         for i in range (0,4):
             L[3*i+i%3]=card
    if freq == 4:
        remplace(L[0],3,5) #on fait bras
        remplace(L[1],6,7) #dos et pec
        remplace(L[2],1,2) #epaules...
        remplace(L[2],8)   #et abdos
        remplace(L[3],9,11) # jambes
        if cardio:
         L[0]=card
         remplace(L[2],3,5) #on ajoutte bras aux jour 3 avec epaules et abdos
    if freq == 5:
        remplace(L[0],3,5) #on fait bras
        remplace(L[1],6) #dos
        remplace(L[2],7) #pec
        remplace(L[3],1,2) #epaules...
        remplace(L[3],8)   #et abdos
        remplace(L[4],9,11) # jambes
        if cardio:
         L[1]=card
         remplace(L[2],6) #on ajoute pec au jour 3 et à pec
    if freq == 6:
       remplace(L[0],3,5) #on fait bras
       remplace(L[1],6) #dos
       remplace(L[2],7) #pec
       remplace(L[3],1,2) #epaules
       remplace(L[4],8)   #abdos
       remplace(L[5],9,11) # jambes
       if cardio:
           L[3]=card
           remplace(L[4],1,2) #on ajoute epaules au jour 5 et aux abods
    if freq == 7:
      remplace(L[0],3,5) #on fait bras
      remplace(L[1],6) #dos
      remplace(L[2],7) #pec
      remplace(L[3],1,2) #epaules
      remplace(L[4],8)   #abdos
      remplace(L[5],9,11) # jambes
      remplace(L[6],3,5) #on fait bras à novueau
      if cardio:
          L[0]=card
    return np.array(L)


names = np.array(DataBase['Exercise'])

def interpreter(p_exos):
    d=dict()
    for i in range(0, len(p_exos)):
        d[names[i]] = p_exos[i]
    return d


Rep=np.array(DataBase['Reps'])
DataBase=DataBase.drop('Reps',axis=1)
DataBase=DataBase.drop('Exercise',axis=1)
DataBase=DataBase.drop('Last_review',axis=1)
DataBase=DataBase.drop('id',axis=1)


Exos=DataBase.values

Rep[:48]=(2*T_repos1+45)*Rep[:48]
Rep[48:]=60*1.25*Rep[48:]
#Le temps pour faire chaque exos en secondes est Rep
Exo=DataBase.values #la database des exos
Exo=np.array(Exo)      
#%%
obj1=[0,0,0,0,0,0,1,1,1,0,0,0]

def p_opt(obj,T_max = T_max1, Reps = Rep, Exos =Exo): #notre fonction d'optimisation
 def g(p_exo):
     Xa=np.dot(p_exo,Exos)
     distance = np.linalg.norm(Xa/np.linalg.norm(Xa) - obj)  # Distance du vecteur normalisé
     return distance +0.01*abs(np.dot(p_exo,Reps)-T_max)

 #On veut minimize g avec les contraintes x,y>=0 et x**2>=y**2
 contraintes = (
     {'type': 'ineq', 'fun': lambda X: np.dot(X,Reps)-T_max*0.75},
     {'type': 'ineq', 'fun': lambda X: 1.15*T_max-np.dot(X,Reps)})  
 bornes=[(0, 3)] * len(Exo)
 minimum_info = sco.minimize(g, [1] * len(Exos), method='SLSQP',
                             bounds=bornes, constraints=contraintes) 
 p_exos=np.round(minimum_info['x'])
 return(p_exos)





def create_workout_session(day_repetition):
    workout_session = []
    for row in day_repetition:
        workout_session.append(p_opt(row))
    return np.array(workout_session)
        
        
def interpreter(p_exos):
    d=dict()
    for i in range(0, len(p_exos)):
        if p_exos[i] != 0:
            d[names[i]] = p_exos[i]
    return d
