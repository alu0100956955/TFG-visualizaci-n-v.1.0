#Aqui leer los datos del csv y se parametrizaran de forma correcta
import pandas as pd
import numpy as np

#df = pd.read_csv('data/casos_2019.csv')

#print(df.head(0))
#print("Cantidad de columnas: ")
#print(df.shape)

class Lector:
    # El constructor por defecto se le pasa la ruta del archivo y carga todos los datos
    def __init__(self,ruta):
        self.df = pd.read_csv(ruta)
        self.ar = self.df.to_numpy()

    # Nos devolvera los valores del ejeX que en este caso seran los dias |
    # si el fichero no tubiese cabezeras o elementos necesarios para el ejex se mandara un array de numeros por defecto que coincidiran con la cantidad de columnas o datos de y
    # tengo problemas para sacar la cabezera asique lo paraemetrizo para sacar una fila en concreto
    def ejeX(self):
        cabeceras = self.df.columns.values
        # es desde la 4 porque las primeras son datos que no necesitamos
        return cabeceras[4:cabeceras.size]
        #return self.df.loc[0, '1/22/20':'3/17/20']
        #return self.ar[0][4:59]  # no puedo usar esto ya que al pasarlo a numpy la primera fila la elimina
        #return self.df.loc[x, '1/22/20':'3/17/20'].to_numpy()  # lo convierto en numpy para trabajar mas facil con los datos

    def ejeY(self,y):
        return self.df.loc[y, '1/22/20':'3/17/20'].to_numpy()

    # esta funcion es para tener el rango de valores de x, ya que vamos a tener un MONTON  de dias es mejor que no esten todos los dias en el ejex
    def rango(self):
        return np.arange(0,self.ejeX().size,3).tolist()

    # Devuelve un array de valores que seran la leyenda del ejeX segun el rango de valores previo
    # valores = el array tipo numpy que se crea con el ejeY() o con el ejeX() pero de esta forma se pasaran los valores correctos y no me tengo que preocupar de eso aqui
    def labelsX(self,valores):
        array = np.array([]) # el array auxiliar que sera el que contendra las etiquetas para el eje x
        for i in self.rango():
            if(i<valores.size): # para evitar el overflow
                aux = np.append(array,valores[i])
            array = aux # para seguir añadiendo valores
        return array

    # para obtener directamente el dataframe
    def getdf(self):
        return self.df



#l = Lector('data/casos_2019.csv')
#print(l.ejeX())

#print(type(a))


#adfasf
