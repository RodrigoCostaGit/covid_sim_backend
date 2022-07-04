#todo:
#usar a base de dados com dados diarios
#total population
#susceptible(not infected)
#infected(use data from last 7 days)
#imunes =confirmados+obitos
# r0, i think there is a database for that too

class model:
    def __init__(self,population,susceptible,infected,imune) -> None:
        self.population = population
        self.susceptible = susceptible
        self.infected = infected
        self.imune = imune

    def run(self):
        
