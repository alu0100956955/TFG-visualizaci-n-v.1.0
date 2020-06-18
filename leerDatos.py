#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Aqui leer los datos del csv y se parametrizaran de forma correcta
import pandas as pd
import numpy as np
from clases_base import Parse
from dataset import Dataset
import datetime

#TO DO: cambiar el nombre de esta clase para poder hacer escalable el ecosistema sin problemas con los nombres
# Esta clase se la encargada de leer los datos de casos confirmados globales
class ParseCasosConfirmados(Parse):
    # El constructor por defecto se le pasa la ruta del archivo y carga todos los datos
    def __init__(self):
        self.df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
        self.ar = self.df.to_numpy()

    # Nos devolvera los valores del ejeX que en este caso seran los dias |
    # TO DO :si el fichero no tubiese cabezeras o elementos necesarios para el ejex se mandara un array de numeros por defecto que coincidiran con la cantidad de columnas o datos
    # Este es ahora el metodo que extrae el array de dias necesario para una de las opciones de eje
    def ejeX(self):
        cabeceras = self.df.columns.values
        # es desde la 4 porque las primeras son datos que no necesitamos y en la columna 4 empiezan las fechas
        return cabeceras[4:cabeceras.size]


    # CAMBIAR: este tiene que ser un metodo que me devuelva la matriz con todos los paises ( un pais por fila) representando la cantidad de contagios y no sera garantizado el ejeY
    def ejeY(self):
        filas = []
        x,y = self.df.shape # el shape nos devuelve la cantidad de filas y columnas , si no lo hiciese asi me meteria en la misma variable las dos (x,y)
        for i in range(x):
            filas.append(self.getRow(i))
        return filas

    # Nos devuelve en tipo array la fila del indice que le indiquemos
    def getRow(self,index):
        #print(index)
        columnas = self.df.columns
        return self.df.loc[index , columnas[4]:columnas[len(columnas)-1]].to_numpy()

    # Devuelve un array con todos los paises ( segunda columna) para poder consultar en que filas esta un pais en concreto
    def getPaises(self):
        return self.df.loc[:,'Country/Region'].to_numpy()

    # Devuelve un array con todos los paises ( segunda columna) que seran las opciones para poder representar
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
        #data.setEjeX(self.ejeX())
        #data.setEjeY(self.ejeY())
        #data.setEjeY(self.getMatrizCasosConfirmados())
        data.setTodasLasOpciones(self.getPaises())  #Todas las opciones mantiene los duplicados por si hay mas de una linea con la misma opcion (pais)
        

        #Modificacion del parse
        data.addOpcionEje("Dias")
        data.addOpcionEje("Cantidad de contagios")
        data.addOpcionEje("% de contagios")
        #data.addElementoEje(self.espaciar())
        data.addElementoEje(self.ejeX())
        data.addElementoEje(self.getMatrizCasosConfirmados())
        data.addElementoEje(self.porcentajesDeContagios())

        paises = self.getOpciones()
        #print(type(paises))
        #Diccionario con los paises que debo cambiar el nombre
        diccionario = {"US":"United States of America"}
        # Para que coincida con los nombres del fichero Json para los mapas le aplico el diccionario sobre el conjunto original
        paisesFinales = [diccionario.get(n,n) for n in paises]
        #print(type(paisesFinales))
        data.setOpciones(paisesFinales)
        data.setTiposGraficas(["1:  Linea Terminal", "2: Linea html", "3: Linea navegador", "4: Barras navegador", "5: mapa navegador", "6: dispersion navegador", "7: box navegador","8: Box navegador" , "9: Histograma terminal"])
        return data


