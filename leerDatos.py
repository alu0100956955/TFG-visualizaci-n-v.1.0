#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Aqui leer los datos del csv y se parametrizaran de forma correcta
import pandas as pd
import numpy as np
from clases_base import Parse
from dataset import Dataset
import datetime
from datetime import datetime


tiposGraficas = ["1 :  Linea Terminal", "2 : Linea html", "3 : Linea navegador","4 : Barras navegador", "6 : dispersion navegador", "7 : box terminal",
                "9 : Histograma Terminal", "10: Histograma navegador","11: Clasificacion vecino", "12: Clasificacion Gausian", "13: Clasificacion Tree",
                "14: Regresion Linear","15: Regresion Gradient","16: Regresion Isotonic","17: Kmeans","18: Mixture","19: DBscan",
                "20: Todas las clasificaciones","21: Todas las regresion", "22: Todos los clustering","0 : Pruebas"]

class ParseTemplate:

    def __init__(self):
        self.df = pd.read_csv("data/")

    def getDataset(self):
        data = Dataset("")
        #data.setIntFuente()
        #data.setOpciones()

        #----------
        data.addOpcionEje("")

        #----------
        data.addElementoEje()


        data.setTiposGraficas(tiposGraficas) # Los tipos de graficas es una variable global
        return data



