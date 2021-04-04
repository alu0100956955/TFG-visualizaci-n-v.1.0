#!/usr/bin/env python
# -*- coding: utf-8 -*-
from leerDatos import ParseCasosConfirmados, ParseAccidentesTrafico, ParseParoEspaña, ParseCovid, ParseCpu, ParseLol, ParsePokemon, ParseStroke
from grafica_mat import Linea_mat, Box_matplotlib , Barras_matplotlib, Histograma_matplotlib, Scatter_matplotlib, Clustering_matplotlib
from grafica_pygal import Linea_pygal, Box_pygal
from clases_base import Grafica
from grafica_ploty import Lineas_plotly, Barras_plotly, Mapa_plotly, Scatter_plotly, Box_plotly, Histograma_plotly
from scikit import Gausian, Kneighbors, Tree, Linear, Gradient, Isotonic,AllRegresion, Kmeans, Mixture, DBscan,AllClustering, AllClasification, AllRegresion2

# NO ES UN PATRON FACTORY, tengo que cambiarle el nombre y actualizar las referencias
class Factory:

    # este metodo devolvera el tipo de parse dependiendo de la ruta
    # To do analizar la ruta para decidir el tipo de parse | para esto primero hay que arreglar la estructura de los parse
    # antes que analizar la ruta hacer lo mismo que con el tipo de grafica
    def getParse(ruta):
        switcher = {
            
            2: ParseAccidentesTrafico,
            3: ParseParoEspaña,
            4: ParseCovid,
            5: ParseCpu,
            6: ParseLol,
            7: ParsePokemon,
            8: ParseStroke
        }

        return switcher.get(int(ruta))
        #return ParseCasosConfirmados(ruta)
        #return ParseAccidentesTrafico(ruta)

        # TODO: limpiar las opciones del switch
    def grafica(eleccion, contexto):
        switcher = {
            1: Linea_mat,
            2: Linea_pygal,
            3: Lineas_plotly,
            4: Barras_plotly,
            5: Mapa_plotly,
            6: Scatter_plotly,
            7: Box_matplotlib,
            8: Box_plotly,
            9: Histograma_matplotlib,
            10: Histograma_plotly,
            11: Kneighbors,
            12: Gausian,
            13: Tree,
            14: Linear,
            15: Gradient,
            16: Isotonic,
            17: Kmeans,
            18: Mixture,
            19: DBscan,
            20: AllClasification,
            21: AllRegresion2,
            22: AllClustering,
            0: AllRegresion
        }
        # 0: cluestering

        elec = switcher.get(int(eleccion))
        contexto.setGrafica(elec)



#gfsdfgsdf