#--------------------------------------Actualizacion-------------------------------------
    # Le pasamos un pais que sera la opcion y nos dice en cuantas filas se encuentra
    def indicesPais(self, opcion):
        posicion = []   # Lo hago array por si hay mas de una opcion
        paises = self.getPaises()
        for index in range(len(paises)):
            if(paises[index] == opcion):
                posicion.append(index)
        return posicion 

    # Le pasamos las posiciones del pais, busca las filas corresponcientes, las suma y nos devuelve el array resultado, si no encuentra nada devuelve el array con un cero
    def searchRow(self,posiciones):
        primera = True
        rows = [0]
        #print(posiciones)
        for i in posiciones:
            if(primera):
                primera = False
                rows = self.getRow(i)   # ERROR AQUI
                continue
            rows += self.getRow(i)
        return rows

    def getMatrizCasosConfirmados(self):
        opciones = self.getOpciones()
        #print(opciones)
        matriz = []
        for opcion in opciones:
            #print(opcion)
            matriz.append(self.searchRow(self.indicesPais(opcion)))
        return matriz

    # Nos devuelve la matriz pero con el porcentaje con respecto al global de contagios
    def porcentajesDeContagios(self):
        contagiosTotales = []   # Contendra la cantidad de contagios totales por dia
        # En la columna 4 comienzan los dias, hasta el maximo de columnas
        for i in range(4,self.df.columns.size):
            contagiosTotales.append(self.cantidadContagios(i))


        opciones = self.getOpciones()
        matriz = []
        for opcion in opciones:
            matriz.append(self.getRowPorcentaje(self.indicesPais(opcion),contagiosTotales))
        return matriz

    # Le pasamos un dia en concreto y nos devuelve la cantidad de contagios que han ocurrido ese dia ( el dia sera la posicion en el array)
    def cantidadContagios(self,dia):
        aux = 0
        for i in self.ar:
            aux += i[dia]
        return aux

    # Nos devuele la fila del pais que le pasemos (posiciones) y acada valor representa el porcentaje de contagios con respecto al total global de contagios
    def getRowPorcentaje(self,posiciones,contagios):
        primera = True
        row = [0]
        for i in posiciones:
            if(primera):
                primera = False
                row = self.getRow(i)
                continue
            row += self.getRow(i)

        # Aqui calculo el porcentaje
        for i in range(0,row.size):
            row[i] = row[i]/contagios[i] * 100
        return row

    # Metodo para covnertir en espacios los dias que no quiero que se muestren
    def espaciar(self):
        cabeceras = self.df.columns.values
        # es desde la 4 porque las primeras son datos que no necesitamos y en la columna 4 empiezan las fechas
        dias = cabeceras[4:cabeceras.size]

        tam = len(dias)
        z = tam/7   # Este es para la cantidad de ticks, como quiero que solo salgan 7 etiquetas pos el modulo sera con el numero que salga como resultado
        for i in np.arange(0,tam):
            if(i%int(z) != 0):
                # añadir espcios
                dias[i] = ""
        # devolver el array con las fechas sobreescritas
        return dias

    def getDias(self):
        cabeceras = self.df.columns.values
        # es desde la 4 porque las primeras son datos que no necesitamos y en la columna 4 empiezan las fechas
        dias = cabeceras[4:cabeceras.size]
        diasFormateado = []
        for i in dias:
            diasFormateado.append(datetime.strptime(i,'%m/%d/%y'))
        return diasFormateado
        

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Parse para los accidentes de trafico
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
            for i in range(len(array)): # para quitar las comillas que se generan al leer el fichero
                array[i] = array[i].replace('"','')

            #print(array)
            array[2] = int(array[2])
            
            self.matriz.append(array)

    def getDataset(self):

        data = Dataset("Accidentes traficos")
        #data.setEjeX(self.ejeX())
        #data.setEjeY(self.ejeY())
        #data.setTodasLasOpciones(self.getOpciones())    # Como se que no va a haber duplicados en las filas uso el metodo de getOpciones
        data.setOpciones(self.getOpciones())

        data.addOpcionEje("Meses")
        data.addOpcionEje("Cantidad de Accidentes")
        #data.addOpcionEje("% de contagios")
        data.addElementoEje(self.meses())
        data.addElementoEje(self.victimas())
        data.setTiposGraficas(["1:  Linea Terminal", "3: Linea navegador", "4: Barras navegador", "6: dispersion navegador", "7: box terminal","8: Box navegador"])
        return data

     # Meses
    def meses(self):
        meses = []
        maximo = 0 # Se que solo son doce anios asique para que no se mire todo el df innecesariamente, si ha guardado 12 elementos que salte
        #for index, row in df.iterrows():
        # REVISAR
        for linea in self.matriz:
            #print(linea[0])
            if(linea[0] == '2010'):  # si coincide el anio con el de la fila guardo el elemento | Tengo que cambiar la conficion
                meses.append(linea[1]) # El elemento que se guardara es la cantidad de accidentes que corresponde a la tercera fila
                maximo += 1
                if (maximo == 12):
                    break

        return meses
        #return np.unique(self.df.loc[:,'Periodo'].to_numpy())


    # Matriz que cada fila representa victimas, PASARLO A NUMEROS
    def victimas(self):
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

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class ParseParoEspaña:

    def __init__(self):
        # Abrir la fuente de datos
        # guardarlo en la variables para poder tabajar mas adelante
        self.df = pd.read_csv('https://raw.githubusercontent.com/LuisSevillano/historical-evolution-of-the-unemployment-rate-in-spain/master/docs/data/historico.csv')
        

    def getDataset(self):
        data = Dataset("Paro en españa")
        #data.setEjeX(self.ejeX())
        #data.setEjeY(self.ejeY())
        #data.setTodasLasOpciones(self.getOpciones())    # Como se que no va a haber duplicados en las filas uso el metodo de getOpciones
        data.setOpciones(self.getOpciones())

        data.addOpcionEje("Años")
        data.addOpcionEje("Cantidad de Accidentes")
        data.addOpcionEje("% de Paro")
        data.addElementoEje(self.getAnios())
        data.addElementoEje(self.cantidadParo())
        data.addElementoEje(self.porcentajeParo())
        data.setTiposGraficas(["1:  Linea Terminal", "2: Linea html", "3: Linea navegador", "4: Barras navegador", "6: dispersion navegador", "7: box terminal","8: Box navegador", "9: Histograma Terminal"])

        return data

    # Los paises seran las opciones basicas de representación
    def getOpciones(self):
        return np.unique(self.df.loc[:,'state'].to_numpy()).tolist()

    # metodo que devuelve en una lista todos los anios
    def getAnios(self):
        # Cuidado que cada anio esta dividido en dos temporadas y 
        cabeceras = self.df.columns.values
        # es desde la 2 porque las primeras son datos que no necesitamos 
        anios = []
        # Dabo que son string los paso a tipo datetime segun la temporada que sea
        for i in cabeceras[2:cabeceras.size]:
            anios.append(self.creacionFecha(i))
        #print(anios)
        return anios


    # Para obtener las distintas comunidades, que seran las opciones a representar
    def getComunidades():
        comunidades = []

        return comunidades

    # Devolvera una matriz que contendra el paro de cada comunidad, siendo cada fila una comunidad
    def cantidadParo(self):
        paro = []
        columnas = self.df.columns
        for index, row in self.df.iterrows():
            paro.append(self.df.loc[index , columnas[2]:columnas[len(columnas)-1]].to_numpy())
        return paro

    # Devolvera una matriz con el procentaje que representa los accidentes en ese anio (columna) para cada pais (fila)
    def porcentajeParo(self):
        porcentaje = []

        return porcentaje

    def getRow(self, index):
        columnas = self.df.columns
        return self.df.loc[index , columnas[2]:columnas[len(columnas)-1]].to_numpy()

    # Le paso el string de la columna para convertirlo en tipo datetime | Para que trabaje mejor las graficas a la hora de de hacer los ticks
    def creacionFecha(self, fecha):
        anio = int(fecha[0]+fecha[1]+fecha[2]+fecha[3])
        if(len(fecha)== 6):
            return datetime.datetime(anio,3,1)
        if(len(fecha) == 8):
            return datetime.datetime(anio,9,1)
        #Llegados a este punto solo quedan las temporadas TII & TIV, asi que miro la posicion 6 de los array de tamaño 7
        if(fecha[6] == "I"):
            return datetime.datetime(anio,6,1)
        else:
            return datetime.datetime(anio,12,1)



#adfasf