#TO DO: cambiar el nombre de esta clase para poder hacer escalable el ecosistema sin problemas con los nombres
# Esta clase se la encargada de leer los datos de casos confirmados globales
class ParseCasosConfirmados(Parse):
    # Mantener esta o cambiarlo por lo otro
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
        data.setIntFuente(1)

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
        #data.setTiposGraficas(["1:  Linea Terminal", "2: Linea html", "3: Linea navegador", "4: Barras navegador", "5: mapa navegador",
         #                     "6: dispersion navegador", "7: box terminal", "9: Histograma terminal","0: pruebas"])
        data.setTiposGraficas(tiposGraficas)
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
        data.setIntFuente(2)

        data.addOpcionEje("Meses")
        data.addOpcionEje("Cantidad de Accidentes")
        #data.addOpcionEje("% de contagios")
        data.addElementoEje(self.meses())
        data.addElementoEje(self.victimas())
        #data.setTiposGraficas(["1:  Linea Terminal", "3: Linea navegador", "4: Barras navegador",
        #                      "6: dispersion navegador", "7: box terminal", "9: Histograma Terminal", "0: Pruebas"]) # ,"8: Box navegador"  "5. Dispersion terminal"
        data.setTiposGraficas(tiposGraficas)
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

            # Sorted es para que las opciones salgan ordenadas
        return sorted(opciones) 

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
        data.setIntFuente(3)    # Para que dentro del dataset este el numero de la fuente de datos

        data.addOpcionEje("Años")
        data.addOpcionEje("Cantidad de parados")
        #data.addOpcionEje("% de Paro") #Lo tengo comentado porque aun no esta implementado
        data.addElementoEje(self.getAnios())
        data.addElementoEje(self.cantidadParo())
        data.addElementoEje(self.porcentajeParo())
        #data.setTiposGraficas(["1:  Linea Terminal", "2: Linea html", "3: Linea navegador", "4: Barras navegador", 
        #                      "6: dispersion navegador", "7: box terminal", "9: Histograma Terminal", "0: Pruebas"]) # "5. Dispersion terminal"
        data.setTiposGraficas(tiposGraficas)
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
            return datetime(anio,3,1)
        if(len(fecha) == 8):
            return datetime(anio,9,1)
        #Llegados a este punto solo quedan las temporadas TII & TIV, asi que miro la posicion 6 de los array de tamaño 7
        if(fecha[6] == "I"):
            return datetime(anio,6,1)
        else:
            return datetime(anio,12,1)


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Problema: los datos avanza de forma diaria
class ParseCovid:
    
    def __init__(self):
        #print("En proceso")
        #ruta = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
        self.df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv")

    # total_cases, new_cases, new_deaths, total_test, new_test
    def getDataset(self):
        data = Dataset("Covid")
        paises = self.getPaises()
        data.setOpciones(paises)    #las opciones son los paises
        data.setIntFuente(4)

        data.addOpcionEje("Dias")
        data.addOpcionEje("Cantidad total de contagios")
        data.addOpcionEje("Cantidad diaria de contagios")
        data.addOpcionEje("Cantidad diaria de fallecidos")
        #data.addOpcionEje("% de Paro") #Lo tengo comentado porque aun no esta implementado
        data.addElementoEje(self.getDias())
        #data.addElementoEje(self.getMatriz(paises,'total_cases'))
        #data.addElementoEje(self.getMatriz(paises,'new_cases'))
        #data.addElementoEje(self.getMatriz(paises,'new_deaths'))
        total, nuevos_casos, nuevas_muertes = self.getMatrices(paises)
        data.addElementoEje(total)
        data.addElementoEje(nuevos_casos)
        data.addElementoEje(nuevas_muertes)

        #data.setTiposGraficas(["1:  Linea Terminal", "2: Linea html", "3: Linea navegador", "4: Barras navegador", 
        #                      "6: dispersion navegador", "7: box terminal", "9: Histograma Terminal", "0: Pruebas"]) # "5. Dispersion terminal"
        data.setTiposGraficas(tiposGraficas)
        return data


    def getPaises(self):
        return np.unique(self.df.loc[:,'location'].to_numpy()).tolist()

    def getDias(self):
        dias = np.unique(self.df.loc[:,'date'])
        diasFormateado = []
        for i in dias:
            diasFormateado.append(datetime.strptime(i,'%Y-%m-%d'))
            #diasMat = matplotlib.dates.date2num(diasFormateado)
            

        return diasFormateado

    def getMatriz(self, paises,parametro):
        fila = []
        matriz = []
        i = 0
        for index, row in self.df.iterrows():
            if(i == 212): break # Para evitar salirme de rango
            if(paises[i] != row['location']):
                i += 1
                matriz.append(fila)#guardo la fila porque hemos pasado aun nuevo pais
                fila = []# limpio el contenido de la fila
            if(row[parametro] is None or row[parametro] < 0):
                fila.append(0)  # meter un cero o dejarlo vacio ?
            else:
                fila.append(row[parametro])
        return matriz

    def getMatrices(self, paises):
        fila_totales = []
        fila_casos_nuevos = []
        fila_muertes_nuevas = []
        casos_totales = []
        nuevos_casos = []
        nuevas_muertes = []
        i = 0
        for index, row in self.df.iterrows():
            if(i == 212): break # Para evitar salirme de rango
            if(paises[i] != row['location']):
                i += 1
                casos_totales.append(fila_totales)#guardo la fila porque hemos pasado aun nuevo pais
                nuevos_casos.append(fila_casos_nuevos)
                nuevas_muertes.append(fila_muertes_nuevas)


                #Reseteo el contenido de las filas
                fila_totales = []
                fila_casos_nuevos = []
                fila_muertes_nuevas = []

            # Añadir datos de los casos totales de contagios
            if(row['total_cases'] is None or row['total_cases'] < 0):
                fila_totales.append(0)  # meter un cero o dejarlo vacio ?
            else:
                fila_totales.append(row['total_cases'])
            
            # Añadir datos de los casos nuevos diarios de contagios
            if(row['new_cases'] is None or row['new_cases'] < 0):
                fila_casos_nuevos.append(0)  # meter un cero o dejarlo vacio ?
            else:
                fila_casos_nuevos.append(row['new_cases'])

            # Añadir datos de los casos nuevos de muerte
            if(row['new_deaths'] is None or row['new_deaths'] < 0):
                fila_muertes_nuevas.append(0)  # meter un cero o dejarlo vacio ?
            else:
                fila_muertes_nuevas.append(row['new_deaths'])


        return  casos_totales, nuevos_casos, nuevas_muertes
        0

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Problema: solo tengo una opción a seleccionar que es intel, debo buscar los datos de otras marcas para poder comprar, no dan chance para los de machine learning
class ParseCpu:

    def __init__(self):
        #print("En proceso")
        self.df = pd.read_csv("data/CPU.csv")

    def getDataset(self):
        data = Dataset("CPU")
        data.setIntFuente(5)
        data.setOpciones(self.getOpciones()) 
        #----------
        data.addOpcionEje("Cores")
        data.addOpcionEje("Cantidad de hilos")
        data.addOpcionEje("Frecuencia(GHz)")
        data.addOpcionEje("Cache(M)")
        #----------
        cores, hilos, frecuencia, cache = self.getDatos()
        data.addElementoEje(cores)
        data.addElementoEje(hilos)
        data.addElementoEje(frecuencia)
        data.addElementoEje(cache)


        #data.setTiposGraficas(["1:  Linea Terminal", "2: Linea html", "3: Linea navegador","4: Barras navegador", 
        #                      "6: dispersion navegador", "7: box terminal", "9: Histograma Terminal", "0: Pruebas"]) # "5. Dispersion terminal"
        data.setTiposGraficas(tiposGraficas)
        return data

    def getOpciones(self):
        #return np.unique(self.df.loc[:,'Name'].to_numpy()).tolist()
        return ["Intel"]    # Todos estos datos corresponden a los procesadores intel

    def getDatos(self):
        core = []
        hilos = []
        frecuencia = []
        cache = []
        for index, row in self.df.iterrows(): 
            if (row['Cores'] is None ) or (row['Threads'] is None ) or (row['Speed(GHz)'] is None) or (row['Cache(M)'] is None ):
                continue    # Si alguno de los valores falta esa linea no me interesa
            core.append(row['Cores'])
            hilos.append(row['Threads'])
            frecuencia.append(row['Speed(GHz)'])
            cache.append(row['Cache(M)'])
        return core, hilos, frecuencia, cache


 # TODO poner las etiquetas para perdedor y ganador | osea generar la opcion a seleccionar de ganador y perdedor
 # Meter mas datos disponible dentro de los ficheros
 # intentar optimizar el get dataset ya que COLAPSA TODO, PETA MUY FUERTE
