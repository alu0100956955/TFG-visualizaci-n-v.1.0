#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
from leerDatos import ParseCasosConfirmados
import numpy as np
from clases_base import Grafica
from datetime import datetime
import scipy.stats as st    # Para la linea de densidad en los histogramas | Regresion lineal
import math
import seaborn as sns
from sklearn.cluster import KMeans
#from scipy import scipy

#import geopandas as gpd 
#TAmbien hay que instalar descartes

#l = Lector('data/casos_2019.csv')
class auxiliar():
    def comprobarDias(data, eleccion):
        if (eleccion == "Dias"):
            diasFormateado = []
            for i in data:
                diasFormateado.append(datetime.strptime(i,'%m/%d/%y'))
            #diasMat = matplotlib.dates.date2num(diasFormateado)
            return diasFormateado
        return data #Si no es la elección dias devolvera el conjunto de datos igual



class Linea_mat(Grafica):


#funcion encargada de hacer que no aparezcan todos los valores ya que eso hara la vision mas jodida | solo si es string algun eeje
    def ticks(self,array):
        i = 0
        for x in array:
            if(i%2==0):
                add(i)
                i +=1

# TO DO:
# El metodo para poder rotar entre los distintso tipos de lineas ( mirar hojas)
# probar mas tipos de graficas
# Permitir distintos tipos de graficas o tener distintos metodos para hacere las graficas
    def show(data):
        #paises = ['Spain','Italy','China','Portugal']
        plt.clf() # Para limpiar graficas anteriores
        seleccionados = data.getSeleccionados()
        for i in range(len(seleccionados)): # Lo hago con el rango para los metodos complementarios
            #TO DO: pasar de forma parametrizada el eje que se quiere representar
            # SE BUGEA PORQUE AL PASARLE LOS DIAS YA ESPACIADOS NO RECONOCE ESE DATO Y LO PONE MAL

            #ejeX = auxiliar.comprobarDias(data.getEje(data.getSeleccionEjeX(),seleccionados[i]), data.getSeleccionEjeX())
            #ejeY = auxiliar.comprobarDias(data.getEje(data.getSeleccionEjeY(),seleccionados[i]), data.getSeleccionEjeY())
            ejeX = data.getEje(data.getSeleccionEjeX(),seleccionados[i])
            ejeY = data.getEje(data.getSeleccionEjeY(),seleccionados[i])

            ejeX,ejeY = Linea_mat.sort(ejeX,ejeY)
            #print(ejeX)
            #print(ejeY)

            plt.plot(ejeX,ejeY, marker = Linea_mat.marker(i), linestyle = Linea_mat.line(i), markeredgecolor = Linea_mat.color(i) , label = seleccionados[i])
            # TO DO falta quitar lo de ejeY y poner solo getEje
            #plt.text(len(data.getEje("Dias",0)),data.getEjeY(seleccionados[i])[-1],s = seleccionados[i]) # Para que aparezcan los nombres de los elementos al final de la linea
        #plt.xticks(ticks=Linea_mat.rango(data),labels=data.getEjeX(),rotation=70)
        #plt.xticks(ticks=Grafica.espaciar(data.getEje("Dias",0)),labels=data.getEjeX(),rotation=1)  # ARREGLAR
        #plt.xticks(ticks=data.getEje("Dias",0),labels=data.getEje("Dias",0),rotation=1)
        plt.xticks(rotation=1)
        #plt.set_ylabel(data.getSeleccionEjeY())
        #plt.set_xlabel(data.getSeleccionEjeX())
        plt.xlabel(data.getSeleccionEjeX())
        plt.ylabel(data.getSeleccionEjeY())
        plt.title(data.getTitle())
        plt.legend()
        plt.grid()
        plt.show()

