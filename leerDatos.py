#Aqui leer los datos del csv y se parametrizaran de forma correcta
import pandas as pd
import numpy as np
from clases_base import Parse
from dataset import Dataset
#df = pd.read_csv('data/casos_2019.csv')



rutaGit = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
rutaGit2 = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
#TO DO: cambiar el nombre de esta clase para poder hacer escalable el ecosistema sin problemas con los nombres
# Esta clase se la encargada de leer los datos de casos confirmados globales
class ParseCasosConfirmados(Parse):
    # El constructor por defecto se le pasa la ruta del archivo y carga todos los datos
    def __init__(self,ruta):
        self.df = pd.read_csv(ruta)
        self.ar = self.df.to_numpy()

    # Nos devolvera los valores del ejeX que en este caso seran los dias |
    # TO DO :si el fichero no tubiese cabezeras o elementos necesarios para el ejex se mandara un array de numeros por defecto que coincidiran con la cantidad de columnas o datos
    # este NO hay que modificarlo para pasarselo al dataset
    def ejeX(self):
        cabeceras = self.df.columns.values
        # es desde la 4 porque las primeras son datos que no necesitamos y en la columna 4 empiezan las fechas
        return cabeceras[4:cabeceras.size]


    # Hay que modificarlo, devolvera una matriz que seera un array de arrays y en cada fila esta una fila del data set pero solo con las columnas que nos interesan
    def ejeY(self):
        #columnas = self.df.columns
        #return self.getRows(columnas,self.index(self.df,pais))
        filas = []
        #rango = self.ar.size -1
        x,y = self.df.shape # el shape nos devuelve la cantidad de filas y columnas , si no lo hiciese asi me meteria en la misma variable las dos (x,y)
        #print(x)
        for i in range(x):
            #print(i)
            filas.append(self.getRow(i))
        return filas


    def getRow(self,index):
        columnas = self.df.columns
        return self.df.loc[index , columnas[4]:columnas[len(columnas)-1]].to_numpy()

    # Devuelve un array con todos los paises ( segunda columna) para poder consultar en que filas esta un pais en concreto
    def getPaises(self):
        return self.df.loc[:,'Country/Region'].to_numpy()

    # Este metodo nos dira en que filas esta el pais que estamos buscando,si son varios devolvera varios indices por eso devuelve un array
    # df: Dataframe que contiene los datos en donde buscar el pais
    # pais: String que contiene el pais que queremos buscar en que posiciones se encuentra
    def index(self,df,pais):
        posicion = []
        for index, row in df.iterrows():
            if(row[1] == pais):
                posicion.append(index)
        return posicion

# METODOS ANTIGUOS
    # le pasamos las posiciones en el dataframe y aqui suma todas las filas para obtener una unica fila del pais que se escogio, esto es porque algunos pais aparecen varias veces difenciados por regiones solo
    # columnas: Array que contiene las cabeceras de las columnas, necesario para la eleccion de las columnas correctas para cada fila
    # posicion: array que contiene las posiciones de las filas en el dataframe que indican el pais que queremos representas
    #
    def getRows(self,columnas,posicion):
        primera = True
        for i in posicion:
            if(primera):
                primera = False
                rows = self.df.loc[i , columnas[4]:columnas[len(columnas)-1]].to_numpy()
                continue
            rows += self.df.loc[i , columnas[4]:columnas[len(columnas)-1]].to_numpy()
        return rows


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

    def getDataset(self):
        # Dentro de cada parse se configurara el titulo
        data = Dataset("casos Confirmados")
        #data.setTitle(data,"Casos confirmados")
        data.setEjeX(self.ejeX())
        data.setEjeY(self.ejeY())
        data.setPaises(self.getPaises())
        return data


def ParseGit(rutaGit):

    def __init__(self,rutaGit):
        self.df = pd.read_csv(rutaGit)
        self.ar = self.df.to_numpy()
    def ejeX():
        print("Sin acabar")

    def ejeY():
        print("sin acabar")




#l = Lector('data/casos_2019.csv')
#print(l.ejeX())
#print(l.getdf().columns)

#print(type(a))


#adfasf