class ParseLol:

    def __init__(self):
        self.df = pd.read_csv("data/Lol_winner.csv")
        self.df2 = pd.read_csv("data/Lol_looser.csv")

    def getDataset(self):
        data = Dataset("Corean rankeds")
        #data.setIntFuente()
        data.setOpciones(self.getOpciones())
        #----------
        data.addOpcionEje("Towerkilss")
        data.addOpcionEje("InhibitorKills")
        data.addOpcionEje("baronKills")
        data.addOpcionEje("riftHeraldKills")
        #----------
        # Guardo los datos de los ganadores
        torres1, inhibidores1, barones1, heraldo1 = self.getDatos(self.df)
        #etiquetas = ["Winner"] * len(torres)
        # Guardo los datos de los perdedores
        torres2, inhibidores2, barones2, heraldo2 = self.getDatos(self.df2)
        # Los combino
        #for i in range(len(torres2)):
        #    torres.append(torres2[i]) 
        #    inhibidores.append(inhibidores2[i])
        #    barones.append(barones2[i])
        #    heraldo.append(heraldo2[i])
        #    etiquetas.append()

        torres = []
        torres.append(torres1)
        torres.append(torres2)

        inhibidores = []
        inhibidores.append(inhibidores1)
        inhibidores.append(inhibidores2)

        barones = []
        barones.append(barones1)
        barones.append(barones2)

        heraldo = []
        heraldo.append(heraldo1)
        heraldo.append(heraldo2)

        data.addElementoEje(torres)
        data.addElementoEje(inhibidores)
        data.addElementoEje(barones)
        data.addElementoEje(heraldo)


        data.setTiposGraficas(["1:  Linea Terminal", "2: Linea html", "3: Linea navegador","4: Barras navegador", 
                              "6: dispersion navegador", "7: box terminal", "9: Histograma Terminal", "0: Pruebas"]) # "5. Dispersion terminal"
        return data


    def getDatos(self, data):
        torres = []
        inhibidores = []
        barones = []
        heraldo = []
        for index, row in data.iterrows(): 
            torres.append(row['towerKills'])
            inhibidores.append(row['inhibitorKills'])
            barones.append(row['baronKills'])
            heraldo.append(row['riftHeraldKills'])


        return torres, inhibidores, barones, heraldo

    def getOpciones(self):
        #return np.unique(self.df.loc[:,'Name'].to_numpy()).tolist()
        return ["Winner","Losers"]    # Todos estos datos corresponden a corea