# To do : controlar cuando se sale de rango, si se pasa restarle la cantidad del array o hacer % o una division...
# Controlar cuando se salga del limite
    # Metodo que devuelve el tipo de marca
    def marker(indice):
        if (indice > 21):
            return marker(indice -21)
        else:
            markers = ['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd', '|', '_' ]
        return markers[indice]

    # Metodo que devuelve el tipo de linea
    def line(indice):
        if ( indice > 3):   # Si el indice es mayor que la cuarta posicion le restamos 4 y empleamos la recursividad
            return line(indice-4)
        else:
            line = ['-', '--', '-.', ':' ]
        return line[indice]

    # Metodo que devuelve el color de la linea
    def color(indice):
        if( indice > 7):
            return color(indice - 7)
        else:
            colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w' ]
        return colors[indice]

    # En caso de que el ejeX sea numerico lo ordena
    # Le paso los dos ejes para que el valor de Y sea el que le corresponde
    def sort(ejex,ejey): 
        # https://www.programiz.com/python-programming/methods/built-in/sorted
        if( (isinstance(ejex[0],int)) or (isinstance(ejex[0],float))  ):# Si es un int o float hay que ordenar
            ejex, ejey = (list(t) for t in zip(*sorted(zip(ejex, ejey))))
        
        return ejex, ejey

    def prueba():
        a = l.ejeX(4)
        print(a)
        a = l.ejeX(12)
        print(a)



class Barras_matplotlib(Grafica):

    # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.bar.html

    def show(data):
        plt.clf() # Para limpiar graficas anteriores
        seleccionados = data.getSeleccionados()
        fig, ax = plt.subplots()

        for i in range(len(seleccionados)): 

            ejeX = data.getEje(data.getSeleccionEjeX(),seleccionados[i])
            ejeY = data.getEje(data.getSeleccionEjeY(),seleccionados[i])
            ax.bar(ejeY,label=seleccionados[i])

            #plt.bar(ejeX,ejeY , label = seleccionados[i])

        plt.xlabel(data.getSeleccionEjeX())
        plt.ylabel(data.getSeleccionEjeY())
        plt.show()

    def media(matriz):
        aux = []
        media = []
        x = len(matriz[0])
        for i in range(x):
            aux = 0
            for row in matriz:
                aux += row[i]
            media.append(aux/x)
        return media

    def varianza():
        aux = []

    # Para calcular el maximo de cada columna
    def maximo():
        aux = []
        maximo = []
        x = len(matriz[1])
        for i in range(x):
            for row in matriz:
                if(aux < row[i]):
                    aux = row[i]
            maximo.append(aux)
        return maximo

    # Para calcular el minimo de cada columna
    def minimo():
        aux = []
        minimo = []
        x = len(matriz[1])
        for i in range(x):
            for row in matriz:
                if(aux > row[i]):
                    aux = row[i]
            minimo.append(aux)
        return minimo

    def desviacionMedia():
        aux = []


# Scatter : https://matplotlib.org/3.2.2/gallery/lines_bars_and_markers/scatter_with_legend.html#sphx-glr-gallery-lines-bars-and-markers-scatter-with-legend-py
class Scatter_matplotlib(Grafica):
    # TODO: Leyendas para los ejes
    def show(data):
        #print("Scatter matplotlib")
        plt.clf() # Para limpiar graficas anteriores
        fig, ax = plt.subplots()
        seleccionados = data.getSeleccionados()
        for selec in seleccionados:
            ax.scatter(data.getEje(data.getSeleccionEjeX(),selec),data.getEje(data.getSeleccionEjeY(),selec),alpha=0.3)
        
        ax.legend()
        ax.grid(True)

        plt.show()

class Box_matplotlib(Grafica):

    def show(data):
        plt.clf() # Para limpiar graficas anteriores
        seleccionados = data.getSeleccionados()
        ejeY = []
        for selec in seleccionados:
            #ejeY = auxiliar.comprobarDias(data.getEje(data.getSeleccionEjeY(),selec), data.getSeleccionEjeY())
            ejeY.append( data.getEje(data.getSeleccionEjeY(),selec))
        plt.boxplot(ejeY,labels=seleccionados)
        plt.ylabel(data.getSeleccionEjeY()) # Label del eje Y
        #plt.ylabel("Recuento de veces") # Label del eje Y
        plt.title(data.getTitle())
        plt.show()


