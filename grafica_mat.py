#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
from leerDatos import ParseCasosConfirmados
import numpy as np
from clases_base import Grafica
from datetime import datetime

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


#funcion encargada de hacer que no aparezcan todos los valores ya que eso hara la vision mas jodida
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
        seleccionados = data.getSeleccionados()
        for i in range(len(seleccionados)): # Lo hago con el rango para los metodos complementarios
            #TO DO: pasar de forma parametrizada el eje que se quiere representar
            # SE BUGEA PORQUE AL PASARLE LOS DIAS YA ESPACIADOS NO RECONOCE ESE DATO Y LO PONE MAL

            ejeX = auxiliar.comprobarDias(data.getEje(data.getSeleccionEjeX(),seleccionados[i]), data.getSeleccionEjeX())
            ejeY = auxiliar.comprobarDias(data.getEje(data.getSeleccionEjeY(),seleccionados[i]), data.getSeleccionEjeY())
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

    def prueba():
        a = l.ejeX(4)
        print(a)
        a = l.ejeX(12)
        print(a)


class Box_matplotlib(Grafica):

    def show(data):

        seleccionados = data.getSeleccionados()
        ejeY = []
        for selec in seleccionados:
            #ejeY = auxiliar.comprobarDias(data.getEje(data.getSeleccionEjeY(),selec), data.getSeleccionEjeY())
            ejeY.append( data.getEje(data.getSeleccionEjeY(),selec))
        plt.boxplot(ejeY,labels=seleccionados)
        plt.title(data.getTitle())
        plt.show()


class Histograma_matplotlib(Grafica):

    def show(data):
        # TO DO: revisar los ejes que se usan
        seleccionados = data.getSeleccionados()
        matriz = []
        for selec in seleccionados:# TO DO, por ahora solo cojo el ejeY pero tengo que controlar si me lo pone en el eje X
            matriz.append(data.getEje(data.getSeleccionEjeY(),selec))   #TO DO: como se guarda este dato | empleare los metodos de mas abajo
        # TODO arreglar el eje X

        #TO DO dependiendo de la eleccion del usuario que se haga la operacion correcta a los datos
        ejeY = Histograma_matplotlib.media(matriz)
        plt.hist(ejeY, density=False)
        plt.ylabel(data.getSeleccionEjeY())
        plt.xlabel(data.getSeleccionEjeX())

        plt.show()

    # Metodos para llevar a cabo las operaciones sobre los datos del histograma
    # Para cada metodo se pasara la matriz con los datos numericos

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

# Aun que no sea matplot lib al ser por terminal dejo la representacion de mapas de geopandas dentro de este fichero
class mapa_Geopandas():
    def show():
        print("sin terminar")
#adfasfd


