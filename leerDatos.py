#Aqui leer los datos del csv y se parametrizaran de forma correcta
import pandas as pd
import numpy as np
from clases_base import Parse
from dataset import Dataset

#TO DO: cambiar el nombre de esta clase para poder hacer escalable el ecosistema sin problemas con los nombres
# Esta clase se la encargada de leer los datos de casos confirmados globales
class ParseCasosConfirmados(Parse):
    # El constructor por defecto se le pasa la ruta del archivo y carga todos los datos
    def __init__(self):
        self.df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
        self.ar = self.df.to_numpy()

    # Nos devolvera los valores del ejeX que en este caso seran los dias |
    # TO DO :si el fichero no tubiese cabezeras o elementos necesarios para el ejex se mandara un array de numeros por defecto que coincidiran con la cantidad de columnas o datos
    def ejeX(self):
        cabeceras = self.df.columns.values
        # es desde la 4 porque las primeras son datos que no necesitamos y en la columna 4 empiezan las fechas
        return cabeceras[4:cabeceras.size]


    # Hay que modificarlo, devolvera una matriz que seera un array de arrays y en cada fila esta una fila del data set pero solo con las columnas que nos interesan
    def ejeY(self):
        filas = []
        x,y = self.df.shape # el shape nos devuelve la cantidad de filas y columnas , si no lo hiciese asi me meteria en la misma variable las dos (x,y)
        for i in range(x):
            filas.append(self.getRow(i))
        return filas


    def getRow(self,index):
        columnas = self.df.columns
        return self.df.loc[index , columnas[4]:columnas[len(columnas)-1]].to_numpy()

    # Devuelve un array con todos los paises ( segunda columna) para poder consultar en que filas esta un pais en concreto
    def getPaises(self):
        return self.df.loc[:,'Country/Region'].to_numpy()

    # Devuelve un array con todos los paises ( segunda columna) para poder llenar la dropdownList
    def getOpciones(self):
        return np.unique(self.df.loc[:,'Country/Region'].to_numpy())

    # Este metodo nos dira en que filas esta el pais que estamos buscando,si son varios devolvera varios indices por eso devuelve un array
    # df: Dataframe que contiene los datos en donde buscar el pais
    # pais: String que contiene el pais que queremos buscar en que posiciones se encuentra
    def index(self,df,pais):
        posicion = []
        for index, row in df.iterrows():
            if(row[1] == pais):
                posicion.append(index)
        return posicion




    def getDataset(self):
        # Dentro de cada parse se configurara el titulo
        data = Dataset("Casos Confirmados")
        data.setEjeX(self.ejeX())
        data.setEjeY(self.ejeY())
        data.setTodasLasOpciones(self.getPaises())  #Todas las opciones mantiene los duplicados por si hay mas de una linea con la misma opcion (pais)
        data.setOpciones(self.getOpciones())
        return data


class ParseAccidentesTrafico:

    def __init__(self): # Creo que compensa mas tener la ruta aqui dentro
        self.df = open('data/muertos_en_accidentes_de_trafico.csv')
        #self.ar = self.df.to_numpy()
        self.matriz = []
        for linea in self.df:
            array = linea.split(';')
            if (array[0] == ""):# al final del fichero hay una lineas con datos irrelevantes para lo que necesito de esta forma puedo
                break
            if (array[1] == '"Periodo"'):# Para saltarse la primera linea
                continue
            #print(array[2])
            array[2] = array[2].replace('\n','')# para eliminar el salto de linea que tiene cada linea
            array[2] = array[2].replace('\xad','') # para limpiar la cabecera
            for i in array: # para quitar las comillas que se generan al leer el fichero
                i = i.replace('"','')
            array[2] = int(array[2])
            self.matriz.append(array)

    def getDataset(self):

        data = Dataset("Accidentes traficos")
        data.setEjeX(self.ejeX())
        data.setEjeY(self.ejeY())
        data.setTodasLasOpciones(self.getOpciones())    # Como se que no va a haber duplicados en las filas uso el metodo de getOpciones
        data.setOpciones(self.getOpciones())

        return data

     # Meses
    def ejeX(self):
        meses = []
        maximo = 0 # Se que solo son doce anios asique para que no se mire todo el df innecesariamente, si ha guardado 12 elementos que salte
        #for index, row in df.iterrows():
        for linea in self.matriz:
            print(linea[0])
            if(linea[0] == '"2011"'):  # si coincide el anio con el de la fila guardo el elemento | Tengo que cambiar la conficion
                meses.append(linea[1]) # El elemento que se guardara es la cantidad de accidentes que corresponde a la tercera fila
                maximo += 1
                if (maximo == 12):
                    break

        return meses
        #return np.unique(self.df.loc[:,'Periodo'].to_numpy())


    # Matriz que cada fila representa victimas, PASARLO A NUMEROS
    def ejeY(self):
        matriz = []
        opciones = self.getOpciones()   # Las opciones son los distintos años y cada fila son los datos de cada anio
        for anio in opciones:
            matriz.append(self.getRow(anio))

        return matriz

    #Le pasamos un año y nos devuelve una fila con todos los elementos correspondiente a ese anio
    def getRow(self, anio):
        #
        fila = []
        maximo = 0 # Se que solo son doce anios asique para que no se mire todo el df innecesariamente, si ha guardado 12 elementos que salte
        #for index, row in df.iterrows():
        for linea in self.matriz:
            if(linea[0] == anio):  # si coincide el anio con el de la fila guardo el elemento
                fila.append(int(linea[2])) # El elemento que se guardara es la cantidad de accidentes que corresponde a la tercera fila
                maximo += 1
                if (maximo == 12):
                    break

        return fila



    # Las opciones seran los distintos años
    def getOpciones(self):
        #return np.unique(self.df.loc[:,'AÃ±o'].to_numpy())
        opciones = set()# las opcines seran los años
        for l in self.matriz:
            opciones.add(l[0])

        return sorted(opciones) # Esto es para que las opciones salgan ordenadas



#adfasf