class Histograma_matplotlib(Grafica):

    def show(data):
        # TO DO: revisar los ejes que se usan
        
        #for selec in seleccionados:# TO DO, por ahora solo cojo el ejeY pero tengo que controlar si me lo pone en el eje X
        #    matriz.append(data.getEje(data.getSeleccionEjeY(),selec))   #TO DO: como se guarda este dato | empleare los metodos de mas abajo
        #TO DO dependiendo de la eleccion del usuario que se haga la operacion correcta a los datos
        #ejeY = Histograma_matplotlib.media(matriz)

        #if(cantidad de seleccionados = par) mitad y mitad, ej: 6 = 3,3
        #else dividir mitad y mitad pero sumo uno a la primera, ej 7 = 4,3

        #funcion = Histograma_matplotlib.switch(data.getIntFuente())   #ESTA CABLEADO POR AHORA
        #ejeY = funcion(data)
        plt.clf() # Para limpiar graficas anteriores
        seleccionados = data.getSeleccionados()
        x,y = Histograma_matplotlib.dimensiones(len(seleccionados))
        #plt.title(data.getTitle())  # Le asigno el titulo a la gráfica
        
        for i in range(len(seleccionados)):
            plt.subplot(x,y,i+1)
            ejeY = data.getEje(data.getSeleccionEjeY(),seleccionados[i])
            plt.hist(ejeY, density=True, bins = 10)
            # Esto me genera un intervalo de x ticks según el minimo y el máximo del eje que le indique
            #ticks = np.linspace(min(ejeY),max(ejeY),10).astype(int) 
            #plt.xticks(ticks) # Para los ticks del ejeX
            plt.ylabel("Frecuencia valores") # Label del eje Y
            plt.title(seleccionados[i])
            plt.xlabel(data.getSeleccionEjeY())
            #kde = st.gaussian_kde(ejeY)
            #plt.plot(ticks, kde.pdf(ticks), label="PDF")
            # https://towardsdatascience.com/histograms-and-density-plots-in-python-f6bda88f5ac0
            sns.distplot(ejeY, hist = False, kde = True, rug = True,
             color = 'darkblue', 
             kde_kws={'linewidth': 2},
             rug_kws={'color': 'black'},
             norm_hist=False)   # norm_hist es lo que me permite controlar si sera densidad o cuenta

        
        #plt.hist(ejeY, density=False, bins = 30)    # bins es la cantidad de columnas
         # Pese a que 
        plt.tight_layout(3.0)   # Para ajustar la separación entre gráficas
        
        #plt.xlabel(data.getSeleccionEjeX())
        # TO DO: controlar si el usuario ha elegido algo que no es numerico
        #plt.xticks(Histograma_matplotlib.getTicks(ejeY,10))
        
        plt.show()

    # Metodo para saber cuantas graficas habra y poder ajustar las dimensiones de las columnas y filas
    def dimensiones(cantidad):
        raiz = math.sqrt(cantidad)  # Hago la raiz cuadrada
        dimension = math.ceil(raiz) # Redondeo hacia arriba para que siempre este numero por si mismo sea mayor o igual que la cantidad de subplots
        return dimension, dimension
        
    # Metodo para obtener un array de donde deben estar situados los ticks del eje | OBSOLETO
    def getTicks(valores,cantidadTicks):
        diferencia = max(valores) /  cantidadTicks # La diferencia entre ticks es el maximo dividido entre la cantidad de ticks que quiero
        ticks = [0]  # Array con los ticks para el eje
        for i in range(cantidadTicks): #El bucle para añadir la diferencia por cada ticks
            ticks.append(ticks[i]+diferencia)

        return ticks

    # Metodos para llevar a cabo las operaciones sobre los datos del histograma
    # Para cada metodo se pasara la matriz con los datos numericos
    # OBSOLETO
    def switch(eleccion):
        switcher = {
            1: Histograma_matplotlib.diario,
            2: Histograma_matplotlib.sinTratar,
            3: Histograma_matplotlib.sinTratar,
            4: Histograma_matplotlib.sinTratar
            }
        return switcher.get(eleccion)

    # Metodo para calcular la cantidad de contagios diarios debido a que se acumulan la cantidad diaria
    def diario(data):
        seleccionados = data.getSeleccionados()
        matriz = []
        for i in range(len(seleccionados)):
            if(i == 0):
                matriz = Histograma_matplotlib.diarioArray(data.getEje(data.getSeleccionEjeY(),seleccionados[i]))
                continue
            matriz += Histograma_matplotlib.diarioArray(data.getEje(data.getSeleccionEjeY(),seleccionados[i]))
        return matriz


    # Metodo auxiliar que le paso un array y medice cuanto es diario dependiendo del valor actual y del dia anterior
    def diarioArray(array):
        aux = []
        aux.append(array[0])    # Guardo el primer elemento
        for i in range(len(array)-1):# Lo hago hasta una antes por como guardo el valor
            aux.append(array[i+1]-array[i]) #Al dia siguiente le resto el dia anterior para tener los contagios de ese dia

        return aux

    # Para las fuentes de datos que no necesitan ser tratadas para el histograma
    def sinTratar(data):
        seleccionados = data.getSeleccionados()
        matriz = []
        for i in range(len(seleccionados)):
            if(i == 0):
                matriz = data.getEje(data.getSeleccionEjeY(),seleccionados[i])
                continue
            matriz += data.getEje(data.getSeleccionEjeY(),seleccionados[i])
        return matriz

    # What, pero si ya tengo un metodo de scatter??