#  
# Esta distribuido por tipo de pokemon para hacer el machine learning más interesante
# Tiene etiquetas
class ParsePokemon:

    def __init__(self):
        self.df = pd.read_csv("data/Pokemon.csv")

    def getDataset(self):
        data = Dataset("Pokemon")
        #data.setIntFuente()
        
        #----------
        #data.addOpcionEje("Tipo1") # Los tipso seran las opciones
        #data.addOpcionEje("Tipo2")
        data.addOpcionEje("Sumatorio estadisticas")
        data.addOpcionEje("HP")
        data.addOpcionEje("Atk")
        data.addOpcionEje("Defense")
        data.addOpcionEje("Sp. Atk")
        data.addOpcionEje("Sp. Def")
        data.addOpcionEje("Speed")

        #----------
        #  TODO LLAMAR A GET DATOS , GUARDAR LOS DATOS EN EL DATASET Y PROBAR EL DATASET
        data.setOpciones(self.getOpciones()) # Las opciones seran los tipos de los pokemons
        #data.setEtiquetas()
        total, hp, atk, defense, spAtk, spDef, speed = self.getDatos()
        data.addElementoEje(total)
        data.addElementoEje(hp)
        data.addElementoEje(atk)
        data.addElementoEje(defense)
        data.addElementoEje(spAtk)
        data.addElementoEje(spDef)
        data.addElementoEje(speed)

        #data.setTiposGraficas(["1 :  Linea Terminal", "2 : Linea html", "3 : Linea navegador","4 : Barras navegador", 
        #                      "6 : dispersion navegador", "7 : box terminal", "9 : Histograma Terminal", "10: Histograma navegador","11: vecino", "0 : Pruebas"]) # "5. Dispersion terminal"
        data.setTiposGraficas(tiposGraficas)  
        return data
    #Si te preguntas por que hago una función que solo sera llamda una única vez es para que si tengo que modificar como guardar los dtos
    # se que se encuentra todo dentro de esta función y así no ensució la función principal
    def getDatos(self):
        tipos = []
        total = []
        hp = []
        atk = []
        defense = []
        spAtk = []
        spDef = []
        speed = []
        # Sacar los tipos sin repetir en una lista | ya lo tengo de las opciones asi que debo pasarselo o no
        tipos = self.df['Type 1'].unique().tolist()
        # Añado tantas listas secundarias en los almacenamientos como tipos haya
        for i in range(len(tipos)):
            total.append([])
            hp.append([])
            atk.append([])
            defense.append([])
            spAtk.append([])
            spDef.append([])
            speed.append([])


        # Para cada linea tengo que comprobar que tipo es y saber en que posición esta la lista a la que pertenece
        for index, row in self.df.iterrows(): 
            #nombres.append(row['Name'])
            #tipos.append( (row['Type 1'], row['Type 2']))   # combino los dos por que importan si es simple o doble, y cuales son esos atributos
            i = tipos.index(row['Type 1'])  # Saco el indice de donde se guardaran los datos
            #if(): 
            #    continue      # Si el indice no existe debido a que tiene el tipo vacio que continue | tambien se podria comprobar ants de intentar sacar el indice

            total[i].append( row['Total'])
            hp[i].append(row['HP'])
            atk[i].append(row['Attack'])
            defense[i].append(row['Defense'])
            spAtk[i].append(row['Sp. Atk'])
            spDef[i].append(row['Sp. Def'])
            speed[i].append(row['Speed'])


        return total, hp, atk, defense, spAtk, spDef, speed

    # Las opciones seran los tipos de los pokemons
    def  getOpciones(self):

        return self.df['Type 1'].unique().tolist()

    # Sinceramente se que deben de haber otras formas de organizar la información en vez de tener que declarar tantas listas pero solo quiero terminar esto
class ParseStroke:

    def __init__(self):
        self.df = pd.read_csv("data/Stroke-data.csv")

    def getDataset(self):
        data = Dataset("Derrame")
        #data.setIntFuente()
        #data.setOpciones()


        #----------
        data.addOpcionEje("Genero")
        data.addOpcionEje("Edad")
        data.addOpcionEje("Hypertension")
        data.addOpcionEje("Problemas de corazon")
        data.addOpcionEje("Trabajo")
        data.addOpcionEje("Residencia")
        data.addOpcionEje("Glucosa")
        data.addOpcionEje("Bmi")
        data.addOpcionEje("Fumador")

        data.setOpciones(self.getOpciones()) # LAs opcuiiones

        #----------
        genero,edad,hypertension,corazon,trabajo,residencia,glucosa,bmi,fumador = self.getDatos()
        data.addElementoEje(genero)
        data.addElementoEje(edad)
        data.addElementoEje(hypertension)
        data.addElementoEje(corazon)
        data.addElementoEje(trabajo)
        data.addElementoEje(residencia)
        data.addElementoEje(glucosa)
        data.addElementoEje(bmi)
        data.addElementoEje(fumador)

        data.setTiposGraficas(tiposGraficas)
        return data

    def getDatos(self):
        opciones = self.df['stroke'].unique().tolist() # Las opciones que seran mostradas al usuario
        gender = []
        age = []
        hypertension = []
        heart_disease = []
        work = []
        residence = []
        glucose = []
        bmi = []
        smoking = []
        for i in range(len(opciones)):
            gender.append([])
            age.append([])
            hypertension.append([])
            heart_disease.append([])
            work.append([])
            residence.append([])
            glucose.append([])
            bmi.append([])
            smoking.append([])

        for index, row in self.df.iterrows():
            i = opciones.index(row['stroke'])  # Saco el indice de donde se guardaran los datos
            gender[i].append(row['gender'])
            age[i].append(row['age'])
            hypertension[i].append(row['hypertension'])
            heart_disease[i].append(row['heart_disease']) 
            work[i].append(row['work_type'])
            residence[i].append(row['Residence_type'])
            glucose[i].append(row['avg_glucose_level'])
            bmi[i].append(row['bmi']) # Cuidado con valores raros
            smoking[i].append(row['smoking_status'])

        return gender,age,hypertension,heart_disease,work,residence,glucose,bmi,smoking

    def  getOpciones(self):

        return self.df['stroke'].unique().tolist()

#adfasf
