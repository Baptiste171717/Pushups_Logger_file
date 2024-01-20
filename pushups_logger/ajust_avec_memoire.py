import sys
sys.path.append('C:/Users/titou/OneDrive/Escritorio/cour_info_2A/TDLOG')
from fonct2_avec_memoire import p_opt
import pandas as pd
import numpy as np
#%%
DataBase=pd.read_csv('C:/Users/titou/OneDrive/Escritorio/cour_info_2A/TDLOG/TDLOG_ exercices - Feuille 1.csv',
                 index_col=0,
                 parse_dates=True)
Rep=np.array(DataBase['Reps'])
DataBase=DataBase.drop('Reps',axis=1)
T_max1=60*120
T_repos1=60
Rep[:48]=(2*T_repos1+45)*Rep[:48]
Rep[48:]=60*1.25*Rep[48:]
#Le temps pour faire chaque exos en secondes est Rep
Exo=DataBase.values #la database des exos
Exo=np.array(Exo)
Exo = np.column_stack([Exo, np.zeros(Exo.shape[0])] ) #composante mémoire afin de pas trop se répeter
#%%
e=0
for i in range(0,5):
    Exo[i][-1]=e
for i in range(5,10):
    Exo[i][-1]=e
for i in range(10,15):
    Exo[i][-1]=e
print(Exo)
#%%
def error(poid,obj,T_max,Reps,Exos):
    Xa=np.dot(poid,Exos)
    #on ajuste pour enelever le terme mémoire
    Xa=Xa[:len(Xa)-1]
    obj=obj[:len(obj)-1] 
    dist=np.linalg.norm(Xa/np.linalg.norm(Xa) - obj)
    return([ dist, abs(np.dot(poid,Reps)-T_max)/60, sum(poid[0:15])])
   # print(np.round(np.dot(poid,Exos)))
obj1=[1,0,1,0,0,0,0,0,1,0,0,0]
obj1.append(0) #composante mémoire afin de pas trop se répeter
poids=p_opt(obj1,T_max1,Rep,Exo)
print(error(poids,obj1,T_max1,Rep,Exo))
#%%
import matplotlib.pyplot as plt
log_scale = np.logspace(np.log10(0.01), np.log10(10), 30)
for i in range (0,5):
  print(i)
  obj_i=np.random.randint(2, size=13)
  obj_i[-1]=0
  L=[]
  for k in log_scale:
    for i in range(0,5):
        Exo[i][-1]=k
    for i in range(5,10):
        Exo[i][-1]=2*k
    for i in range(10,15):
        Exo[i][-1]=3*k
    poids=p_opt(obj_i,T_max1,Rep,Exo)
    L.append(error(poids,obj_i,T_max1,Rep,Exo))
  L=np.array(L)
  fig, axs = plt.subplots(3, 1, figsize=(12, 6))
  axs[0].plot(log_scale, L[0:, 0])
  axs[0].axvline(1,color='r')
  axs[1].plot(log_scale, L[0:, 1])
  axs[1].axvline(1,color='r')
  axs[2].plot(log_scale, L[0:, 2])
  axs[2].axvline(1,color='r')
  axs[0].set_title("Distance")
  axs[1].set_title("Temps")
  axs[2].set_title("Memoire")
  fig.suptitle("Test set 3")
  
# e=1 semble optimal: on ne veut pas forcer l'exclusion des exercices si ils sont nécessaires






