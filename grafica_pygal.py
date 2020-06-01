#!/usr/bin/env python
# -*- coding: utf-8 -*-
from leerDatos import ParseCasosConfirmados
import pygal
from clases_base import Grafica
import numpy as np



class Linea_pygal(Grafica):

# TO DO
# probar mas tipos de graficas
# Cambiar la forma de pedir los datos en las graficas
#Comprobar el self de show
# Si el eje X no es datetime PETA
    def show(data):
        seleccionados = data.getSeleccionados()
        #chart = pygal.Line(x_label_rotation=1) # de tipo linea la grafica
        #chart = pygal.Line()
        #chart = pygal.bar() # de tipo barras
        chart = pygal.Line(x_label_rotation=1)
        
        #chart.x_labels = Grafica.espaciar(data.getEjeX())  #para añadirle datos al ejex, se ve muy pequeño pero si se pasa el raton se ve bien

        # Esto es para poner la orientacion dependiendo de donde ubique los datos de tipo temporal
        if(Linea_pygal.orientacion(data.getSeleccionEjeX())):
            
            chart.x_labels = data.getEje(data.getSeleccionEjeX(), 0)
            for selec in seleccionados:
                chart.add(selec, data.getEje(data.getSeleccionEjeY(), selec))
        else:
            chart = pygal.HorizontalLine()
            chart.x_labels = data.getEje(data.getSeleccionEjeY(), 0)
            for selec in seleccionados:
                chart.add(selec, data.getEje(data.getSeleccionEjeX(), selec))

        chart.title = data.getTitle()
        
        

        #chart.x_labels = l.labelsX(l.ejeX()) # no los reconoce como valores asique los apila igual pero como son menos pos quedan todos apretados al principio
        chart.render_to_file('output/lineas_pygal.html')
        #chart.render_in_browser()
        #chart.render()

    # metodo para saber la orientación de la gráfica con respecto a los datos no numericos, es decir si sera basica o en horizontal
    # True  si en el ejeX estan los dias, False si es al contrario
    def orientacion(eleccionX):
        if((eleccionX == 'Dias') or (eleccionX == 'Meses')):
            return True
        return False



class Box_pygal(Grafica):

        # es lo mismo pero solo varia la primera linea es decir la instancia pero en python tengo problemas para devolver nuevas instancias
    def show(data):
        seleccionados = data.getSeleccionados()
        #chart = pygal.Box(box_mode="pstdev")    # stander desviation
        chart = pygal.Box()

        chart.title = data.getTitle()
        chart.x_labels = data.getEje(data.getSeleccionEjeX(), 0)

        for selec in seleccionados:
            chart.add(selec, data.getEje(data.getSeleccionEjeY(), selec))
        chart.render_to_file('output/box_pygal.html')



#parse = Factory.parse('data/casos_2019.csv')
#Box_pygal.show(parse)

#asdfasdf
