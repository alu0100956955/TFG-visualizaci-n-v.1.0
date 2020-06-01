#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

# Clase que contendra los datos del parse
class Dataset:

    def __init__(self,title):
        self.title = title
        #Inicializo las variables para almacenar los ejes y que representa cada eje
        self.OpcionesEje = []
        self.matrizEje = []

    def setEjeY(self,matriz):
        self.ejey = matriz

    def getEjeY(self,eleccion):
        #return self.searchRow(self.searchIndex(eleccion))
        #Para probar si la modificacion funciona igual
        #print(self.ejey)
        #index = self.opciones.index(eleccion)
        #print(type(self.opciones))   # numpy.ndarray
        index = np.where(self.opciones == eleccion)# El where devuelve una tupla, que cada elemento es un nunpy ndarray por eso tengo que
        return self.ejey[index[0][0]]

    def setEjeX(self,array):
        self.ejex = array


    def getEjeX(self):
        return self.ejex


    def getTitle(self):
        return self.title

    # Esto hay que eliminarlo no es optimo
    # En vez de set paises deberia ser setTodasLasOpciones, esto es debido a que son todas las opciones incluidos duplicados
    def setTodasLasOpciones(self, array):
        self.TOpciones = array

    # Le pasamos un pais y nos devulve un array con la posicion o posiciones del pais | en vez de pais que sea
    # Le indicamos la opcion que escogio el usuario y nos indica el indice de la fila en la que se encuentra
    def searchIndex(self, opcion):
        posicion = []   # Lo hago array por si hay mas de una opcion
        for index in range(len(self.TOpciones)):
            if(self.TOpciones[index] == opcion):
                posicion.append(index)
        return posicion

    # Le pasamos las posiciones del pais, busca las filas corresponcientes, las suma y nos devuelve el array resultado, si no encuentra nada devuelve el array con un cero
    def searchRow(self,posicion):
        primera = True
        rows = [0]
        for i in posicion:
            if(primera):
                primera = False
                rows = self.ejey[i]
                continue
            rows += self.ejey[i]
        return rows

    #Array con las distintas opciones de lo que se puede representar
    def setOpciones(self, opciones_):
        self.opciones= opciones_

    def getOpciones(self):
        return self.opciones

    def setSeleccionados(self, selec):
        self.seleccionados = selec

    def getSeleccionados(self):
        return self.seleccionados


    #------------------------------------ Actualización dataset ------------------------#
    # Los datos para cada eje
    def addElementoEje(self,elemento):
        self.matrizEje.append(elemento)

    # Las opciones para cada eje
    def addOpcionEje(self,opcion ):
        self.OpcionesEje.append(opcion)


    #Este metodo devuelve las opciones que se pueden representar en los ejes
    def getOpcionesEje(self):
        return self.OpcionesEje

    # Parametros:
    # eje: (string) indica que eje se representa
    # elemento: (string) nos indica que elemento se quiere representar con respecto a las distintas opciones_
    # Hay que sacar de la matrz de ejes con el indice el elemento que necesitamos, si su primer elemento NO es un array significa que no es una matriz por tanto la devolvemos sin hacer mas comprobaciones
    # Si por el contrario es una matriz buscaremos el indice del elemento que nos han pasado ( hacer un metodo para buscar el indice segun el array de opciones) y lo usamos para pasar la fila correcta de la matriz
    # TO DO: si no encuentra el elemento que devuelva algo aunque sea
    def getEje(self, eje, elemento):
        matriz = self.matrizEje[self.indexEje(eje)]
        #print(matriz)
        # Esta condicion tengo que cambiarlo por ver su tamaño
        #print(type(matriz[0]))
        #if ( type(matriz) != list):
        #Si es un array lo devuelvo tal cual
        if (self.ifArray(matriz) ): # Si no es una matriz devulvo tal cual la matriz porque es un array
            return matriz
        # Devolveremos la fila del elemento indicado, para saber el index miramos el indice que tiene en el array de opciones ya que TODAS las matrices estan ordenadas siguiendo el array de opciones
        #print(self.matrizEje[self.opciones.index(elemento)])
        #index = np.where(self.opciones == elemento) # esto podria meterlo en una funcion ya que lo uso en dos partes
        #print(elemento)
        index = self.opciones.index(elemento)
        #print(index)
        return matriz[index]

    #Metodo para comprobar si el elemento existe | para mapas basicamente
    def existeElemento(self, elemento):
        esta = False
        for i in self.opciones:
            if (i == elemento):
                esta = True
        return esta

    # Metodo para saber si es un array la matriz (dabe de haber forma mas optimas, como ver sus dimensiones pero por ahora asi se queda)
    # TO DO: revisar otra forma de hacerlo
    def ifArray(self,matriz):
        # Si es un numpy array
        #print(type(matriz[0]))
        if(type(matriz[0]) == str ):
            return True
        if(type(matriz[0]) == int ):
            return True
        return False


    # Le pasamos un eje y nos dice en que posicion se encuenta en la matriz de eje | innecesario ?¿
    def indexEje(self, eje):
        #print(self.OpcionesEje)
        return self.OpcionesEje.index(eje)

    def setSeleccionEjeX(self, eleccion):
        self.ejeX = eleccion

    def getSeleccionEjeX(self):
        return self.ejeX

    def setSeleccionEjeY(self, eleccion):
        self.ejeY = eleccion

    def getSeleccionEjeY(self):
        return self.ejeY

#asdfasf
