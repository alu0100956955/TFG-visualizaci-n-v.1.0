from leerDatos import ParseCasosConfirmados
import pygal
from clases_base import Grafica
import numpy as np



class Linea_pygal(Grafica):

# TO DO
# probar mas tipos de graficas
# Cambiar la forma de pedir los datos en las graficas
#Comprobar el self de show
    def show(data):
        seleccionados = data.getSeleccionados()
        chart = pygal.Line(x_label_rotation=1) # de tipo linea la grafica
        #chart = pygal.Line()
        #chart = pygal.bar() # de tipo barras

        chart.title = data.getTitle()
        chart.x_labels = Grafica.espaciar(data.getEjeX())  #para añadirle datos al ejex, se ve muy pequeño pero si se pasa el raton se ve bien
        for selec in seleccionados:
            chart.add(selec, data.getEjeY(selec))

        #chart.x_labels = l.labelsX(l.ejeX()) # no los reconoce como valores asique los apila igual pero como son menos pos quedan todos apretados al principio
        chart.render_to_file('output/lineas_pygal.html')
        #chart.render_in_browser()

    

class Box_pygal(Grafica):

        # es lo mismo pero solo varia la primera linea es decir la instancia pero en python tengo problemas para devolver nuevas instancias
    def show(data):
        seleccionados = data.getSeleccionados()
        chart = pygal.Box(box_mode="pstdev")


        chart.title = data.getTitle()
        chart.x_labels = Grafica.espaciar(data.getEjeX())

        for selec in seleccionados:
            chart.add(selec, data.getEjeY(selec))
        chart.render_to_file('output/box_pygal.html')



#parse = Factory.parse('data/casos_2019.csv')
#Box_pygal.show(parse)

#asdfasdf