class Clustering_matplotlib(Grafica):
    # primero guardar todos los putos X e Y cada uno en un respectivo array
    # Segundo generar los conjuntos de entrenamiento y visualización / creo que no hace falta entrenar
    # Tercero crear el Kmeans para hacer clusterin, osea el encargado de hacer el clustering sea cual sea su nombre
    # Cuarto pasarle los puntos al Kmeans
    # Quinto con el modelo hacer scatter (con diferente color para cada uno ) de los distintos nucleos (mirar como disferenciar entre nucleos)
    def show(data):
        plt.clf() # Para limpiar graficas anteriores
        seleccionados = data.getSeleccionados()
        x = []
        y = []
        kmeans = KMeans(n_clusters = len(seleccionados)) # La cantidad de nucleos sera la cantidad de opciones seleccionados
        for i in range(len(seleccionados)):
            x += (data.getEje(data.getSeleccionEjeX(),seleccionados[i]))
            y += (data.getEje(data.getSeleccionEjeY(),seleccionados[i]))
        
        # https://docs.python.org/3.4/library/functions.html#zip
        puntos = list(zip(x,y)) # https://stackoverflow.com/questions/41468116/python-how-to-combine-two-flat-lists-into-a-2d-array/41468178
        #print(puntos)
        Npuntos = np.array(puntos)
        kmeans.fit(Npuntos)
        clusters = kmeans.cluster_centers_ # Donde cree scikit que estan los centros
        prediccion = kmeans.fit_predict(puntos)
        # voy a cablearlo para 1
        plt.scatter(Npuntos[prediccion == 0,0], Npuntos[prediccion == 0,1], color='red')
        #plt.scatter(puntos[y_km == 1,0], puntos[y_km == 1,1], color='green')
        #plt.scatter(clusters[0][0], clusters[0][1], marker='*', s=200, color='black')
        #plt.scatter(clusters[1][0], clusters[1][1], marker='*', s=200, color='black')
    
        plt.show()

# Aun que no sea matplot lib al ser por terminal dejo la representacion de mapas de geopandas dentro de este fichero
class mapa_Geopandas():
    def show():
        print("problemas en los paquetes") # el código funciona en la zona de pruebas de jupyter
        # Pero si dejo aqui el código entonces el framework no se ejecutara
#adfasfd




