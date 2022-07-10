#todo:
#usar a base de dados com dados diarios
#total population
#susceptible população total tuga - infected - recovered (some website with current tuga pop)
#infected(use data from last 7 days) (daily)
#rercovered =confirmados+obitos - infected (daily)
# r0, i think there is a database for that too
#beta = rt
#gamma = 1/14

from scipy.integrate import odeint
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




def diferencial_equation(a,time,beta,gamma,total_population):
    s = a[0]
    i = a[1]
    r = a[2]
    return[
        -beta/total_population * s * i,
        beta/total_population * s * i -gamma * i,
        gamma * i
        
    ]

# solution = odeint(diferencial_equation,y0 =[s,i,r],t =time,args = (beta,gamma,total_population))

# S = solution.T[0]
# I = solution.T[1]
# R = solution.T[2]

# plt.plot(time,S)
# plt.plot(time,I)
# plt.plot(time,R)
# plt.show()

# print(solution)

def pred_run():
    #daily data covid, (data,confirmados, confirmados_novos,obitos, obitos_novos)
    url = "https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/dados_diarios.csv"
    df = pd.read_csv(url)

    #daily rt data covid
    url2 = "https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/rt.csv"
    df2 = pd.read_csv(url2)

    #fonte https://www.pordata.pt/Portugal/Popula%C3%A7%C3%A3o
    total_population = 10344802
    i = df.tail(14)
    i = i["confirmados_novos"].sum()
    r = int(df["confirmados"].tail(1) + df["obitos"].tail(1) -i)
    s = int(total_population - i - r)
    beta = float(df2["rt_nacional"].tail(1))*(1/14)
    gamma = 1/14 #10= dias em media para recuperar de covid
    time = np.arange(0,60,1)
    solution = odeint(diferencial_equation,y0 =[s,i,r],t =time,args = (beta,gamma,total_population))
    # solution = odeint(diferencial_equation,y0 =[s,i,r],t =time,args = (gamma,beta,total_population))


    # S = solution.T[0]
    # I = solution.T[1]
    # R = solution.T[2]

    # plt.plot(time,S)
    # plt.plot(time,I)
    # plt.plot(time,R)
    # plt.show()
    # print(s)
    # print(i)
    # print(r)
    # print(beta)
    # print(gamma)


    return solution


pred_run()


