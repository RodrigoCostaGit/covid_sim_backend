import pandas as pd

#weekly data of covid cases
url = "https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/data.csv"

#loads the csv to df
df = pd.read_csv(url)


df = df.iloc [:,3:10]
df = df[["confirmados_arsalentejo","confirmados_arsalgarve","confirmados_arslvt","confirmados_arscentro","confirmados_arsnorte","confirmados_madeira","confirmados_acores"]]
df2 = df.rename({"confirmados_arsalentejo":"Alentejo","confirmados_arsalgarve":"Algarve","confirmados_arslvt":"Área Metropolitana de Lisboa","confirmados_arscentro":"Centro (PT)","confirmados_arsnorte":"Norte","confirmados_madeira":"Região Autónoma da Madeira","confirmados_acores":"Região Autónoma dos Açores"}, axis=1)
df2 = df2.tail(1)
index = df2.head().index.values
index = index[0]
df2 = df2.rename(index={index:"info"})
df2 = df2.T
print(df2)

df2.to_csv("data_regions.csv")
