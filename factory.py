#!/usr/bin/env python
# -*- coding: utf-8 -*-
from leerDatos import ParseCasosConfirmados, ParseAccidentesTrafico, ParseParoEspaña
from grafica_mat import Linea_mat
from grafica_pygal import Linea_pygal, Box_pygal
from clases_base import Grafica
from grafica_ploty import Lineas_plotly, Barras_plotly, Mapa_plotly, Scatter_plotly

# NO ES UN PATRON FACTORY, tengo que cambiarle el nombre y actualizar las referencias
class Factory:

    # este metodo devolvera el tipo de parse dependiendo de la ruta
    # To do analizar la ruta para decidir el tipo de parse | para esto primero hay que arreglar la estructura de los parse
    # antes que analizar la ruta hacer lo mismo que con el tipo de grafica
    def getParse(ruta):
        switcher = {
            1: ParseCasosConfirmados,
            2: ParseAccidentesTrafico,
            3: ParseParoEspaña
        }

        return switcher.get(int(ruta))
        #return ParseCasosConfirmados(ruta)
        #return ParseAccidentesTrafico(ruta)

    def grafica(eleccion, contexto):
        switcher = {
            1: Linea_mat,
            2: Linea_pygal,
            3: Lineas_plotly,
            4: Barras_plotly,
            5: Mapa_plotly,
            6: Scatter_plotly,
            7: Box_pygal
        }

        elec = switcher.get(int(eleccion))
        contexto.setGrafica(elec)



#gfsdfgsdf
